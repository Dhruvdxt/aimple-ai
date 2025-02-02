from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from ..controllers import admin_controller as admin_ctrl
from ..core.utils.auth import decode_admin_token
from ..schemas.admin_schemas.request import *
from ..schemas.admin_schemas.response import *
from ..schemas.base_schemas import TokenData


router = APIRouter(prefix="/admin", tags=['Admin'])
token_dependency = Annotated[TokenData, Depends(decode_admin_token)]


@router.post("/register", response_model=AdminRegisterResponseSchema)
async def register(req: AdminRegisterRequestSchema):
    return admin_ctrl.register(req)


@router.post("/login", response_model=AdminLoginResponseSchema)
async def login(req: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return admin_ctrl.login(req)


@router.get("/get_profile", response_model=AdminGetProfileResponseSchema)
async def get_profile(token: token_dependency):
    return admin_ctrl.get_profile(token)


@router.get("/get_dashboard_data", response_model=AdminGetDashboardDataResponseSchema)
async def get_dashboard_data(token: token_dependency):
    return admin_ctrl.get_dashboard_data(token)


@router.put("/update_profile", response_model=AdminUpdateProfileResponseSchema)
async def update_profile(req: AdminUpdateProfileRequestSchema, token: token_dependency):
    return admin_ctrl.update_profile(req, token)


@router.put("/update_password", response_model=AdminUpdatePasswordResponseSchema)
async def update_password(req: AdminUpdatePasswordRequestSchema, token: token_dependency):
    return admin_ctrl.update_password(req, token)


@router.delete("/delete", response_model=AdminDeleteResponseSchema)
async def delete(token: token_dependency):
    return admin_ctrl.delete(token)