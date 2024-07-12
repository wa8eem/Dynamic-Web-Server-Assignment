### README.md

# Dynamic Web Server Assignment

## Overview

This assignment involves setting up and managing a dynamic web server infrastructure based on the fluctuating price of a vCPU. The price oscillates between 2€ and 8€ periodically every 40 seconds. Based on the current price, you will adapt the number and type of web servers running. The provided setup includes a pricing service, rate-limited web servers, and a visualization tool.

## Provided Scripts and Containers

### 1. Pricing Service

The **pricing-service** container simulates the price of a vCPU. It fluctuates according to a biased noisy sinusoid function, configurable via environment variables:

- **PERIOD**: Period of the sinusoid function in seconds (default: 40).
- **BIAS**: Positive bias in € (default: 5).
- **AMPLITUDE**: Maximum amplitude of sinusoid function in € (default: 2).
- **NOISE_AMPLITUDE**: Maximum random noise amplitude in € (default: 1).

**Files:**

- `pricing-service/app.py`: The main application file for the pricing service.
- `pricing-service/Dockerfile`: Dockerfile to build the pricing service image.

### 2. Rate-Limited Service

The **rate-limited-service** container serves HTTP requests at a configurable rate. It can be set to serve either 3 or 10 requests per second via the **RPS** environment variable.

**Files:**

- `rate-limited-service/app.py`: The main application file for the rate-limited service.
- `rate-limited-service/Dockerfile`: Dockerfile to build the rate-limited service image.

### 3. Poll and Plot Service

The **poll-and-plot** container is a tool to visualize the price of the vCPU over time. It polls the pricing service every 500ms and generates a plot.

**Files:**

- `poll-and-plot/poll_and_plot.py`: Python script to poll the pricing service and plot the price.
- `poll-and-plot/Dockerfile`: Dockerfile to build the poll and plot image.

### 4. Helper Scripts

**build-all.sh**: Builds all Docker images.

**run-all.sh**: Creates the network and runs the containers.

**stop-all.sh**: Stops all containers and removes the network.

**run-poll-and-plot.sh**: Runs the poll-and-plot container one.

## Assignment

### Objective

Write code to monitor the price of a vCPU by making requests to the pricing-service. Based on the current price, dynamically adjust the type and number of rate-limited-service instances running in the Docker network.

### Requirements

1. **Monitor the Price**:
	- Make periodic requests to the pricing-service to fetch the current price **at least** every 1 second.

2. **Adjust Rate-Limited Services**:
	- **Price >= 5€**: Use the slower (3 RPS) webservers.
		- **Price [5, 7) €**: Run 2 instances.
		- **Price >= 7 €**: Run 1 instance.
	- **Price < 5€**: Use the faster (10 RPS) webservers.
		- **Price [3, 5) €**: Run 1 instance.
		- **Price < 3 €**: Run 2 instances.

### Implementation

- Use any programming language (Python recommended) to implement the monitoring and management logic.
- Interact with the Docker daemon to start and stop instances dynamically based on the price.

### Conclusion

This assignment involves creating a dynamic web server infrastructure based on the fluctuating price of a simplified resource (a vCPU). 

By monitoring the price and adjusting the number and type of running instances, you will ensure efficient resource usage based on the current price. 
Use the provided scripts and containers as a foundation to implement the desired functionality. 


## License

**Dynamic Web Server Assignment**

Copyright (C) 2024 Remous Aris KOUTSIAMANIS

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
