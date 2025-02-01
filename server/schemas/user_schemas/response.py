from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


# Base classess
class BaseOfAllSchemas(BaseModel):
    status_code: int
    
class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    
class User(BaseModel):
    email: EmailStr
    disabled: bool = False
    full_name: Optional[str] = None


# Derived classess
class UserRegisterResponseSchema(BaseOfAllSchemas):
    messege: str = "user_registered_successfully"
    
class UserLoginResponseSchema(BaseOfAllSchemas):
    messege: str = "user_logged_in_successfully"
    token: Token
    
class GetUserByIdResponseSchema(BaseOfAllSchemas):
    user: User
    
class UpdateUserByIdResponseSchema(BaseOfAllSchemas):
    messege: str = "user_updated_successfully"
    