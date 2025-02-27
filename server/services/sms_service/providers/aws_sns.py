from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from os import getenv
from ....config.sms_sender_config import sns_client
from .index import Provider


class AWSSNS(Provider):
    def send_sms(self, phone_number: str, message: str):
        """Send sms using AWS SNS"""
        try:
            response = sns_client.publish(
                PhoneNumber=phone_number,
                Message=message,
                MessageAttributes={
                    'AWS.SNS.SMS.SenderID': {
                        'DataType': 'String',
                        'StringValue': 'Aimple-AI'
                    },
                    'AWS.SNS.SMS.SMSType': {
                        'DataType': 'String',
                        'StringValue': 'Transactional'
                    }
                }
            )
            print("_________________Otp_sent_________________")
            print(response["MessageId"])
            return {"message": "SMS sent successfully!", "MessageId": response["MessageId"]}
        
        except NoCredentialsError:
            print("_________________NoCredentialsError_________________")
            return {"error": "AWS credentials not found"}
        
        except PartialCredentialsError:
            print("_________________PartialCredentialsError_________________")
            return {"error": "Incomplete AWS credentials"}
        
        except Exception as e:
            print("_________________Exception_________________")
            return {"error": str(e)}