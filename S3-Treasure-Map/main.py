import boto3
import psycopg2
from psycopg2.extras import execute_values
import os
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(
    host=os.getenv("PG_HOST"),
    database=os.getenv("PG_NAME"),
    user=os.getenv("PG_USER"),
    password=os.getenv("PG_PASSWORD"),
    port=os.getenv("PG_PORT")
)
cursor = conn.cursor()

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_DEFAULT_REGION")
)
response = s3.list_buckets()
buckets = response.get("Buckets", [])

all_bucket_data = []

print("\nScanning all S3 buckets...\n")

print({"submitted_by": "adhwaithas@muid"})
for bucket in buckets:
    bucket_name = bucket["Name"]
    creation_date = bucket["CreationDate"]
    location_resp = s3.get_bucket_location(Bucket=bucket_name)
    region = location_resp.get("LocationConstraint")

    if region is None:
        region = "us-east-1"

    all_bucket_data.append((bucket_name, region, creation_date))

    print(f"Found bucket: {bucket_name} | Region: {region}")

insert_query = """
    INSERT INTO s3_buckets (bucket_name, region, creation_date)
    VALUES %s
    ON CONFLICT (bucket_name) DO UPDATE 
    SET region = EXCLUDED.region,
        creation_date = EXCLUDED.creation_date;
"""

execute_values(cursor, insert_query, all_bucket_data)
conn.commit()

print("\n--- S3 Buckets Stored in PostgreSQL Successfully ---")
print(f"Total Buckets Found: {len(all_bucket_data)}")

cursor.close()
conn.close()
