from fastapi import APIRouter, Depends, Request, Response
from typing import Annotated
from ...config.fastapi_config import limiter
from ...controllers.v1.index import admin_controller as admin_ctrl
from ...core.utils.auth import get_session_id
from ...core.utils.func_tracer import func_tracer
from ...schemas.admin_schemas.request import *
from ...schemas.admin_schemas.response import *
from ...schemas.base_schemas import TokenData


router = APIRouter(prefix="/admin", tags=['Admin'])
session_id_dependency = Annotated[TokenData, Depends(get_session_id)]


@router.post("/register", response_model=AdminRegisterResponseSchema)
@func_tracer
async def register(req: AdminRegisterRequestSchema):
    return admin_ctrl.register(req)


@router.post("/login", response_model=AdminLoginResponseSchema)
@limiter.limit("3/minute")
@func_tracer
async def login(req_body: AdminLoginRequestSchema, request: Request, response: Response):
    return await admin_ctrl.login(req_body, request, response)


@router.get("/logout", response_model=AdminLogoutResponseSchema)
@func_tracer
async def logout(request: Request, response: Response):
    return admin_ctrl.logout(request, response)


@router.get("/get_users", response_model=AdminGetUsersResponseSchema)
@func_tracer
async def get_users(session_id: session_id_dependency):
    return admin_ctrl.get_users()


@router.get("/get_profile_data", response_model=AdminGetProfileDataResponseSchema)
@func_tracer
async def get_profile_data(session_id: session_id_dependency):
    return admin_ctrl.get_profile_data(session_id)


@router.get("/get_profile_data/{user_id}", response_model=AdminGetProfileDataResponseSchema)
@func_tracer
async def get_profile_data(session_id: session_id_dependency, user_id: int):
    return admin_ctrl.get_profile_data(session_id, user_id)


@router.get("/get_dashboard_data", response_model=AdminGetDashboardDataResponseSchema)
@func_tracer
async def get_dashboard_data(session_id: session_id_dependency):
    return admin_ctrl.get_dashboard_data(session_id)


@router.get("/get_sessions", response_model=AdminGetSessionsResponseSchema)
@func_tracer
async def get_sessions(session_id: session_id_dependency):
    return admin_ctrl.get_sessions(session_id)


@router.get("/get_activities", response_model=AdminGetActivitiesResponseSchema)
@func_tracer
async def get_activities(session_id: session_id_dependency):
    return admin_ctrl.get_activities(session_id)


@router.get("/get_settings", response_model=AdminGetSettingsResponseSchema)
@func_tracer
async def get_settings(session_id: session_id_dependency):
    return admin_ctrl.get_settings(session_id)


@router.put("/update_profile_data", response_model=AdminUpdateProfileDataResponseSchema)
@func_tracer
async def update_profile_data(req_body: AdminUpdateProfileDataRequestSchema, session_id: session_id_dependency, request: Request):
    return admin_ctrl.update_profile_data(req_body, session_id, request)


@router.put("/update_profile_data/{user_id}", response_model=AdminUpdateProfileDataResponseSchema)
@func_tracer
async def update_profile_data(req_body: AdminUpdateProfileDataRequestSchema, session_id: session_id_dependency, request: Request, user_id: int):
    return admin_ctrl.update_profile_data(req_body, session_id, request, user_id)


@router.put("/update_password", response_model=AdminUpdatePasswordResponseSchema)
@func_tracer
async def update_password(req_body: AdminUpdatePasswordRequestSchema, session_id: session_id_dependency, request: Request):
    return admin_ctrl.update_password(req_body, session_id, request)


@router.put("/update_password/{user_id}", response_model=AdminUpdatePasswordResponseSchema)
@func_tracer
async def update_password(req_body: AdminUpdatePasswordRequestSchema, session_id: session_id_dependency, request: Request, user_id: int):
    return admin_ctrl.update_password(req_body, session_id, request, user_id)


@router.put("/update_settings", response_model=AdminUpdateSettingsResponseSchema)
@func_tracer
async def update_settings(req_body: AdminUpdateSettingsRequestSchema, session_id: session_id_dependency):
    return admin_ctrl.update_settings(req_body, session_id)


@router.put("/enable_or_disable", response_model=AdminEnableOrDisableResponseSchema)
@func_tracer
async def enable_or_disable(req_body: AdminEnableOrDisableRequestSchema, session_id: session_id_dependency, request: Request):
    return admin_ctrl.enable_or_disable(req_body, session_id, request)


@router.delete("/delete", response_model=AdminDeleteResponseSchema)
@func_tracer
async def delete(session_id: session_id_dependency, request: Request):
    return admin_ctrl.delete(session_id, request)