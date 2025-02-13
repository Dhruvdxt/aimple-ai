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