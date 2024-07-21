#!/bin/bash

# Function to check if a container is running
is_container_running() {
    docker ps --filter "name=$1" --format '{{.Names}}' | grep -w "$1" > /dev/null 2>&1
}

# Function to check if an image exists
is_image_present() {
    docker images --filter "reference=$1" --format '{{.Repository}}' | grep -w "$1" > /dev/null 2>&1
}

# Ensure the network exists
if ! docker network ls --filter "name=pricing-network" --format '{{.Name}}' | grep -w "pricing-network" > /dev/null 2>&1; then
    echo "Creating network pricing-network..."
    docker network create pricing-network
else
    echo "Network pricing-network already exists."
fi

# Ensure the pricing-service image exists
if ! is_image_present pricing-service; then
    echo "Error: pricing-service image not found. Please build the image first."
    exit 1
fi

# Ensure the monitor-and-adjust image exists
if ! is_image_present monitor-and-adjust; then
    echo "Error: monitor-and-adjust image not found. Please build the image first."
    exit 1
fi

# Ensure the pricing-service is running
if ! is_container_running pricing-service; then
    echo "Starting pricing-service..."
    docker run --rm --network pricing-network --name pricing-service -p 20100:80 -d pricing-service
else
    echo "pricing-service is already running."
fi

# Run or restart monitor-and-adjust container
if is_container_running monitor-and-adjust; then
    echo "Restarting monitor-and-adjust..."
    docker stop monitor-and-adjust
fi
# docker run --rm --name monitor-and-adjust --network pricing-network -d monitor-and-adjust # This fails to connect with Docker Daemon
docker run --name monitor-and-adjust --network pricing-network -v /var/run/docker.sock:/var/run/docker.sock -d monitor-and-adjust

