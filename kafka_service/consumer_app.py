from kafka import KafkaConsumer
import json
from kafka_service.location_store import latest_location

def start_consumer():
    consumer = KafkaConsumer(
        'delivery_location',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='latest',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    print("🚀 Kafka consumer started...")

    for message in consumer:
        latest_location.clear()
        latest_location.update(message.value)
        print("📍 Location Update:", latest_location)

if __name__ == "__main__":
    start_consumer()
