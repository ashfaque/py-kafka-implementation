#!/usr/bin/env python3
import json
import sys
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from config import BOOTSTRAP_SERVERS, TOPICS


def json_deserializer(data: bytes) -> dict:
    """Deserialize a JSON byte string to a dictionary."""
    return json.loads(data.decode("utf-8"))


def create_consumer(topic, group_id):
    """Create and return a Kafka consumer with specific configurations."""
    return KafkaConsumer(
        topic,  # Subscribe to the specified topic
        bootstrap_servers=BOOTSTRAP_SERVERS,  # List of Kafka broker addresses
        auto_offset_reset="earliest",  # Start reading at the earliest message
        enable_auto_commit=True,  # Automatically commit offsets
        group_id=group_id,  # Consumer group ID for coordinating consumption
        value_deserializer=json_deserializer,  # Deserialize messages from JSON to dict
        consumer_timeout_ms=1000,  # Timeout for polling messages (1 second)
    )


def main():
    topic = TOPICS["consumer1"]  # HC
    consumer = create_consumer(topic, group_id="group1")  # HC
    print(f"Consumer1 listening on '{topic}' (group 'group1'). Ctrl+C to exit.")
    try:
        while True:
            for msg in consumer:
                print(
                    f"[Consumer1] {msg.timestamp} | {msg.topic}@{msg.partition}/{msg.offset}: {msg.value}"
                )
            # consumer_timeout_ms causes __iter__ to end; loop back to poll again
    except KeyboardInterrupt:
        print("Shutting down consumer1.")
    except KafkaError as e:
        print(f"Consumer error: {e}", file=sys.stderr)
    finally:
        consumer.close()


if __name__ == "__main__":
    main()


"""
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
"""
