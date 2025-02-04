from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from os import getenv
from ...config.mailer_config import ses_client


def send_mail(recipient: str, subject: dict, body: dict):
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