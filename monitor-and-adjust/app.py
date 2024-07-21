import time
import requests
import docker
import uuid

# Initialize Docker client
client = docker.from_env()

def get_current_price():
    """Fetch the current price from the pricing API."""
    try:
        # response = requests.get('http://0.0.0.0:20100/price')
        response = requests.get('http://host.docker.internal:20100/price')
        response.raise_for_status()
        return response.json().get('vCPU_price', 0)
    except requests.RequestException as e:
        print(f"Request error: {e}")
        raise

def get_container_rps(container):
    """Retrieve the RPS environment variable from a container."""
    try:
        env_vars = container.attrs['Config']['Env']
        for env_var in env_vars:
            if env_var.startswith("RPS="):
                return env_var.split('=')[1]
    except (docker.errors.NotFound, IndexError) as e:
        print(f"Error retrieving RPS: {e}")
    return None

def generate_unique_name(base_name):
    """Generate a unique container name using UUID."""
    return f"{base_name}-{uuid.uuid4().hex[:8]}"

def run_or_restart_service(container_name, rps, host_port):
    """Run a new container or restart an existing one with the given RPS and port."""
    if is_container_running(container_name):
        container = client.containers.get(container_name)
        container.stop()
    
    client.containers.run(
        "rate-limited-service",
        detach=True,
        remove=True,
        name=container_name,
        environment={"RPS": str(rps)},
        ports={"80/tcp": host_port},
        network="pricing-network"
    )

def is_container_running(container_name):
    """Check if a container is currently running."""
    try:
        container = client.containers.get(container_name)
        return container.status == 'running'
    except docker.errors.NotFound:
        return False

def determine_instance_configuration(price):
    """Determine instance type, number of instances, and naming convention based on the price."""
    if price >= 7:
        return "3", 1, "rate-limited-service-03", 20003
    elif price >= 5:
        return "3", 2, "rate-limited-service-03", 20003
    elif price >= 3:
        return "10", 1, "rate-limited-service-10", 20010
    else:
        return "10", 2, "rate-limited-service-10", 20010

def update_rate_limited_services(price):
    """Update the number of rate-limited-service containers based on the current price."""
    instance_type, num_instances, base_name, base_port = determine_instance_configuration(price)

    # List all containers with the ancestor image
    current_containers = client.containers.list(filters={"ancestor": "rate-limited-service"})
    
    # Get existing container names and ports
    existing_container_names = {container.name for container in current_containers}
    
    # Determine containers to stop and start
    containers_to_stop = []
    containers_to_start = []

    current_instance_type = get_container_rps(current_containers[0]) if current_containers else None

    print("Instance Type:", instance_type)
    print("No. Instances:", num_instances)
    if current_instance_type != instance_type:
        # Stop all existing containers if instance type has changed
        containers_to_stop = current_containers
        containers_to_start = range(0, num_instances)
    else:
        excess_instances = len(existing_container_names) - num_instances
        if excess_instances > 0:
            containers_to_stop = current_containers[:excess_instances]
        else:
            containers_to_start = range(len(existing_container_names), num_instances)

    # Stop and remove excess containers
    for container in containers_to_stop:
        container.stop()

    # Allocate unique ports and names, and start new containers
    used_ports = {container.attrs['HostConfig']['PortBindings']['80/tcp'][0]['HostPort']
                  for container in current_containers}
    
    for i in containers_to_start:
        container_name = generate_unique_name(base_name)
        host_port = base_port + len(existing_container_names) + i

        # Ensure port is unique
        while str(host_port) in used_ports:
            host_port += 1

        run_or_restart_service(container_name, instance_type, host_port)
        used_ports.add(str(host_port))  # Update used ports

def main():
    """Main loop to monitor price and update services accordingly."""
    while True:
        try:
            current_price = get_current_price()
            print(f"\nCurrent price: {current_price}€")

            update_rate_limited_services(current_price)
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(1)

if __name__ == "__main__":
    main()
