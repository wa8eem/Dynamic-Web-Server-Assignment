#!/bin/bash

# Function to check if a container is running
is_container_running() {
    docker ps --filter "name=$1" --format '{{.Names}}' | grep -w "$1" > /dev/null 2>&1
}

# Stop containers if they are running
if is_container_running rate-limited-service-03; then
    echo "Stopping rate-limited-service-03..."
    docker stop rate-limited-service-03
else
    echo "Container rate-limited-service-03 is not running."
fi

if is_container_running rate-limited-service-10; then
    echo "Stopping rate-limited-service-10..."
    docker stop rate-limited-service-10
else
    echo "Container rate-limited-service-10 is not running."
fi

if is_container_running pricing-service; then
    echo "Stopping pricing-service..."
    docker stop pricing-service
else
    echo "Container pricing-service is not running."
fi

# Remove network if it exists
if docker network ls --filter "name=pricing-network" --format '{{.Name}}' | grep -w "pricing-network" > /dev/null 2>&1; then
    echo "Removing network pricing-network..."
    docker network rm pricing-network
else
    echo "Network pricing-network does not exist."
fi
