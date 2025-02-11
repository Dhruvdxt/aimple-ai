from fastapi import HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from os import getenv
import os
import pyotp
import qrcode
from ...core.utils.auth import *
from ...core.utils.hashing import get_password_hash, verify_password
from ...repositories.activity_repository import *
from ...repositories.mfa_secret_repository import *
from ...repositories.session_repository import *
from ...repositories.user_repository import *
from ...schemas.user_schemas.request import *
from ...schemas.user_schemas.response import *
from ...schemas.base_schemas import TokenData, UserData
from ...services.mail_service.mail_types import verify_email, password_reset

def register(req_body: UserRegisterRequestSchema, request: Request) -> UserRegisterResponseSchema:
    try:
        if get_user_by_email(req_body.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="email_already_registered"
            )
        
        hashed_password = get_password_hash(req_body.password)
        
        user = create_user(req_body.email, hashed_password)
        ip_address = request.client.host
        create_activity(user_id=user.id, admin_id=0, activity_type=ActivityType.REGISTRATION, ip_address=ip_address)
        
        return UserRegisterResponseSchema(status_code=201)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def login(req_body: UserLoginRequestSchema, request: Request, response: Response) -> UserLoginResponseSchema:
    try:
        await check_login_attempts(req_body.email)
        
        user = await authenticate(req_body.email, req_body.password)
        
        if user.is_mfa_enabled:
            if req_body.otp is None: 
                raise HTTPException(status_code=400, detail="mfa_enabled_,_otp_required")
            mfa_secret = get_mfa_secret_by_user_id(user.id)
            totp = pyotp.TOTP(mfa_secret.secret)
            
            if not totp.verify(req_body.otp):
                raise HTTPException(status_code=400, detail="invalid_otp")
            
        await delete_record(user.id)
        
        # access_token = gen_access_token({"user_id": user.id})
        ip_address = request.client.host
        
        session = create_session(
            user_id=user.id,
            ip_address=ip_address
        )
        
        response.set_cookie(
            key=getenv('SESSION_COOKIE_NAME'),
            value=session.session_id,
            httponly=True,
            secure=False,
            samesite="Lax"
        )
        
        create_activity(user_id=user.id, admin_id=0, activity_type=ActivityType.LOGIN, ip_address=ip_address)
        
        return UserLoginResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    

def logout(request: Request, response: Response) -> UserLogoutResponseSchema:
    try:
        session_id = request.cookies.get(getenv('SESSION_COOKIE_NAME'))

        if session_id:
            delete_session_by_session_id(session_id)

        response.delete_cookie(getenv('SESSION_COOKIE_NAME'))

        return UserLogoutResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


