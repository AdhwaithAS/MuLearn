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

ec2 = boto3.client(
    "ec2",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_DEFAULT_REGION")
)

regions = [r["RegionName"] for r in ec2.describe_regions()["Regions"]]

all_instances = []
for region in regions:
    print(f"Scanning region: {region}")

    ec2_regional = boto3.client(
        "ec2",
        region_name=region,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    response = ec2_regional.describe_instances()

    for reservation in response.get("Reservations", []):
        for instance in reservation.get("Instances", []):
            instance_id = instance.get("InstanceId")
            instance_type = instance.get("InstanceType")
            state = instance.get("State", {}).get("Name")
            launch_time = instance.get("LaunchTime")

            all_instances.append(
                (instance_id, region, instance_type, state, launch_time)
            )
insert_query = """
    INSERT INTO ec2_instances (instance_id, region, instance_type, state, launch_time)
    VALUES %s
    ON CONFLICT (instance_id) DO UPDATE 
    SET region = EXCLUDED.region,
        instance_type = EXCLUDED.instance_type,
        state = EXCLUDED.state,
        launch_time = EXCLUDED.launch_time;
"""

execute_values(cursor, insert_query, all_instances)
conn.commit()
print({ "submitted_by": "adhwaithas@muid" })
print("\n--- EC2 Instances Fetched & Stored Successfully ---")
print(f"Total Instances Found: {len(all_instances)}")
cursor.close()
conn.close()
