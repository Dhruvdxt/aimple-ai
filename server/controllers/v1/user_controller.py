from fastapi import HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from os import getenv
from ...core.utils.auth import *
from ...core.utils.hashing import get_password_hash, verify_password
from ...repositories.activity_repository import *
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


def login(req: OAuth2PasswordRequestForm) -> UserLoginResponseSchema:
    try:
        user = authenticate(req.username, req.password)
        
        access_token = gen_access_token({"user_id": user.id})
        
        return UserLoginResponseSchema(status_code=status.HTTP_200_OK, access_token=access_token)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


def get_profile_data(token: TokenData) -> UserGetProfileDataResponseSchema:
    try:
        user = get_user_by_id(token.user_id)
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
                verified=user.verified
            )
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


def send_verify_email_mail(token: TokenData) -> UserSendVerifyEmailMailResponseSchema:
    try:
        user = get_user_by_id(token.user_id)
        if user.verified:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user_is_already_verified")
        
        verification_token = gen_access_token({'user_id': user.id}, timedelta(minutes=5))
        verification_link = f"http://{getenv('DOMAIN')}:{getenv('PORT')}/api/v2/verify_email?token={verification_token}"
        verify_email.send_verify_email_mail(user.email, verification_link)
        
        return UserSendVerifyEmailMailResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
 

def update_profile_data(req: UserUpdateProfileDataRequestSchema, token: TokenData) -> UserUpdateProfileDataResponseSchema:
    try:
        update_data: dict = {k: v for k, v in req.update_data.model_dump().items() if v is not None}
        update_user_profile_data_by_id(token.user_id, update_data)
        return UserUpdateProfileDataResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
     
     
def update_password(req: UserUpdatePasswordRequestSchema, token: TokenData) -> UserUpdatePasswordResponseSchema:
    try:
        user = get_user_by_id(token.user_id)
        if not verify_password(req.curr_password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="password_not_matched")
        
        hashed_password = get_password_hash(req.new_password)
        update_user_password_by_id(token.user_id, {'hashed_password': hashed_password})
        current_time = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        account_settings_url = f"http://{getenv('DOMAIN')}:{getenv('PORT')}/api/v1/account/settings"
        
        password_reset.send_password_reset_mail(user.email, current_time, account_settings_url)
            
        return UserUpdatePasswordResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    

def delete(token: TokenData) -> UserDeleteResponseSchema:
    try:
        delete_user_by_id(token.user_id)
        return UserDeleteResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))