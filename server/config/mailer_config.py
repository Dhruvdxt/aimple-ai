import boto3
import os

AWS_REGION = os.getenv("AWS_SES_REGION")

ses_client = boto3.client(
    "ses",
    region_name=AWS_REGION
)