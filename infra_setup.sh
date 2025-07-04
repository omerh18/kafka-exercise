#!/bin/bash

docker-compose up -d

docker exec -it $(docker ps | grep 'bitnami/kafka' | awk '{print $1}') kafka-topics.sh --create \
  --topic my-topic \
  --bootstrap-server localhost:9092 \
  --partitions 100 \
  --replication-factor 1
