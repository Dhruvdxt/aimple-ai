from ..user_schemas.request import *


class AdminRegisterRequestSchema(UserRegisterRequestSchema):
    pass

class AdminLoginRequestSchema(UserLoginRequestSchema):
    pass
    
class AdminUpdateProfileDataRequestSchema(UserUpdateProfileDataRequestSchema):
    pass
    
class AdminUpdatePasswordRequestSchema(BaseModel):
    curr_password: Optional[str] = None
    new_password: str

class AdminEnableOrDisableRequestSchema(BaseModel):
    user_id: int
    