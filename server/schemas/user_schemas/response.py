from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from ..base_schemas import *


class UserRegisterResponseSchema(BaseOfAllResponseSchemas):
    message: str = "user_registered_successfully"
    
class UserLoginResponseSchema(BaseOfAllResponseSchemas):
    message: str = "user_logged_in_successfully"
    
class UserLogoutResponseSchema(BaseOfAllResponseSchemas):
    message: str = "user_logged_out_successfully"
    
class UserGetProfileDataResponseSchema(BaseOfAllResponseSchemas):
    profile_data: ProfileData
    
class UserGetSessionsResponseSchema(BaseOfAllResponseSchemas):
    sessions_data: list[SessionData]
    
class UserGetActivitiesResponseSchema(BaseOfAllResponseSchemas):
    activities_data: list[ActivityData]
    
class UserSendVerifyEmailMailResponseSchema(BaseOfAllResponseSchemas):
    message: str = "verification_mail_has_been_sent_successfully"
    
class UserSendResetPasswordMailResponseSchema(BaseOfAllResponseSchemas):
    message: str = "reset_password_mail_has_been_sent_successfully"
    
class UserEnableMFAResponseSchema(BaseOfAllResponseSchemas):
    message: str = "scan_qr_code_&_enter_otp"
    otp_uri: str
    
class UserDisableMFAResponseSchema(BaseOfAllResponseSchemas):
    message: str = "mfa_disabled_successfully"
    
class UserVerifyFirstOTPResponseSchema(BaseOfAllResponseSchemas):
    message: str = "otp_verified_successfully"
    
class UserUpdateProfileDataResponseSchema(BaseOfAllResponseSchemas):
    message: str = "user_s_profile_updated_successfully"
    
class UserUpdatePasswordResponseSchema(BaseOfAllResponseSchemas):
    message: str = "user_s_password_updated_successfully"
    
class UserDeleteResponseSchema(BaseOfAllResponseSchemas):
    message: str = "user_deleted_successfully"