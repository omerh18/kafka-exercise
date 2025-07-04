from prometheus_client import start_http_server, Counter
from kafka import KafkaConsumer
from schemas import message_pb2
import yaml
import os

CONSUMER_GROUP = 'my-consumergroup'

execution_env = os.getenv("EXEC_ENV", "local")
with open(f"config/{execution_env}.yml", "r") as f:
    config = yaml.safe_load(f)
    bootstrap_servers = config['Kafka']['bootstrap_servers']
    topic_name = config['Kafka']['topic_name']

consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers=bootstrap_servers,
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id=CONSUMER_GROUP,
)

messages_consumed = Counter(
    'messages_consumed', 
    'Total messages consumed',
    ['partition', 'consumer_group']
)
start_http_server(8001)

for message in consumer:

    partition_id = message.partition
    value_bytes = message.value

    try:
        # Deserialize
        msg = message_pb2.MyMessage()
        msg.ParseFromString(value_bytes)

        # Access fields
        timestamp = msg.timestamp
        contents = msg.contents

        print(f"Received: {timestamp=}, {contents=}, from partition #{partition_id}")

        messages_consumed.labels(
            partition=str(partition_id), 
            consumer_group=CONSUMER_GROUP
        ).inc()

    except Exception as e:
        print(f"ERROR: Failed to parse message from partition {partition_id}: {e}")
