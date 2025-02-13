import boto3
import os

AWS_REGION = os.getenv("AWS_SNS_REGION")

sns_client = boto3.client(
    "sns",
    region_name=AWS_REGION
)