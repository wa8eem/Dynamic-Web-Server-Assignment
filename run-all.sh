#!/bin/bash

# Function to check if a container is running
is_container_running() {
    docker ps --filter "name=$1" --format '{{.Names}}' | grep -w "$1" > /dev/null 2>&1
}

# Create network if it doesn't exist
if ! docker network ls --filter "name=pricing-network" --format '{{.Name}}' | grep -w "pricing-network" > /dev/null 2>&1; then
    echo "Creating network pricing-network..."
    docker network create pricing-network
else
    echo "Network pricing-network already exists."
fi

# Run or restart rate-limited-service with RPS=3 on host port 20003
if is_container_running rate-limited-service-03; then
    echo "Restarting rate-limited-service-03..."
    docker stop rate-limited-service-03
fi
docker run --rm --network pricing-network --name rate-limited-service-03 -e RPS=3 -p 20003:80 -d rate-limited-service

# Run or restart rate-limited-service with RPS=10 on host port 20010
if is_container_running rate-limited-service-10; then
    echo "Restarting rate-limited-service-10..."
    docker stop rate-limited-service-10
fi
docker run --rm --network pricing-network --name rate-limited-service-10 -e RPS=10 -p 20010:80 -d rate-limited-service

# Run or restart pricing-service on host port 20100
if is_container_running pricing-service; then
    echo "Restarting pricing-service..."
    docker stop pricing-service
fi
docker run --rm --network pricing-network --name pricing-service -p 20100:80 -d pricing-service
