from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from ..controllers import user_controller as user_ctrl
from ..core.utils.auth import decode_user_token
from ..schemas.user_schemas.request import *
from ..schemas.user_schemas.response import *
from ..schemas.base_schemas import TokenData


router = APIRouter(prefix="/user", tags=['User'])
token_dependency = Annotated[TokenData, Depends(decode_user_token)]


@router.post("/register", response_model=UserRegisterResponseSchema)
async def register(req: UserRegisterRequestSchema):
    return user_ctrl.register(req)


@router.post("/login", response_model=UserLoginResponseSchema)
async def login(req: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return user_ctrl.login(req)


@router.get("/get_profile_data", response_model=UserGetProfileDataResponseSchema)
async def get_profile_data(token: token_dependency):
    return user_ctrl.get_profile_data(token)


@router.put("/update_profile_data", response_model=UserUpdateProfileDataResponseSchema)
async def update_profile_data(req: UserUpdateProfileDataRequestSchema, token: token_dependency):
    return user_ctrl.update_profile_data(req, token)


@router.put("/update_password", response_model=UserUpdatePasswordResponseSchema)
async def update_password(req: UserUpdatePasswordRequestSchema, token: token_dependency):
    return user_ctrl.update_password(req, token)


@router.delete("/delete", response_model=UserDeleteResponseSchema)
async def delete(token: token_dependency):
    return user_ctrl.delete(token)