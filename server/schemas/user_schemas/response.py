from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from ..base_schemas import BaseOfAllResponseSchemas, Token, UserData


class UserRegisterResponseSchema(BaseOfAllResponseSchemas):
    message: str = "user_registered_successfully"
    
class UserLoginResponseSchema(BaseOfAllResponseSchemas, Token):
    message: str = "user_logged_in_successfully"
    
class UserGetProfileResponseSchema(BaseOfAllResponseSchemas):
    profile_data: UserData
    
class UserUpdateProfileResponseSchema(BaseOfAllResponseSchemas):
    message: str = "user_s_profile_updated_successfully"
    
class UserUpdatePasswordResponseSchema(BaseOfAllResponseSchemas):
    message: str = "user_s_password_updated_successfully"
    
class UserDeleteResponseSchema(BaseOfAllResponseSchemas):
    message: str = "user_deleted_successfully"