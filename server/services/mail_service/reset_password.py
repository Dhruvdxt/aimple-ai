import os
from typing import Optional
from .providers.index import Provider
from .index import Mail


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, "../../core/utils/templates/mail_templates/reset_password_template.html")


class ResetPassword(Mail):
    def __get_reset_password_mail_body(self, reset_password_link: str):
        with open(TEMPLATE_PATH, "r", encoding="utf-8") as file:
            template = file.read()
        return template.replace("{{reset_password_link}}", reset_password_link)

    def send(self, recipient: str, provider: Provider, verification_link: Optional[str] = None, current_time: Optional[str] = None, account_settings_url: Optional[str] = None, reset_password_link: Optional[str] = None):
        subject = "Action Required: Reset Your Aimple AI Password"
        body = ResetPassword.__get_reset_password_mail_body(self, reset_password_link)
        
        provider.send_mail(recipient, {"Data": subject}, {"Html": {"Data": body}})