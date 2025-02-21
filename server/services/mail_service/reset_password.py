import os
# from .index import MailService as ms
from .mailer import Mailer
from .mailer import ProviderType


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, "../../core/utils/templates/mail_templates/reset_password_template.html")


class ResetPassword():
    def __get_reset_password_mail_body(self, reset_password_link: str):
        with open(TEMPLATE_PATH, "r", encoding="utf-8") as file:
            template = file.read()
        return template.replace("{{reset_password_link}}", reset_password_link)

    def send(self, recipient: str, provider: ProviderType, reset_password_link: str):
        subject = "Action Required: Reset Your Aimple AI Password"
        body = ResetPassword.__get_reset_password_mail_body(self, reset_password_link)
        
        mailer = Mailer()
        mailer.send_mail(recipient, provider, {"Data": subject}, {"Html": {"Data": body}})
        return


# def get_reset_password_mail_body(reset_password_link: str):
#     with open(TEMPLATE_PATH, "r", encoding="utf-8") as file:
#         template = file.read()
#     return template.replace("{{reset_password_link}}", reset_password_link)


# def send_reset_password_mail(recipient: str, reset_password_link: str):
#     subject = "Action Required: Reset Your Aimple AI Password"
#     body = get_reset_password_mail_body(reset_password_link)
    
#     send_mail(recipient, {"Data": subject}, {"Html": {"Data": body}})
#     return
    