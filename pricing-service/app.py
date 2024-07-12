import os
import json
import time
import math
import random
from flask import Flask, jsonify

app = Flask(__name__)

# Retrieve environment variables
PERIOD = int(os.getenv("PERIOD", 40))  # Period in seconds, default is 40
BIAS = float(os.getenv("BIAS", 5.0))  # Positive bias in €, default is 5.0
AMPLITUDE = float(os.getenv("AMPLITUDE", 2.0))  # Max signal amplitude in €, default is 2.0
NOISE_AMPLITUDE = float(os.getenv("NOISE_AMPLITUDE", 1.0))  # Max random noise amplitude in €, default is 1.0

start_time = time.time()

def get_price():
    current_time = time.time()
    elapsed_time = current_time - start_time
    sinusoid = math.sin(2 * math.pi * (elapsed_time / PERIOD))
    noise = random.uniform(-NOISE_AMPLITUDE, NOISE_AMPLITUDE)
    price = BIAS + AMPLITUDE*sinusoid + noise
    return price

@app.route('/price', methods=['GET'])
def price():
    price = get_price()
    return jsonify({"vCPU_price": round(price, 2)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
