import requests
from os import getenv
from .index import Provider


class MSG91(Provider):
    def send_sms(self, phone_number: str, message: str):
        """Send sms using MSG91"""
        headers = {
            "authkey": getenv('MSG91_AUTH_KEY'),
            "Content-Type": "application/json"
        }
        
        payload = {
            "sender": getenv('MSG91_SENDER_ID'),
            "route": getenv('MSG91_ROUTE'),
            "country": "91",
            "sms": [
                {
                    "message": message,
                    "to": [phone_number]
                }
            ]
        }
        try:
            response = requests.post(getenv('MSG91_API_URL'), json=payload, headers=headers)

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