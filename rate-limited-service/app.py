from flask import Flask
from ratelimit import limits, sleep_and_retry
import os

app = Flask(__name__)
RPS = int(os.getenv("RPS", 10))  # Get the RPS value from environment variables

@sleep_and_retry
@limits(calls=RPS, period=1)
def limit_request():
    pass

@app.route('/')
def hello_world():
    limit_request()
    return 'Hello World!'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