def get_profile_data(session_id: str) -> UserGetProfileDataResponseSchema:
    try:
        session = get_session_by_session_id(session_id)
        user = get_user_by_id(session.user_id)
        return UserGetProfileDataResponseSchema(
            status_code=status.HTTP_200_OK,
            profile_data=UserData(
                id=user.id,
                email=user.email,
                full_name=user.full_name,
                phone=user.phone, 
                address=user.address,
                country=user.country,
                disabled=user.disabled,
                verified=user.verified,
                is_mfa_enabled=user.is_mfa_enabled
            )
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


def send_verify_email_mail(session_id: str) -> UserSendVerifyEmailMailResponseSchema:
    try:
        session = get_session_by_session_id(session_id)
        user = get_user_by_id(session.user_id)
        if user.verified:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user_is_already_verified")
        
        verification_token = gen_access_token({'user_id': user.id}, timedelta(minutes=5))
        verification_link = f"http://{getenv('DOMAIN')}:{getenv('PORT')}/api/v2/verify_email?token={verification_token}"
        verify_email.send_verify_email_mail(user.email, verification_link)
        
        return UserSendVerifyEmailMailResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
 
 
def enable_mfa(session_id: str, request: Request) -> UserEnableMFAResponseSchema:
    try:
        session = get_session_by_session_id(session_id)
        user = get_user_by_id(session.user_id)
        
        mfa_secret = get_mfa_secret_by_user_id(session.user_id)
        
        if not mfa_secret:
            secret = pyotp.random_base32()
            create_mfa_secret(session.user_id, secret)
        else:
            secret = mfa_secret.secret
            

        otp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=f"{user.email}", issuer_name="Aimple AI"
        )
        
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        QR_CODE_PATH = os.path.join(BASE_DIR, "../../public/qr_codes/mfa_qr_code.png")

        qr = qrcode.make(otp_uri)
        # buf = BytesIO()
        qr.save(QR_CODE_PATH)
        # buf.seek(0)

        # return StreamingResponse(buf, media_type="image/png")
    
        return UserEnableMFAResponseSchema(status_code=status.HTTP_200_OK, otp_uri="your_qr_code_has_been_saved_at_path_/server/public/qr_codes/mfa_qr_code.png")
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
 
 
def verify_first_otp(req_body: UserVerifyFirstOTPRequestSchema, session_id: str, request: Request) -> UserVerifyFirstOTPResponseSchema:
    try:
        session = get_session_by_session_id(session_id)
        mfa_secret = get_mfa_secret_by_user_id(session.user_id)
        
        if not mfa_secret:
            raise HTTPException(status_code=400, detail="mfa_not_initialized_for_this_user")

        totp = pyotp.TOTP(mfa_secret.secret)
        
        if totp.verify(req_body.otp):
            update_user_profile_data_by_id(session.user_id, {'is_mfa_enabled': True})
            ip_address = request.client.host
            create_activity(user_id=user.id, admin_id=0, activity_type=ActivityType.MFA_ENABLED, ip_address=ip_address)
            return UserVerifyFirstOTPResponseSchema(status_code=status.HTTP_200_OK)
        
        raise HTTPException(status_code=400, detail="invalid_otp")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
 

def disable_mfa(session_id: str, request: Request) -> UserDisableMFAResponseSchema:
    try:
        session = get_session_by_session_id(session_id)
        
        delete_mfa_secret_by_user_id(session.user_id)
        update_user_profile_data_by_id(session.user_id, {'is_mfa_enabled': False})
        
        ip_address = request.client.host
        create_activity(user_id=session.user_id, admin_id=0, activity_type=ActivityType.MFA_DISABLED, ip_address=ip_address)
        
        return UserDisableMFAResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


def update_profile_data(req_body: UserUpdateProfileDataRequestSchema, session_id: str, request: Request) -> UserUpdateProfileDataResponseSchema:
    try:
        session = get_session_by_session_id(session_id)
        update_data: dict = {k: v for k, v in req_body.update_data.model_dump().items() if v is not None}
        update_user_profile_data_by_id(session.user_id, update_data)
        
        ip_address = request.client.host
        create_activity(user_id=session.user_id, admin_id=0, activity_type=ActivityType.UPDATE_PROFILE, ip_address=ip_address)
        return UserUpdateProfileDataResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
     
     
def update_password(req_body: UserUpdatePasswordRequestSchema, session_id: str, request: Request) -> UserUpdatePasswordResponseSchema:
    try:
        session = get_session_by_session_id(session_id)
        user = get_user_by_id(session.user_id)
        if not verify_password(req_body.curr_password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="password_not_matched")
        
        hashed_password = get_password_hash(req_body.new_password)
        update_user_password_by_id(session.user_id, {'hashed_password': hashed_password})
        ip_address = request.client.host
        create_activity(user_id=user.id, admin_id=0, activity_type=ActivityType.PASSWORD_RESET, ip_address=ip_address)
        
        current_time = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        account_settings_url = f"http://{getenv('DOMAIN')}:{getenv('PORT')}/api/v1/account/settings"
        password_reset.send_password_reset_mail(user.email, current_time, account_settings_url)
            
        return UserUpdatePasswordResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


def delete(session_id: str, request: Request) -> UserDeleteResponseSchema:
    try:
        session = get_session_by_session_id(session_id)
        delete_user_by_id(session.user_id)
        delete_session_by_session_id(session.session_id)
        
        ip_address = request.client.host
        create_activity(user_id=session.user_id, admin_id=0, activity_type=ActivityType.ACCOUNT_DELETE, ip_address=ip_address)
        
        return UserDeleteResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))