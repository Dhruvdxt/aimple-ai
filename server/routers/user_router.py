from fastapi import APIRouter
from ..controllers import user_controller as user_con
from ..schemas.user_schemas.request import UserRegisterRequestSchema, UserLoginRequestSchema, UpdateUserByIdRequestSchema
from ..schemas.user_schemas.response import UserRegisterResponseSchema, UserLoginResponseSchema, GetUserByIdResponseSchema, UpdateUserByIdResponseSchema

router = APIRouter(prefix="/user", tags=['User'])


@router.post("/register", response_model=UserRegisterResponseSchema)
async def register(req: UserRegisterRequestSchema):
    return user_con.register(req)

@router.post("/login", response_model=UserLoginResponseSchema)
async def login(req: UserLoginRequestSchema):
    return user_con.login(req)

# @router.get("/", response_model=GetUserByIdResponseSchema)
# async def get_user_by_id():
#     return user_con.get_user_by_id()

# @router.put("/update", response_model=UpdateUserByIdResponseSchema)
# async def update_user_by_id(requereqst: UpdateUserByIdRequestSchema):
#     return user_con.update_user_by_id(req)

