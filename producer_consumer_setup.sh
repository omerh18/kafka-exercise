#!/bin/bash

cd producer_consumer_app

docker build -f producer/Dockerfile -t my-kafka-producer:1.0 .

docker build -f consumer/Dockerfile -t my-kafka-consumer:1.0 .

docker run -d --rm --network kafka_exercise_kafka-net -e EXEC_ENV=prod -p 8000:8000 my-kafka-producer:1.0

docker run -d --rm --network kafka_exercise_kafka-net -e EXEC_ENV=prod -p 8001:8001 my-kafka-consumer:1.0
