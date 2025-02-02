from pydantic import BaseModel, EmailStr, ConfigDict
from ..base_schemas import UpdateData


class UserRegisterRequestSchema(BaseModel):
    email: EmailStr
    password: str
    
class UserUpdateProfileRequestSchema(BaseModel):
    update_data: UpdateData
    
class UserUpdatePasswordRequestSchema(BaseModel):
    curr_password: str
    new_password: str
    