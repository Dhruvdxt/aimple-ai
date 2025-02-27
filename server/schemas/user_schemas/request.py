from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from ..base_schemas import UpdateData


class UserRegisterRequestSchema(BaseModel):
    email: EmailStr
    password: str

class UserLoginRequestSchema(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    phone_number: Optional[str] = None
    phone_otp: Optional[int] = None
    mfa_otp: Optional[int] = None
    
class UserVerifyFirstOTPRequestSchema(BaseModel):
    otp: int
    
class UserSendOtpRequestSchema(BaseModel):
    phone_number: str
    
class UserVerifyOtpRequestSchema(UserSendOtpRequestSchema):
    otp: int
    
class UserUpdateProfileDataRequestSchema(BaseModel):
    update_data: UpdateData
    
class UserUpdatePasswordRequestSchema(BaseModel):
    curr_password: Optional[str] = None
    new_password: str
    