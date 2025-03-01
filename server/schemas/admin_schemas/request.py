from ..user_schemas.request import *
from ..base_schemas import Settings


class AdminRegisterRequestSchema(UserRegisterRequestSchema):
    pass

class AdminLoginRequestSchema(UserLoginRequestSchema):
    pass
    
class AdminUpdateProfileDataRequestSchema(UserUpdateProfileDataRequestSchema):
    pass
    
class AdminUpdatePasswordRequestSchema(BaseModel):
    curr_password: Optional[str] = None
    new_password: str
    
class AdminUpdateSettingsRequestSchema(BaseModel):
    update_data: Settings

class AdminEnableOrDisableRequestSchema(BaseModel):
    user_id: int
    