import boto3
import os
from dotenv import load_dotenv

load_dotenv()
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_DEFAULT_REGION")

ec2_client = boto3.client(
    "ec2",
    region_name=aws_region,
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key
)

def list_aws_regions():
    response = ec2_client.describe_regions(AllRegions=True)
    
    print("submitted_by: adhwaithas@muid")
    print("Available AWS Regions:")
    for region in response["Regions"]:
        print(f"- {region['RegionName']} ({region['Endpoint']})")

if __name__ == "__main__":
    list_aws_regions()
