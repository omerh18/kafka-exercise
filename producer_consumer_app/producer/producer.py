from prometheus_client import start_http_server, Counter
from kafka import KafkaProducer, KafkaAdminClient
from schemas import message_pb2
import yaml
import time
import os

execution_env = os.getenv("EXEC_ENV", "local")
with open(f"config/{execution_env}.yml", "r") as f:
    config = yaml.safe_load(f)
    bootstrap_servers = config['Kafka']['bootstrap_servers']
    topic_name = config['Kafka']['topic_name']

admin_client = KafkaAdminClient(
    bootstrap_servers=bootstrap_servers
)
metadata = admin_client.describe_topics([topic_name])
partitions = [partition['partition'] for partition in metadata[0]['partitions']]

producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    value_serializer=lambda v: v,
    key_serializer=lambda k: str(k).encode('utf-8')
)

messages_sent = Counter(
    'messages_produced', 
    'Total messages produced',
    ['partition']
)
start_http_server(8000)

while True:

    for partition_id in partitions:

        msg = message_pb2.MyMessage()
        msg.timestamp = int(time.time() * 1000)
        msg.contents = f"This is message to partition #{partition_id}"

        value_bytes = msg.SerializeToString()

        for _ in range(partition_id):
            producer.send(
                topic_name,
                value=value_bytes,
                partition=partition_id
            )
            messages_sent.labels(
                partition=str(partition_id)
            ).inc()
        
        time.sleep(1)
