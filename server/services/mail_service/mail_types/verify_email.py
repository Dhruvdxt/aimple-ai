import os
from ..mailer import send_mail


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, "../../../core/utils/templates/mail_templates/verify_email_template.html")


def get_verify_email_mail_body(verification_link: str):
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as file:
        template = file.read()
    return template.replace("{{verification_link}}", verification_link)


def send_verify_email_mail(recipient: str, verification_link: str):
    subject = "Action Required: Verify Your Email for Aimple AI"
    body = get_verify_email_mail_body(verification_link)
    
    send_mail(recipient, {"Data": subject}, {"Html": {"Data": body}})
    return
    