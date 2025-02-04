import boto3
import os

AWS_REGION = os.getenv("AWS_REGION")
AWS_SES_SENDER = os.getenv("AWS_SES_SENDER")

ses_client = boto3.client(
    "ses",
    region_name=AWS_REGION
)