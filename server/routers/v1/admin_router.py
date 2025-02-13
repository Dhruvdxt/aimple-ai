from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from ...config.fastapi_config import limiter
from ...controllers.v1.index import admin_controller as admin_ctrl
from ...core.utils.auth import get_session_id
from ...schemas.admin_schemas.request import *
from ...schemas.admin_schemas.response import *
from ...schemas.base_schemas import TokenData


router = APIRouter(prefix="/admin", tags=['Admin'])
session_id_dependency = Annotated[TokenData, Depends(get_session_id)]


@router.post("/register", response_model=AdminRegisterResponseSchema)
async def register(req: AdminRegisterRequestSchema):
    return admin_ctrl.register(req)


@router.post("/login", response_model=AdminLoginResponseSchema)
@limiter.limit("3/minute")
async def login(req_body: AdminLoginRequestSchema, request: Request, response: Response):
    return await admin_ctrl.login(req_body, request, response)


@router.get("/logout", response_model=AdminLogoutResponseSchema)
async def logout(request: Request, response: Response):
    return admin_ctrl.logout(request, response)


@router.get("/get_users", response_model=AdminGetUsersResponseSchema)
async def get_users(session_id: session_id_dependency):
    return admin_ctrl.get_users()


@router.get("/get_profile_data", response_model=AdminGetProfileDataResponseSchema)
async def get_profile_data(session_id: session_id_dependency):
    return admin_ctrl.get_profile_data(session_id)


@router.get("/get_profile_data/{user_id}", response_model=AdminGetProfileDataResponseSchema)
async def get_profile_data(session_id: session_id_dependency, user_id: int):
    return admin_ctrl.get_profile_data(session_id, user_id)


@router.get("/get_dashboard_data", response_model=AdminGetDashboardDataResponseSchema)
async def get_dashboard_data(session_id: session_id_dependency):
    return admin_ctrl.get_dashboard_data()


@router.get("/get_sessions", response_model=AdminGetSessionsResponseSchema)
async def get_sessions(session_id: session_id_dependency):
    return admin_ctrl.get_sessions()


@router.get("/get_activities", response_model=AdminGetActivitiesResponseSchema)
async def get_activities(session_id: session_id_dependency):
    return admin_ctrl.get_activities()


@router.put("/update_profile_data", response_model=AdminUpdateProfileDataResponseSchema)
async def update_profile_data(req_body: AdminUpdateProfileDataRequestSchema, session_id: session_id_dependency):
    return admin_ctrl.update_profile_data(req_body, session_id)


@router.put("/update_profile_data/{user_id}", response_model=AdminUpdateProfileDataResponseSchema)
async def update_profile_data(req_body: AdminUpdateProfileDataRequestSchema, session_id: session_id_dependency, user_id: int):
    return admin_ctrl.update_profile_data(req_body, session_id, user_id)


@router.put("/update_password", response_model=AdminUpdatePasswordResponseSchema)
async def update_password(req_body: AdminUpdatePasswordRequestSchema, session_id: session_id_dependency):
    return admin_ctrl.update_password(req_body, session_id)


@router.put("/update_password/{user_id}", response_model=AdminUpdatePasswordResponseSchema)
async def update_password(req_body: AdminUpdatePasswordRequestSchema, session_id: session_id_dependency, user_id: int):
    return admin_ctrl.update_password(req_body, session_id, user_id)


@router.put("/enable_or_disable", response_model=AdminEnableOrDisableResponseSchema)
async def enable_or_disable(req_body: AdminEnableOrDisableRequestSchema, session_id: session_id_dependency):
    return admin_ctrl.enable_or_disable(req_body, session_id)


@router.delete("/delete", response_model=AdminDeleteResponseSchema)
async def delete(session_id: session_id_dependency):
    return admin_ctrl.delete(session_id)