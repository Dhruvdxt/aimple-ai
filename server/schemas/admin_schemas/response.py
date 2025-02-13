from ..user_schemas.response import *
from ..base_schemas import *


class AdminRegisterResponseSchema(BaseOfAllResponseSchemas):
    message: str = "admin_registered_successfully"
    
class AdminLoginResponseSchema(BaseOfAllResponseSchemas):
    message: str = "admin_logged_in_successfully"
    
class AdminLogoutResponseSchema(BaseOfAllResponseSchemas):
    message: str = "admin_logged_out_successfully"
    
class AdminGetUsersResponseSchema(BaseOfAllResponseSchemas):
    users_data: list[UserData]
    
class AdminGetProfileDataResponseSchema(UserGetProfileDataResponseSchema):
    pass

class AdminGetDashboardDataResponseSchema(BaseOfAllResponseSchemas):
    dashboard_data: DashboardData
    
class AdminGetSessionsResponseSchema(UserGetSessionsResponseSchema):
    pass

class AdminGetActivitiesResponseSchema(UserGetActivitiesResponseSchema):
    pass

class AdminUpdateProfileDataResponseSchema(BaseOfAllResponseSchemas):
    message: str = "profile_updated_successfully"
    
class AdminUpdatePasswordResponseSchema(BaseOfAllResponseSchemas):
    message: str = "password_updated_successfully"
    
class AdminEnableOrDisableResponseSchema(BaseOfAllResponseSchemas):
    message: str = "user_enabled_or_disabled_successfully"
    
class AdminDeleteResponseSchema(BaseOfAllResponseSchemas):
    message: str = "admin_deleted_successfully"