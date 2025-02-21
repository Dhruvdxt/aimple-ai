import os
# from .index import MailService as ms
from .mailer import Mailer
from .mailer import ProviderType


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, "../../core/utils/templates/mail_templates/password_reset_template.html")


class PasswordReset():
    def __get_password_reset_mail_body(self, current_time: str, account_settings_url: str):
        with open(TEMPLATE_PATH, "r", encoding="utf-8") as file:
            template = file.read()
            
        return template.replace("{{current_time}}", current_time).replace("{{account_settings_url}}", account_settings_url)

    def send(self, recipient: str, provider: ProviderType, current_time: str, account_settings_url: str):
        subject = "Security Alert: Password Modified"
        body = PasswordReset.__get_password_reset_mail_body(self, current_time, account_settings_url)
        
        mailer = Mailer()
        mailer.send_mail(recipient, provider, {"Data": subject}, {"Html": {"Data": body}})
        return
    
    

# def get_password_reset_mail_body(current_time: str, account_settings_url: str):
#     with open(TEMPLATE_PATH, "r", encoding="utf-8") as file:
#         template = file.read()
        
#     return template.replace("{{current_time}}", current_time).replace("{{account_settings_url}}", account_settings_url)
#     # return template.format(current_time=current_time, account_settings_url=account_settings_url)


# def send_password_reset_mail(recipient: str, current_time: str, account_settings_url: str):
#     subject = "Security Alert: Password Modified"
#     body = get_password_reset_mail_body(current_time, account_settings_url)
    
#     send_mail(recipient, {"Data": subject}, {"Html": {"Data": body}})
#     return
    