from kafka import KafkaProducer
import json

# Configure the Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=["localhost:9092", "localhost:9093", "localhost:9094"],
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

# Define the topic and data
topic = "my_topic"
message = {"key": "value"}

# Send the message
producer.send(topic, message)
producer.flush()

print(f"Message sent to topic {topic}")
