import logging
from http.server import BaseHTTPRequestHandler
import urllib.parse
import time
from kubernetes import client
import threading
import os

# Set environment variables
# Get the values of your-image and tag from environment variables
worker_image = os.environ.get("WORKER_IMAGE", "busybox")
worker_tag = os.environ.get("WORKER_TAG", "latest")

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def create_and_monitor_pod(self, index):
        job_name = f"job-{time.strftime('%y-%m-%d-%H-%M')}-{index}" # ZKValidator

        job = client.V1Job(
            metadata=client.V1ObjectMeta(name=job_name),
            spec=client.V1JobSpec(
                template=client.V1PodTemplateSpec(
                    spec=client.V1PodSpec(
                        containers=[
                            client.V1Container(
                                name="zk-validator",
                                image=f"{worker_image}:{worker_tag}",
                                command=["sleep", "10"],
                                env=[
                                    client.V1EnvVar(name="JobName", value="value1"),
                                    client.V1EnvVar(name="FileBatchList", value='[]'),
                                ],
                                image_pull_policy="Always",  # Set the image pull policy here
                            )
                        ],
                        restart_policy="Never",
                    )
                )
            )
        )

        namespace = open("/var/run/secrets/kubernetes.io/serviceaccount/namespace").read()
        api.create_namespaced_job(namespace, job)

        logging.info(f"Launching pod {index}")

        start_time = time.time()
        while True:
            pod = api.read_namespaced_job(job_name, namespace)
            if pod.status.succeeded is not None and pod.status.succeeded > 0:
                end_time = time.time()
                self.wfile.write(f"Pod {index} completed in {end_time - start_time} seconds\n".encode('utf-8'))
                logging.info(f"Pod {index} completed in {end_time - start_time} seconds")
                break
            time.sleep(1)