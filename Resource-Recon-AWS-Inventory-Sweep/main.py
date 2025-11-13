import boto3
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("PG_HOST"),
    port=os.getenv("PG_PORT"),
    user=os.getenv("PG_USER"),
    password=os.getenv("PG_PASSWORD"),
    database=os.getenv("PG_DATABASE")
)
cur = conn.cursor()

def save_resource(resource_id, service, region, resource_type):
    cur.execute("""
        INSERT INTO aws_resources (resource_id, service, region, resource_type)
        VALUES (%s, %s, %s, %s)
    """, (resource_id, service, region, resource_type))
    conn.commit()

# Get all AWS regions
ec2 = boto3.client("ec2")
regions = [r['RegionName'] for r in ec2.describe_regions()['Regions']]
print({ "submitted_by": "adhwaithas@muid" })

# --------- SCAN EC2 (Instances) ---------
def scan_ec2():
    for region in regions:
        ec2 = boto3.client("ec2", region_name=region)
        reservations = ec2.describe_instances()["Reservations"]

        for res in reservations:
            for instance in res["Instances"]:
                instance_id = instance["InstanceId"]
                save_resource(instance_id, "EC2", region, "Instance")

        print(f"[EC2] Scanned {region}")

# --------- SCAN S3 (Buckets) - Global but store region ---------
def scan_s3():
    s3 = boto3.client("s3")
    buckets = s3.list_buckets().get("Buckets", [])

    for bucket in buckets:
        bucket_name = bucket["Name"]
        region = "us-east-1"
        try:
            loc = s3.get_bucket_location(Bucket=bucket_name)
            if loc.get("LocationConstraint"):
                region = loc["LocationConstraint"]
        except:
            pass

        save_resource(bucket_name, "S3", region, "Bucket")

    print("[S3] Scanned all buckets")

# --------- SCAN Lambda ---------
def scan_lambda():
    for region in regions:
        lam = boto3.client("lambda", region_name=region)

        functions = lam.list_functions().get("Functions", [])
        for fn in functions:
            fn_arn = fn["FunctionArn"]
            save_resource(fn_arn, "Lambda", region, "Function")

        print(f"[Lambda] Scanned {region}")

scan_ec2()
scan_s3()
scan_lambda()
cur.close()
conn.close()
print("✔ AWS Resource Discovery Completed")
