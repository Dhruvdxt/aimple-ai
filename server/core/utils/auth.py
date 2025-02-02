from fastapi import HTTPException, Depends, Security, status
from fastapi.security import SecurityScopes
from typing import Optional
from datetime import datetime, timedelta
from os import getenv
from jose import JWTError, jwt
from ...config.fastapi_config import user_oauth2_scheme, admin_oauth2_scheme
from .errors import cred_exp
from .hashing import verify_password
from ...repositories.admin_repository import get_admin_by_email
from ...repositories.user_repository import get_user_by_email
from ...schemas.base_schemas import TokenData

def authenticate(email: str, password: str, isAdmin: Optional[bool] = False):
    try:
        entity = get_user_by_email(email) if not isAdmin else get_admin_by_email(email)
        if entity is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="email_not_registered"
            )
            
        if not verify_password(password, entity.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="incorrect_email_or_password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return entity
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=int(getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, getenv('SECRET_KEY'), algorithm=getenv('ALGORITHM'))
        return encoded_jwt
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
def decode_user_token(
    security_scopes: SecurityScopes = SecurityScopes(),
    token: str = Depends(user_oauth2_scheme),
) -> TokenData:
    try:
        payload = jwt.decode(token, getenv('SECRET_KEY'), algorithms=[getenv('ALGORITHM')])
        user_id = payload.get('user_id')
        
        if user_id is None:
            raise cred_exp
        return TokenData(user_id=int(user_id))
    except JWTError:
        raise cred_exp
    
def decode_admin_token(
    security_scopes: SecurityScopes = SecurityScopes(),
    token: str = Depends(admin_oauth2_scheme),
) -> TokenData:
    try:
        payload = jwt.decode(token, getenv('SECRET_KEY'), algorithms=[getenv('ALGORITHM')])
        admin_id = payload.get('admin_id')
        
        if admin_id is None:
            raise cred_exp
        return TokenData(admin_id=int(admin_id))
    except JWTError:
        raise cred_exp