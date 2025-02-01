from fastapi import HTTPException, status
from ..config.db_config import db
from ..core.utils.auth import authenticate, create_access_token
from ..core.utils.hashing import get_password_hash, verify_password
from ..repositories.user_repository import get_user_by_email, create_user
from ..schemas.user_schemas.request import UserRegisterRequestSchema, UserLoginRequestSchema
from ..schemas.user_schemas.response import UserRegisterResponseSchema, UserLoginResponseSchema, Token

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
    
def login(req: UserLoginRequestSchema) -> UserLoginResponseSchema:
    try:
        user = authenticate(req.email, req.password)
        
        access_token = create_access_token(data={"sub": user.email})
        
        return UserLoginResponseSchema(status_code=status.HTTP_200_OK, token=Token(access_token=access_token))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        
