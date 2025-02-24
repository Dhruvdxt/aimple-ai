from fastapi import HTTPException, status, Request, Response
from os import getenv
import os
import random
import pyotp
import qrcode
import user_agents
from ...core.utils.auth import *
from ...core.utils.hashing import get_password_hash, verify_password
from ...core.utils.network import get_ip_info
from ...repositories.activity_repository import *
from ...repositories.mfa_secret_repository import *
from ...repositories.session_repository import *
from ...repositories.user_repository import *
from ...schemas.user_schemas.request import *
from ...schemas.user_schemas.response import *
from ...schemas.base_schemas import *
from ...services.index import ServiceFactory, ServiceType, MailType, MProviderType, SProviderType
from ...services.sms_service.sms_sender import SMSSender , ProviderType
from ...services.mail_service import password_reset, reset_password
# from ...services.mail_service import verify_email



def register(req_body: UserRegisterRequestSchema, request: Request) -> UserRegisterResponseSchema:
    try:
        if get_user_by_email(req_body.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="email_already_registered"
            )
            
        hashed_password = get_password_hash(req_body.password)
    
        user = create_user(req_body.email, hashed_password)
        ip_info = get_ip_info(request)
        create_activity(user_id=user.id, activity_type=ActivityType.REGISTRATION, public_ip_address=ip_info.get('ip'), city=ip_info.get('city'), region=ip_info.get('region'), country=ip_info.get('country'), isp=ip_info.get('org'))
        
        return UserRegisterResponseSchema(status_code=201)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def login(req_body: UserLoginRequestSchema, request: Request, response: Response) -> UserLoginResponseSchema:
    try:
        await check_login_attempts(req_body.email)
        
        user = await authenticate(req_body.email, req_body.password)
        
        # if not user.verified:
        #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="verify_your_email_first")
        
        if user.is_mfa_enabled:
            if req_body.otp is None: 
                raise HTTPException(status_code=400, detail="mfa_enabled_,_otp_required")
            mfa_secret = get_mfa_secret_by_user_id(user.id)
            totp = pyotp.TOTP(mfa_secret.secret)
            
            if not totp.verify(req_body.otp):
                raise HTTPException(status_code=400, detail="invalid_otp")
        
        await delete_record(user.id)
        
        ip_address = request.client.host
        user_agent = user_agents.parse(request.headers.get('user-agent'))
        
        session = create_session(
            user_id=user.id,
            ip_address=ip_address,
            device=user_agent.device.family,
            os=user_agent.os.family,
            browser=user_agent.browser.family
        )
        
        response.set_cookie(
            key=getenv('SESSION_COOKIE_NAME'),
            value=session.session_id,
            httponly=True,
            secure=False,
            samesite="Lax"
        )
        
        ip_info = get_ip_info(request)
        create_activity(session_id=session.session_id, user_id=user.id, activity_type=ActivityType.LOGIN, public_ip_address=ip_info.get('ip'), city=ip_info.get('city'), region=ip_info.get('region'), country=ip_info.get('country'), isp=ip_info.get('org'))
        
        return UserLoginResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


def logout(session_id: str, request: Request, response: Response) -> UserLogoutResponseSchema:
    try:
        session = get_session_by_session_id(session_id)
        # if session_id:
        #     delete_session_by_session_id(session_id)

        response.delete_cookie(getenv('SESSION_COOKIE_NAME'))
        
        ip_info = get_ip_info(request)
        create_activity(session_id=session_id, user_id=session.user_id, activity_type=ActivityType.LOGOUT, public_ip_address=ip_info.get('ip'), city=ip_info.get('city'), region=ip_info.get('region'), country=ip_info.get('country'), isp=ip_info.get('org'))

        return UserLogoutResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


