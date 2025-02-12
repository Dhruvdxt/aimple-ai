from fastapi import HTTPException, Depends, Security, status, Request, Response
from typing import Optional
from datetime import datetime, timedelta
from os import getenv
from jose import JWTError, jwt
from ...config.db_config import redis
from .errors import cred_exp
from .hashing import verify_password
from ...repositories.admin_repository import get_admin_by_email
from ...repositories.session_repository import *
from ...repositories.user_repository import get_user_by_email


async def authenticate(email: str, password: str, is_admin: Optional[bool] = False):
    try:
        entity = get_user_by_email(email) if not is_admin else get_admin_by_email(email)
        if entity is None:
            await record_failed_attempt(email)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="email_not_registered"
            )
            
        if not verify_password(password, entity.hashed_password):
            await record_failed_attempt(email)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="incorrect_email_or_password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return entity
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    

def get_session_id(request: Request):
    try:
        session_id = request.cookies.get(getenv('SESSION_COOKIE_NAME'))

        if not session_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not_authenticated")
        
        session = get_session_by_session_id(session_id)

        if session.expired_at <= datetime.now():
            # delete_session_by_session_id(session_id)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="session_expired")

        return session_id
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def check_login_attempts(email: str):
    lock_key = f"lockout:{email}"
    fail_key = f"login_attempts:{email}"
    
    
    
    is_locked = await redis.get(lock_key)
    
    
    if is_locked:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="your_account_is_locked_due_to_multiple_failed_login_attempts.try_again_later."
        )
    
        
    failed_attempts = await redis.get(fail_key)

    
    if failed_attempts and int(failed_attempts) >= int(getenv('FAILED_ATTEMPT_LIMIT')):
        await redis.set(lock_key, "LOCKED", ex=int(getenv('BLOCK_DURATION')))
        await redis.delete(fail_key)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="too_many_failed_attempts.your_account_is_locked_for_2_hours."
        )
    


async def record_failed_attempt(email: str):
    fail_key = f"login_attempts:{email}"
    
    failed_attempts = await redis.get(fail_key)
    if failed_attempts:
        await redis.incr(fail_key)
    else:
        await redis.set(fail_key, 1, ex=getenv('ATTEMPT_RESET_TIME'))


async def delete_record(email: str):
    key = f"login_attempts:{email}"
    if await redis.exists(key):
        await redis.delete(key)


def gen_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(minutes=int(getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, getenv('SECRET_KEY'), algorithm=getenv('ALGORITHM'))
        return encoded_jwt
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, getenv('SECRET_KEY'), algorithms=[getenv('ALGORITHM')])
    except JWTError:
        raise cred_exp
        
    
# def decode_user_token(
#     security_scopes: SecurityScopes = SecurityScopes(),
#     token: str = Depends(user_oauth2_scheme),
# ) -> TokenData:
#     try:
#         payload = decode_access_token(token)
#         user_id = payload.get('user_id')
        
#         if user_id is None:
#             raise cred_exp
#         return TokenData(user_id=int(user_id))
#     except JWTError:
#         raise cred_exp
 
   
# def decode_admin_token(
#     security_scopes: SecurityScopes = SecurityScopes(),
#     token: str = Depends(admin_oauth2_scheme),
# ) -> TokenData:
#     try:
#         payload = decode_access_token(token)
#         admin_id = payload.get('admin_id')
        
#         if admin_id is None:
#             raise cred_exp
#         return TokenData(admin_id=int(admin_id))
#     except JWTError:
#         raise cred_exp