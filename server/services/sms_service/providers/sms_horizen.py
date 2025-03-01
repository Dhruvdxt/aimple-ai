import requests
from os import getenv
from .index import Provider


class SMSHorizen(Provider):
    def send_sms(self, phone_number: str, message: str):
        """Send sms using SMS Horizen"""
        payload = {
            'user': getenv('SMS_Horizen_USER_NAME'),
            'apikey': getenv('SMS_Horizen_USER_NAME'),
            'mobile': phone_number,
            'message': message,
            'senderid': getenv('SMS_Horizen_USER_NAME'),
            'type': 'txt',
        }
        try:
            response = requests.post(getenv('SMS_Horizen_API_URL'), data=payload)

            if response.status_code == 200:
                print("________________________sms_sent________________________")
                print(message, phone_number)
                return {"message": "SMS sent successfully", "response": response.json()}
            else:
                print("________________________error________________________")
                return {"error": response.text}
        except Exception as e:
            print("_________________Exception_________________")
            print(e)
            return {"error": str(e)}