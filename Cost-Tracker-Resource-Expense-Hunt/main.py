import boto3
import psycopg2
from datetime import datetime, timedelta
import os
import random
from dotenv import load_dotenv
load_dotenv()
ce = boto3.client("ce")

conn = psycopg2.connect(
    host=os.getenv("PG_HOST"),
    port=os.getenv("PG_PORT"),
    user=os.getenv("PG_USER"),
    password=os.getenv("PG_PASSWORD"),
    database=os.getenv("PG_DATABASE")
)
cur = conn.cursor()
cursor = conn.cursor()

end = datetime.utcnow().date()
start = end - timedelta(days=365)
start_str = start.strftime("%Y-%m-%d")
end_str = end.strftime("%Y-%m-%d")

print({"submitted_by": "adhwaithas@muid"})
print("TimePeriod:", start_str, "->", end_str)

resp = ce.get_cost_and_usage(
    TimePeriod={"Start": start_str, "End": end_str},
    Granularity="DAILY",
    Metrics=["UnblendedCost"],
    GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}]
)

service_costs = {}
for day in resp.get("ResultsByTime", []):
    groups = day.get("Groups", [])
    for g in groups:
        service = g["Keys"][0]
        cost = float(g["Metrics"]["UnblendedCost"]["Amount"])

        if service not in service_costs:
            service_costs[service] = 0.0
        service_costs[service] += cost

sorted_costs = [
    (svc, amt) for svc, amt in sorted(service_costs.items(), key=lambda x: x[1])
    if amt > 0
]

for service, cost in sorted_costs:
    cursor.execute("""
        INSERT INTO aws_cost_data (resource_id, service, cost, start_date, end_date, submitted_by)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (random.randint(92382, 1000000), service, cost, start_str, end_str, "adhwaithas@muid"))

    print(f"Inserted → {service} : ${cost}")

conn.commit()
cursor.close()
conn.close()
