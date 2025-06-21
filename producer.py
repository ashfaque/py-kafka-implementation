import json
import random
import time
from kafka import KafkaProducer
from kafka.errors import KafkaError
from config import BOOTSTRAP_SERVERS, TOPICS


def json_serializer(data: dict) -> bytes:
    """Serialize a dictionary to a JSON byte string."""
    return json.dumps(data).encode("utf-8")


def create_producer():
    """Create and return a Kafka producer with specific configurations."""
    return KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,  # List of Kafka broker addresses
        value_serializer=json_serializer,  # Serialize messages from dict to JSON
        retries=5,  # Retry sending messages up to 5 times
        # linger_ms=10,  # Wait up to 10ms to batch messages
        acks="all",  # Wait for all replicas to acknowledge the message, ensuring durability.
    )


def send(producer, topic, data):
    """Send one JSON message to the given topic, synchronously."""
    future = producer.send(topic, data)
    try:
        record_metadata = future.get(timeout=10)
        print(
            f"Message sent to {record_metadata.topic} "
            f"partition {record_metadata.partition} "
            f"offset {record_metadata.offset}"
        )
    except KafkaError as e:
        print(f"Failed to send message to {topic}: {e}")


def main():
    """Main function to run the producer."""
    print("Starting Kafka producer...")
    producer = create_producer()
    all_topics = list(TOPICS.values())

    print("Producer up. Press Ctrl+C to exit.")
    try:
        while True:
            # Decide randomly: broadcast to all or single topic
            if random.random() < 0.5:
                # send same data to all topics
                payload = {"event": "broadcast", "value": random.randint(1, 100)}
                for topic in all_topics:
                    send(producer, topic, payload)
            else:
                # send unique data to one random topic
                topic = random.choice(all_topics)
                payload = {
                    "event": "single",
                    "topic": topic,
                    "value": random.randint(100, 200),
                }
                send(producer, topic, payload)

            time.sleep(1 + random.random() * 2)  # adhoc pacing
    except KeyboardInterrupt:
        print("Shutting down producer.")
    finally:
        producer.flush()
        producer.close()


if __name__ == "__main__":
    main()


"""
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
"""
