#!/bin/bash

# Build poll-and-plot image
docker build -t poll-and-plot ./poll-and-plot

# Build pricing-service image
docker build -t pricing-service ./pricing-service

# Build rate-limited-service image
docker build -t rate-limited-service ./rate-limited-service
 
