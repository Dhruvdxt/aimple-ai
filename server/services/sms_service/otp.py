import os
from typing import Optional
from .providers.index import Provider
from .index import SMS


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, "../../core/utils/templates/mail_templates/verify_email_template.html")


class OTP(SMS):
    def send(self, phone_number: str, provider: Provider, otp: int):
        message = f"Your OTP is: {otp}. Valid for 2 minutes."
        provider.send_sms(phone_number=phone_number, message=message)
    # def __get_verify_email_mail_body(self, verification_link: str):
    #     with open(TEMPLATE_PATH, "r", encoding="utf-8") as file:
    #         template = file.read()
    #     return template.replace("{{verification_link}}", verification_link)
    
    # def send(self, pho: str, provider: Provider, verification_link: Optional[str] = None, current_time: Optional[str] = None, account_settings_url: Optional[str] = None, reset_password_link: Optional[str] = None):
    #     subject = "Action Required: Verify Your Email for Aimple AI"
    #     body = VerifyEmail.__get_verify_email_mail_body(self, verification_link)
        
    #     provider.send_mail(recipient, {"Data": subject}, {"Html": {"Data": body}})