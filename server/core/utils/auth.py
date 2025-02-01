from fastapi import HTTPException, Depends, Security, status
from typing import Optional
from datetime import datetime, timedelta
from os import getenv
from jose import JWTError, jwt
from .hashing import verify_password
from ...repositories.admin_repository import get_admin_by_email
from ...repositories.user_repository import get_user_by_email

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

# def get_current_user(
#     # db: Session = Depends(SessionLocal),
#     security_scopes: SecurityScopes = SecurityScopes(),
#     token: str = Depends(oauth2_scheme),
#     user_type: UserType = UserType.USER
# ):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
#         token_user_type: str = payload.get("user_type")
#         if email is None or token_user_type != user_type:
#             raise credentials_exception
#         token_data = TokenData(email=email, user_type=token_user_type)
#     except JWTError:
#         raise credentials_exception
    
#     user = get_user(db, token_data.email, user_type)
#     if user is None:
#         raise credentials_exception
#     return user