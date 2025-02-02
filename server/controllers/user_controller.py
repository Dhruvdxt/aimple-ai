from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..core.utils.auth import authenticate, create_access_token
from ..core.utils.hashing import get_password_hash, verify_password
from ..repositories.user_repository import *
from ..schemas.user_schemas.request import *
from ..schemas.user_schemas.response import *
from ..schemas.base_schemas import TokenData, UserData

def register(req: UserRegisterRequestSchema) -> UserRegisterResponseSchema:
    try:
        if get_user_by_email(req.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="email_already_registered"
            )
        
        hashed_password = get_password_hash(req.password)
        
        create_user(req.email, hashed_password);
        
        return UserRegisterResponseSchema(status_code=201)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


def login(req: OAuth2PasswordRequestForm) -> UserLoginResponseSchema:
    try:
        user = authenticate(req.username, req.password)
        
        access_token = create_access_token(data={"user_id": user.id})
        
        return UserLoginResponseSchema(status_code=status.HTTP_200_OK, access_token=access_token)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


def get_profile_data(token: TokenData) -> UserGetProfileDataResponseSchema:
    try:
        user = get_user_by_id(token.user_id)
        return UserGetProfileDataResponseSchema(
            status_code=status.HTTP_200_OK,
            profile_data=UserData(
                email=user.email,
                full_name=user.full_name,
                phone=user.phone, 
                address=user.address,
                country=user.country,
                disabled=user.disabled
            )
        )
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
            
        return UserUpdatePasswordResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    

def delete(token: TokenData) -> UserDeleteResponseSchema:
    try:
        delete_user_by_id(token.user_id)
        return UserDeleteResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))