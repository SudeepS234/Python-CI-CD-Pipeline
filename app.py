# app.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    """
    Root endpoint that returns a simple greeting.
    """
    return "Hello from Python App!"

@app.route('/health')
def health_check():
    """
    Health check endpoint for Kubernetes readiness/liveness probes.
    Returns a JSON response with status 'OK'.
    """
    return jsonify({"status": "OK"})

if __name__ == '__main__':
    # Run the Flask application on all available interfaces (0.0.0.0)
    # and on port 5000. This is important for Docker containers.
    app.run(host='0.0.0.0', port=5000)
