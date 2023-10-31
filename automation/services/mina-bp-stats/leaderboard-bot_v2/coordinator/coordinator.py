import os
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import time
from kubernetes import client, config
import threading
from server import SimpleHTTPRequestHandler

# Configure logging
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Load the in-cluster configuration
config.load_incluster_config()

# Create a Kubernetes API client
api = client.BatchV1Api()

def main():
    host = '0.0.0.0'  # Listen on all available network interfaces
    port = 8080  # The port you want to listen on

    server = HTTPServer((host, port), SimpleHTTPRequestHandler)
    print(f"Server started on {host}:{port}")

    # Log server startup
    logging.info(f"Server started on {host}:{port}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        print("\nServer stopped.")
        logging.info("Server stopped.")

if __name__ == '__main__':
    main()