import os
from typing import Optional
from .providers.index import Provider
from .index import Mail


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, "../../core/utils/templates/mail_templates/password_reset_template.html")


class PasswordReset(Mail):
    def __get_password_reset_mail_body(self, current_time: str, account_settings_url: str):
        with open(TEMPLATE_PATH, "r", encoding="utf-8") as file:
            template = file.read()
            
        return template.replace("{{current_time}}", current_time).replace("{{account_settings_url}}", account_settings_url)

    async def send(self, recipient: str, provider: Provider, verification_link: Optional[str] = None, current_time: Optional[str] = None, account_settings_url: Optional[str] = None, reset_password_link: Optional[str] = None):
        subject = "Security Alert: Password Modified"
        body = PasswordReset.__get_password_reset_mail_body(self, current_time, account_settings_url)
        
        await provider.send_mail(recipient, {"Data": subject}, {"Html": {"Data": body}})