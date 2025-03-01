import aiosmtplib
from email.message import EmailMessage
from os import getenv
from .index import Provider


class SMTP(Provider):
    async def send_mail(self, recipient: str, subject: dict, body: dict):
        """Send email using SMTP"""
        msg = EmailMessage()
        msg["From"] = getenv('SENDER_EMAIL')
        msg["To"] = recipient
        msg["Subject"] = subject.get('Data')
        msg.set_content(body.get('Html').get('Data'), subtype="html")

        try:
            await aiosmtplib.send(
                msg,
                hostname=getenv('SMTP_SERVER'),
                port=getenv('SMTP_PORT'),
                username=getenv('SMTP_USERNAME'),
                password=getenv('SMTP_PASSWORD'),
                use_tls=False,
                start_tls=True,
            )
            return {"message": "Email sent successfully"}
        except Exception as e:
            return {"error": str(e)}
        