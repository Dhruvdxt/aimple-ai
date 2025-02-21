from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from os import getenv
from enum import Enum
from ...config.mailer_config import ses_client as SES, BaseClient


class ProviderType(str, Enum):
    SES = "SES"


map: dict[str, BaseClient] = {
    "SES": SES
}


class Mailer():
    def send_mail(self, recipient: str, provider: ProviderType, subject: dict, body: dict):
        """Send email using AWS SES"""
        try:
            response = map[provider].send_email(
                Source=f"Aimple AI <{getenv('AWS_SES_SENDER')}>",
                Destination={"ToAddresses": [recipient]},
                Message={
                    "Subject": subject,
                    "Body": body
                },
            )
            print("No Error___________________")
            return {"message": "Email sent successfully!", "MessageId": response["MessageId"]}
        
        except NoCredentialsError:
            print("NoCredentialsError________________________")
            return {"error": "AWS credentials not found"}
        
        except PartialCredentialsError:
            print("PartialCredentialsError________________________")
            return {"error": "Incomplete AWS credentials"}
        
        except Exception as e:
            print("Exception________________________")
            print(str(e))
            return {"error": str(e)}
    

