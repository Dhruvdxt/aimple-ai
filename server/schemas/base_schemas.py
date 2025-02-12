from pydantic import BaseModel, EmailStr
from typing import Optional
from ..models.activity_model import ActivityType

class BaseOfAllResponseSchemas(BaseModel):
    status_code: int
    
class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    
class TokenData(BaseModel):
    user_id: Optional[int] = None
    admin_id: Optional[int] = None
    
class UpdateData(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    country: Optional[str] = None
    
class UserData(UpdateData):
    id: int
    email: EmailStr
    disabled: bool = False
    verified: bool = False
    is_mfa_enabled: bool = False
    
class AdminData(UserData):
    pass

class DashboardData(BaseModel):
    total_users: int
    active_users: int
    inactive_users: int
    verified_users: int
    unverified_users: int
    total_admins: int
    
class VerifyEmailResponseSchema(BaseOfAllResponseSchemas):
    message: str = "email_verified_successfully"
    
class SessionData(BaseModel):
    session_id: str
    user_id: int
    admin_id: Optional[int]
    is_admin: Optional[bool]
    ip_address: str
    device: Optional[str]
    created_at: str
    expired_at: str
    
class ActivityData(BaseModel):
    id: int
    session_id: Optional[str]
    user_id: Optional[int]
    activity_type: ActivityType
    timestamp: str
    