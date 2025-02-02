from ..base_schemas import BaseOfAllResponseSchemas, Token, AdminData, DashboardData


class AdminRegisterResponseSchema(BaseOfAllResponseSchemas):
    message: str = "admin_registered_successfully"
    
class AdminLoginResponseSchema(BaseOfAllResponseSchemas, Token):
    message: str = "admin_logged_in_successfully"
    
class AdminGetProfileResponseSchema(BaseOfAllResponseSchemas):
    profile_data: AdminData
    
class AdminGetDashboardDataResponseSchema(BaseOfAllResponseSchemas):
    dashboard_data: DashboardData
    
class AdminUpdateProfileResponseSchema(BaseOfAllResponseSchemas):
    message: str = "admin_s_profile_updated_successfully"
    
class AdminUpdatePasswordResponseSchema(BaseOfAllResponseSchemas):
    message: str = "admin_s_password_updated_successfully"
    
class AdminDeleteResponseSchema(BaseOfAllResponseSchemas):
    message: str = "admin_deleted_successfully"