from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from enum import Enum
from ...config.sms_sender_config import sns_client as SNS, BaseClient

class ProviderType(str, Enum):
    SNS = "SNS"


map: dict[str, BaseClient] = {
    "SNS": SNS
}


class SMSSender():
    def send_sms(self, provider: ProviderType, phone_number: str, message: str):
        """Send sms using AWS SNS"""
        try:
            response = map[provider].publish(
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
            return {"message": "Email sent successfully!", "MessageId": response["MessageId"]}
        
        except NoCredentialsError:
            return {"error": "AWS credentials not found"}
        
        except PartialCredentialsError:
            return {"error": "Incomplete AWS credentials"}
        
        except Exception as e:
            return {"error": str(e)}
    





from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from ...config.sms_sender_config import sns_client



def send_sms(phone_number: str, message: str):
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
        return {"message": "Email sent successfully!", "MessageId": response["MessageId"]}
    
    except NoCredentialsError:
        return {"error": "AWS credentials not found"}
    
    except PartialCredentialsError:
        return {"error": "Incomplete AWS credentials"}
    
    except Exception as e:
        return {"error": str(e)}