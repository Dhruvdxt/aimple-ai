from ..base_schemas import BaseOfAllResponseSchemas, Token, AdminData, DashboardData


class AdminRegisterResponseSchema(BaseOfAllResponseSchemas):
    message: str = "admin_registered_successfully"
    
class AdminLoginResponseSchema(BaseOfAllResponseSchemas):
    message: str = "admin_logged_in_successfully"
    
class AdminLogoutResponseSchema(BaseOfAllResponseSchemas):
    message: str = "admin_logged_out_successfully"
    
class AdminGetProfileDataResponseSchema(BaseOfAllResponseSchemas):
    profile_data: AdminData
    
class AdminGetDashboardDataResponseSchema(BaseOfAllResponseSchemas):
    dashboard_data: DashboardData
    
class AdminUpdateProfileDataResponseSchema(BaseOfAllResponseSchemas):
    message: str = "admin_s_profile_updated_successfully"
    
class AdminUpdatePasswordResponseSchema(BaseOfAllResponseSchemas):
    message: str = "admin_s_password_updated_successfully"
    
class AdminUpdateUserPasswordResponseSchema(BaseOfAllResponseSchemas):
    message: str = "user_s_password_updated_successfully"
    
class AdminEnableOrDisableResponseSchema(BaseOfAllResponseSchemas):
    message: str = "user_enabled_or_disabled_successfully"
    
class AdminDeleteResponseSchema(BaseOfAllResponseSchemas):
    message: str = "admin_deleted_successfully"