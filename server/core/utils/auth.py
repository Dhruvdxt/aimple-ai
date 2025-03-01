from fastapi import HTTPException, Depends, Security, status, Request, Response
from typing import Optional
from datetime import datetime, timedelta
from os import getenv
from jose import JWTError, jwt
from ...config.db_config import redis
from .errors import cred_exp
from .hashing import verify_password
from .settings import Settings
from ...repositories.admin_repository import get_admin_by_email
from ...repositories.session_repository import *
from ...repositories.user_repository import get_user_by_email


async def authenticate(email: str, password: str, is_admin: Optional[bool] = False):
    try:
        entity = get_user_by_email(email) if not is_admin else get_admin_by_email(email)
        if entity is None:
            # await record_failed_attempt(email_or_phone=email)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="email_not_registered"
            )
            
        if not verify_password(password, entity.hashed_password):
            await record_failed_attempt(email_or_phone=email)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="incorrect_email_or_password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return entity
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def verify(phone_number: str, otp: int) -> bool:
    try:
        otp_key = f"otp_for_{phone_number}_is:"
        our_otp = await redis.get(otp_key)

        if not our_otp:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="otp_expired")

        user_otp = str(otp)

        if our_otp != user_otp:
            await record_failed_attempt(email_or_phone=phone_number)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="incorrect_otp")
        
        return True
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


async def check_login_attempts(email_or_phone: str):
    lock_key = f"lockout:{email_or_phone}"
    fail_key = f"login_attempts:{email_or_phone}"
    
    is_locked = await redis.get(lock_key)
    
    if is_locked:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="your_account_is_locked_due_to_multiple_failed_login_attempts.try_again_later."
        )
        
    failed_attempts = await redis.get(fail_key)
    
    if failed_attempts and int(failed_attempts) >= Settings.FAILED_ATTEMPT_LIMIT:
        await redis.set(lock_key, "LOCKED", ex=Settings.BLOCK_DURATION)
        await redis.delete(fail_key)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="too_many_failed_attempts.your_account_is_locked_for_2_hours."
        )
    

async def record_failed_attempt(email_or_phone: str):
    fail_key = f"login_attempts:{email_or_phone}"
    
    failed_attempts = await redis.get(fail_key)
    if failed_attempts:
        await redis.incr(fail_key)
    else:
        await redis.set(fail_key, 1, ex=Settings.ATTEMPT_RESET_TIME)


async def delete_record(email_or_phone: str):
    key = f"login_attempts:{email_or_phone}"
    if await redis.exists(key):
        await redis.delete(key)


def gen_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
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