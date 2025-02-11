from ..user_schemas.request import *


class AdminRegisterRequestSchema(UserRegisterRequestSchema):
    pass
    
class AdminUpdateProfileDataRequestSchema(UserUpdateProfileDataRequestSchema):
    pass
    
class AdminUpdatePasswordRequestSchema(UserUpdatePasswordRequestSchema):
    pass

class AdminUpdateUserPasswordRequestSchema(BaseModel):
    user_id: int
    new_password: str

class AdminEnableOrDisableRequestSchema(BaseModel):
    user_id: int
    