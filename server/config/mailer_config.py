import boto3
from botocore.client import BaseClient
import os

# AWS_REGION = os.getenv("AWS_SES_REGION")

# ses_client = boto3.client(
#     "ses",
#     region_name=AWS_REGION
# )


session = boto3.session.Session()
ses_client: BaseClient = session.client("ses", region_name=os.getenv("AWS_SES_REGION"))