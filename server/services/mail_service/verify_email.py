import os
# from .index import MailService as ms
from .mailer import Mailer
from .mailer import ProviderType


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, "../../core/utils/templates/mail_templates/verify_email_template.html")


class VerifyEmail():
    def __get_verify_email_mail_body(self, verification_link: str):
        with open(TEMPLATE_PATH, "r", encoding="utf-8") as file:
            template = file.read()
        return template.replace("{{verification_link}}", verification_link)

    def send(self, recipient: str, provider: ProviderType, verification_link: str):
        subject = "Action Required: Verify Your Email for Aimple AI"
        body = VerifyEmail.__get_verify_email_mail_body(self, verification_link)
        
        mailer = Mailer()
        mailer.send_mail(recipient, provider, {"Data": subject}, {"Html": {"Data": body}})
        return