import boto3
from botocore.client import BaseClient
import os

# AWS_REGION = os.getenv("AWS_SNS_REGION")

# sns_client = boto3.client(
#     "sns",
#     region_name=AWS_REGION
# )

session = boto3.session.Session()
sns_client: BaseClient = session.client("sns", region_name=os.getenv("AWS_SNS_REGION"))