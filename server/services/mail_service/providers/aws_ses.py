from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from os import getenv
from ....config.mailer_config import ses_client
from .index import Provider


class AWSSES(Provider):
    def send_mail(self, recipient: str, subject: dict, body: dict):
        """Send email using AWS SES"""
        try:
            response = ses_client.send_email(
                Source=f"Aimple AI <{getenv('AWS_SES_SENDER')}>",
                Destination={"ToAddresses": [recipient]},
                Message={
                    "Subject": subject,
                    "Body": body
                },
            )
            return {"message": "Email sent successfully!", "MessageId": response["MessageId"]}
        
        except NoCredentialsError:
            return {"error": "AWS credentials not found"}
        
        except PartialCredentialsError:
            return {"error": "Incomplete AWS credentials"}
        
        except Exception as e:
            return {"error": str(e)}
        