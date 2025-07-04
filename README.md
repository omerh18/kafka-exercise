# Kafka Producer-Consumer App

This repository contains a Python-based Kafka producer and consumer application, designed for demonstration and monitoring with Prometheus. The setup is containerized using Docker and orchestrated with Docker Compose.

## Structure

- **producer_consumer_app/**
  - **producer/**: Kafka producer service (Python, Dockerfile)
  - **consumer/**: Kafka consumer service (Python, Dockerfile)
  - **schemas/**: Protocol Buffers schema and generated Python code
  - **config/**: Environment-specific YAML configuration files
  - **pyproject.toml**: Python project dependencies
  - **README.md**: Project documentation

- **docker-compose.yml**: Defines Zookeeper, Kafka, and Prometheus services
- **prometheus.yml**: Prometheus scrape configuration
- **infra_setup.sh**: Script to start infrastructure and create Kafka topic
- **producer_consumer_setup.sh**: Script to build and run producer/consumer containers

## Features

- **Kafka Producer**: Publishes Protocol Buffers-encoded messages to a configurable topic and partition.
- **Kafka Consumer**: Subscribes to the topic, deserializes messages, and prints their contents.
- **Prometheus Metrics**: Both producer and consumer expose metrics endpoints for monitoring.
- **Dockerized**: All components can be built and run as containers for local or production-like environments.

## Quick Start

1. **Start Infrastructure**  
   ```bash
   chmod +x ./infra_setup.sh
   ./infra_setup.sh
   chmod +x ./producer_consumer_setup
   ./producer_consumer_setup