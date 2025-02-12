from fastapi import APIRouter, Depends, Request, Response
from typing import Annotated
from os import getenv
from ...config.fastapi_config import limiter
from ...controllers.v1.index import user_controller as user_ctrl
from ...core.utils.auth import get_session_id
from ...schemas.user_schemas.request import *
from ...schemas.user_schemas.response import *
from ...schemas.base_schemas import TokenData


router = APIRouter(prefix="/user", tags=['User'])
session_id_dependency = Annotated[TokenData, Depends(get_session_id)]


@router.post("/register", response_model=UserRegisterResponseSchema)
async def register(req_body: UserRegisterRequestSchema):
    return user_ctrl.register(req_body)


@router.post("/login", response_model=UserLoginResponseSchema)
@limiter.limit(f"{getenv('RATE_LIMIT')}/minute")
async def login(req_body: UserLoginRequestSchema, request: Request, response: Response):
    return await user_ctrl.login(req_body, request, response)


@router.get("/logout", response_model=UserLogoutResponseSchema)
async def logout(session_id: session_id_dependency, response: Response):
    return user_ctrl.logout(session_id, response)


@router.get("/get_profile_data", response_model=UserGetProfileDataResponseSchema)
async def get_profile_data(session_id: session_id_dependency):
    return user_ctrl.get_profile_data(session_id)


@router.get("/get_sessions", response_model=UserGetSessionsResponseSchema)
async def get_sessions(session_id: session_id_dependency):
    return user_ctrl.get_sessions(session_id)


@router.get("/get_activities", response_model=UserGetActivitiesResponseSchema)
async def get_activities(session_id: session_id_dependency):
    return user_ctrl.get_activities(session_id)


@router.get("/send_verify_email_mail", response_model=UserSendVerifyEmailMailResponseSchema)
async def send_verify_email_mail(session_id: session_id_dependency):
    return user_ctrl.send_verify_email_mail(session_id)


@router.post("/enable_mfa", response_model=UserEnableMFAResponseSchema)
async def enable_mfa(session_id: session_id_dependency):
    return user_ctrl.enable_mfa(session_id)


@router.post("/verify_first_otp", response_model=UserVerifyFirstOTPResponseSchema)
async def enable_mfa(req_body: UserVerifyFirstOTPRequestSchema, session_id: session_id_dependency):
    return user_ctrl.verify_first_otp(req_body, session_id)


@router.post("/disable_mfa", response_model=UserDisableMFAResponseSchema)
async def disable_mfa(session_id: session_id_dependency):
    return user_ctrl.disable_mfa(session_id)


@router.put("/update_profile_data", response_model=UserUpdateProfileDataResponseSchema)
async def update_profile_data(req_body: UserUpdateProfileDataRequestSchema, session_id: session_id_dependency):
    return user_ctrl.update_profile_data(req_body, session_id)


@router.put("/update_password", response_model=UserUpdatePasswordResponseSchema)
async def update_password(req_body: UserUpdatePasswordRequestSchema, session_id: session_id_dependency):
    return user_ctrl.update_password(req_body, session_id)


@router.delete("/delete", response_model=UserDeleteResponseSchema)
async def delete(session_id: session_id_dependency):
    return user_ctrl.delete(session_id)