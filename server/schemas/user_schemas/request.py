from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


# Base classess
class UserRegisterRequestSchema(BaseModel):
    email: EmailStr
    password: str
    
class UpdateData(BaseModel):
    full_name: Optional[str] = None
    
# Derived classess
class UserLoginRequestSchema(UserRegisterRequestSchema):
    pass
    
class UpdateUserByIdRequestSchema(BaseModel):
    update_data: UpdateData
    
# class UserRegisterRequestSchema(BaseModel):
#     email: str
#     password: str
    
    