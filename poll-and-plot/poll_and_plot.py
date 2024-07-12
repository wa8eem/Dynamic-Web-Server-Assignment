import requests
import time
import matplotlib.pyplot as plt
from datetime import datetime
import argparse

# Parse command line arguments
parser = argparse.ArgumentParser(description="Poll a pricing service and plot the price over time.")
parser.add_argument('--url', type=str, required=True, help="The URL of the pricing service")
parser.add_argument('--interval', type=float, default=0.5, help="Polling interval in seconds")
parser.add_argument('--duration', type=int, default=40, help="Duration to poll in seconds")
parser.add_argument('--output', type=str, default='plot.png', help="Output file for the plot")
args = parser.parse_args()

# Configuration
url = args.url
polling_interval = args.interval
duration = args.duration
output_file = args.output

# Lists to store timestamps and prices
timestamps = []
prices = []

# Start polling
start_time = time.time()
while time.time() - start_time < duration:
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        prices.append(data["vCPU_price"])
        timestamps.append(datetime.now())
    else:
        print(f"Failed to get data: {response.status_code}")
    time.sleep(polling_interval)

# Plotting
plt.figure(figsize=(10, 5))
plt.plot(timestamps, prices, marker='o')
plt.title("vCPU Price Over Time")
plt.xlabel("Time")
plt.ylabel("Price (€)")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(output_file)
print(f"Plot saved to {output_file}")
