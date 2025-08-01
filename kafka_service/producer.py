from kafka import KafkaProducer
import time
import csv
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

with open('location.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        location = {
            "latitude": float(row["latitude"]),
            "longitude": float(row["longitude"])
        }
        producer.send("delivery_location", value=location)
        print("📍 Sent location:", location)
        time.sleep(3)  # Simulate live update every 3 seconds
