from kafka import KafkaConsumer
import json

# Configure the Kafka Consumer
consumer = KafkaConsumer(
    "my_topic",  # Define topic name here
    bootstrap_servers=["localhost:9092", "localhost:9093", "localhost:9094"],
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="my-consumer-group",
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
)

# Consume messages
for message in consumer:
    print(f"Consumed message: {message.value}")
