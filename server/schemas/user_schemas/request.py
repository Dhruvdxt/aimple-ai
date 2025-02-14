from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from ..base_schemas import UpdateData


class UserRegisterRequestSchema(BaseModel):
    email: EmailStr
    password: str

class UserLoginRequestSchema(UserRegisterRequestSchema):
    otp: Optional[int] = None
    
class UserVerifyFirstOTPRequestSchema(BaseModel):
    otp: int
    
class UserUpdateProfileDataRequestSchema(BaseModel):
    update_data: UpdateData
    
class UserUpdatePasswordRequestSchema(BaseModel):
    curr_password: Optional[str] = None
    new_password: str
    