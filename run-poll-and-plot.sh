#!/bin/bash

# Function to check if a container is running
is_container_running() {
    docker ps --filter "name=$1" --format '{{.Names}}' | grep -w "$1" > /dev/null 2>&1
}

# Ensure the network exists
if ! docker network ls --filter "name=pricing-network" --format '{{.Name}}' | grep -w "pricing-network" > /dev/null 2>&1; then
    echo "Creating network pricing-network..."
    docker network create pricing-network
fi

# Ensure the pricing-service is running
if ! is_container_running pricing-service; then
    echo "Starting pricing-service..."
    docker run --rm --network pricing-network --name pricing-service -p 20100:80 -d pricing-service
fi

# Run poll-and-plot container
docker run --rm --network pricing-network -v "$(pwd):/app/output" poll-and-plot --url http://pricing-service:80/price --interval 0.5 --duration 40 --output /app/output/plot.png
