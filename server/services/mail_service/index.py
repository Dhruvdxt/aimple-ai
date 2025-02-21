from enum import Enum
from .mailer import Mailer, ProviderType
from .password_reset import PasswordReset
from .reset_password import ResetPassword
from .verify_email import VerifyEmail


class MailType(str, Enum):
    WELCOME = "WELCOME"
    VERIFY_EMAIL = "VERIFY_EMAIL"
    RESET_PASSWORD = "RESET_PASSWORD"
    PASSWORD_RESET = "PASSWORD_RESET"
    
map: dict[str, any] = {
    # "WELCOME": VerifyEmail(),
    "VERIFY_EMAIL": VerifyEmail(),
    "RESET_PASSWORD": ResetPassword(),
    "PASSWORD_RESET": PasswordReset()
}

class MailService():
    def get_mailer(self):
        return Mailer()
    
    def get(self, mail_type: MailType):
        return map[mail_type]