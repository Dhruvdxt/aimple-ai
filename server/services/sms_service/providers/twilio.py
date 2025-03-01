from ....config.twilio_config import twilio_client
from os import getenv
from .index import Provider


class Twilio(Provider):
    def send_sms(self, phone_number: str, message: str):
        """Send sms using Twilio"""
        try:
            message = twilio_client.messages.create(
                body=message,
                from_=getenv('TWILIO_PHONE_NUMBER'),
                to=phone_number
            )
            print("_________________mail_sent_________________")
            return {"message": "SMS sent successfully", "sid": message.sid}
        except Exception as e:
            print("_________________exception_________________")
            print(e)
            return {"error": str(e)}