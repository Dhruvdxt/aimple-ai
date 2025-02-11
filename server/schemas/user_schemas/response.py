from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from ..base_schemas import BaseOfAllResponseSchemas, Token, UserData


class UserRegisterResponseSchema(BaseOfAllResponseSchemas):
    message: str = "user_registered_successfully"
    
class UserLoginResponseSchema(BaseOfAllResponseSchemas):
    message: str = "user_logged_in_successfully"
    
class UserLogoutResponseSchema(BaseOfAllResponseSchemas):
    message: str = "user_logged_out_successfully"
    
class UserGetProfileDataResponseSchema(BaseOfAllResponseSchemas):
    profile_data: UserData
    
class UserSendVerifyEmailMailResponseSchema(BaseOfAllResponseSchemas):
    message: str = "verification_mail_has_been_sent_successfully"
    
class UserEnableMFAResponseSchema(BaseOfAllResponseSchemas):
    message: str = "scan_qr_code_&_enter_otp"
    otp_uri: str
    
class UserVerifyFirstOTPResponseSchema(BaseOfAllResponseSchemas):
    message: str = "otp_verified_successfully"
    
class UserDisableMFAResponseSchema(BaseOfAllResponseSchemas):
    message: str = "mfa_disabled_successfully"
    
class UserUpdateProfileDataResponseSchema(BaseOfAllResponseSchemas):
    message: str = "user_s_profile_updated_successfully"
    
class UserUpdatePasswordResponseSchema(BaseOfAllResponseSchemas):
    message: str = "user_s_password_updated_successfully"
    
class UserDeleteResponseSchema(BaseOfAllResponseSchemas):
    message: str = "user_deleted_successfully"