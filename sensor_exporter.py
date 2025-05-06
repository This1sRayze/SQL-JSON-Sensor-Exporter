import pyodbc
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import time
import json

with open('config.json', 'r') as f:
    config = json.load(f)

server = config["server"]
database = config["database"]
username = config["username"]
password = config["password"]
push_gateway_url = config["push_gateway_url"]
query = config["query"]

conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                      f'SERVER={server};'
                      f'DATABASE={database};'
                      f'UID={username};'
                      f'PWD={password}')
cursor = conn.cursor()

cursor.execute(query)
rows = cursor.fetchall()

registry = CollectorRegistry()

for row in rows:
    hour = row[0]
    avg_value = row[1]
    avg_value2 = row[2]
    avg_value3 = row[3]

    gauge_avg_value = Gauge("sensor_avg_value", "Average value of sensor readings", labelnames=["hour"], registry=registry)
    gauge_avg_value.labels(hour=str(hour)).set(avg_value)

    gauge_avg_value2 = Gauge("sensor_avg_value2", "Average value2 of sensor readings", labelnames=["hour"], registry=registry)
    gauge_avg_value2.labels(hour=str(hour)).set(avg_value2)

    gauge_avg_value3 = Gauge("sensor_avg_value3", "Average value3 of sensor readings", labelnames=["hour"], registry=registry)
    gauge_avg_value3.labels(hour=str(hour)).set(avg_value3)

    push_to_gateway(push_gateway_url, job='sensor_data', registry=registry)

conn.close()