def get_profile_data(session_id: str, request: Request) -> UserGetProfileDataResponseSchema:
    try:
        session = get_session_by_session_id(session_id)
        user = get_user_by_id(session.user_id)
        
        return UserGetProfileDataResponseSchema(
            status_code=status.HTTP_200_OK,
            profile_data=ProfileData(
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


def get_sessions(session_id: str) -> UserGetSessionsResponseSchema:
    try:
        session = get_session_by_session_id(session_id)
        
        sessions = get_sessions_by_user_id(session.user_id)
        
        return UserGetSessionsResponseSchema(
            status_code=status.HTTP_200_OK,
            sessions_data=[
                SessionData(
                    session_id=s.session_id,
                    user_id=s.user_id,
                    admin_id=s.admin_id,
                    is_admin=s.is_admin,
                    ip_address=s.ip_address,
                    device=s.device,
                    os=s.os,
                    browser=s.browser,
                    created_at=s.created_at.strftime("%B %d, %Y at %I:%M %p"),
                    expired_at=s.expired_at.strftime("%B %d, %Y at %I:%M %p")
                )
                for s in sessions
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


def get_activities(session_id: str) -> UserGetActivitiesResponseSchema:
    try:
        session = get_session_by_session_id(session_id)
        
        activities = get_activities_by_user_id(session.user_id)
        
        return UserGetActivitiesResponseSchema(
            status_code=status.HTTP_200_OK,
            activities_data=[
                ActivityData(
                    id=a.id,
                    session_id=a.session_id,
                    user_id=a.user_id,
                    activity_type=a.activity_type,
                    public_ip_address=a.public_ip_address,
                    city=a.city,
                    region=a.region,
                    country=a.country,
                    isp=a.isp,
                    timestamp=a.timestamp.strftime("%B %d, %Y at %I:%M %p"),
                )
                for a in activities
            ]
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
        ServiceFactory().get(service_type=ServiceType.MAIL_SERVICE).get(mail_type=MailType.VERIFY_EMAIL).send(recipient=user.email, provider=MProviderType.SES, verification_link=verification_link)
        # verify_email.send_verify_email_mail(user.email, verification_link)
        
        return UserSendVerifyEmailMailResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    
def send_reset_password_mail(email: EmailStr) -> UserSendResetPasswordMailResponseSchema:
    try:
        user = get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user_does_not_exists")
        
        reset_password_token = gen_access_token({'user_id': user.id}, timedelta(minutes=5))
        reset_password_link = f"http://{getenv('DOMAIN')}:{getenv('PORT')}/frontend-route-for-reset-password?token={reset_password_token}"
        ServiceFactory().get(service_type=ServiceType.MAIL_SERVICE).get(mail_type=MailType.RESET_PASSWORD).send(recipient=user.email, provider=MProviderType.SES, reset_password_link=reset_password_link)
        reset_password.send_reset_password_mail(user.email, reset_password_link)
        
        return UserSendResetPasswordMailResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
 
 
def enable_mfa(session_id: str) -> UserEnableMFAResponseSchema:
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
 
 
def disable_mfa(session_id: str, request: Request) -> UserDisableMFAResponseSchema:
    try:
        session = get_session_by_session_id(session_id)
        
        delete_mfa_secret_by_user_id(session.user_id)
        update_user_profile_data_by_id(session.user_id, {'is_mfa_enabled': False})
        
        ip_info = get_ip_info(request)
        create_activity(session_id=session_id, user_id=session.user_id, activity_type=ActivityType.MFA_DISABLED, public_ip_address=ip_info.get('ip'), city=ip_info.get('city'), region=ip_info.get('region'), country=ip_info.get('country'), isp=ip_info.get('org'))
        
        return UserDisableMFAResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
 
def verify_first_otp(req_body: UserVerifyFirstOTPRequestSchema, session_id: str, request: Request) -> UserVerifyFirstOTPResponseSchema:
    try:
        session = get_session_by_session_id(session_id)
        mfa_secret = get_mfa_secret_by_user_id(session.user_id)
        
        if not mfa_secret:
            raise HTTPException(status_code=400, detail="mfa_not_enabled_for_this_user")

        totp = pyotp.TOTP(mfa_secret.secret)
        
        if totp.verify(req_body.otp):
            update_user_profile_data_by_id(session.user_id, {'is_mfa_enabled': True})
            ip_info = get_ip_info(request)
            create_activity(session_id=session_id, user_id=session.user_id, activity_type=ActivityType.MFA_ENABLED, public_ip_address=ip_info.get('ip'), city=ip_info.get('city'), region=ip_info.get('region'), country=ip_info.get('country'), isp=ip_info.get('org'))
            return UserVerifyFirstOTPResponseSchema(status_code=status.HTTP_200_OK)
        
        raise HTTPException(status_code=400, detail="invalid_otp")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
 

def update_profile_data(req_body: UserUpdateProfileDataRequestSchema, session_id: str, request: Request) -> UserUpdateProfileDataResponseSchema:
    try:
        session = get_session_by_session_id(session_id)
        update_data: dict = {k: v for k, v in req_body.update_data.model_dump().items() if v is not None}
        update_user_profile_data_by_id(session.user_id, update_data)
        
        ip_info = get_ip_info(request)
        create_activity(session_id=session_id, user_id=session.user_id, activity_type=ActivityType.UPDATE_PROFILE, public_ip_address=ip_info.get('ip'), city=ip_info.get('city'), region=ip_info.get('region'), country=ip_info.get('country'), isp=ip_info.get('org'))
        return UserUpdateProfileDataResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
     
     
def update_password(req_body: UserUpdatePasswordRequestSchema, request: Request, token: Optional[str] = None, session_id: Optional[str] = None) -> UserUpdatePasswordResponseSchema:
    try:
        if session_id:
            session = get_session_by_session_id(session_id)
            user_id = session.user_id
            user = get_user_by_id(user_id)
            if not verify_password(req_body.curr_password, user.hashed_password):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="password_not_matched")
        elif token:
            payload = decode_access_token(token)
            user_id = payload.get('user_id')
            
        hashed_password = get_password_hash(req_body.new_password)
        update_user_password_by_id(user_id, {'hashed_password': hashed_password})
        
        ip_info = get_ip_info(request)
        create_activity(session_id=session_id, user_id=user_id, activity_type=ActivityType.PASSWORD_RESET, public_ip_address=ip_info.get('ip'), city=ip_info.get('city'), region=ip_info.get('region'), country=ip_info.get('country'), isp=ip_info.get('org'))
        
        current_time = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        account_settings_url = f"http://{getenv('DOMAIN')}:{getenv('PORT')}/api/v1/account/settings"
        ServiceFactory().get(service_type=ServiceType.MAIL_SERVICE).get(mail_type=MailType.PASSWORD_RESET).send(recipient=user.email, provider=MProviderType.SES, current_time=current_time, account_settings_url=account_settings_url)
        # password_reset.send_password_reset_mail(user.email, current_time, account_settings_url)
            
        return UserUpdatePasswordResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


def delete(session_id: str, request: Request) -> UserDeleteResponseSchema:
    try:
        session = get_session_by_session_id(session_id)
        delete_user_by_id(session.user_id)
        delete_session_by_session_id(session.session_id)
        
        ip_info = get_ip_info(request)
        create_activity(session_id=session_id, user_id=session.user_id, activity_type=ActivityType.ACCOUNT_DELETE, public_ip_address=ip_info.get('ip'), city=ip_info.get('city'), region=ip_info.get('region'), country=ip_info.get('country'), isp=ip_info.get('org'))
        
        return UserDeleteResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
async def send_verify_otp(session_id :str,phone_number: str) ->UserSendVerifyPhoneOtpResponseSchema:
    session = get_session_by_session_id(session_id)
    user = get_user_by_id(session.user_id)
    if user.is_phone_verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user_is_already_verified")
    
    otp = generate_otp()
    print(otp)
    message = f"Your OTP is: {otp}. Valid for 5 minutes."
    SMSSender.send_sms(SMSSender ,ProviderType, phone_number, message)
    otp_key = f"otp:{session_id}"
    await redis.set(otp_key, otp +","+ phone_number, ex=300)
    return UserSendVerifyPhoneOtpResponseSchema(status_code=status.HTTP_200_OK)


# send_verify_phoneNumber_OTP()
def generate_otp(length=6):
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

async def verify_otp(session_id : str , otp : str)->UserEnteredPhoneOtpResponseSchema:
   session = get_session_by_session_id(session_id)
   otp_key = f"otp:{session_id}"
   response  = str(await redis.get(otp_key))
   res_otp = response.split(",")[0]
   res_phone = response.split(",")[1] 

   if res_otp == otp:
      update_user_profile_data_by_id(session.user_id , {"phone":res_phone , "is_phone_verified":True})

      return UserEnteredPhoneOtpResponseSchema(status_code=status.HTTP_200_OK)
      
   else:
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP expired or not found")