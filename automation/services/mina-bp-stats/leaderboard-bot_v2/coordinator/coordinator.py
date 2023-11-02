import os
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from kubernetes import client, config
from server import SimpleHTTPRequestHandler
from helper import createRegister, updateRegister, getDefinedMinute, checkPreviousRegister, createSlackPost, pullFileNames
from datetime import datetime, timedelta, timezone
import psycopg2
from dotenv import load_dotenv
import boto3

# Configure logging
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Load the in-cluster configuration
config.load_incluster_config()

# Create a Kubernetes API client
api = client.BatchV1Api()

def main():
    load_dotenv()
    
    connection = psycopg2.connect(
    host=os.environ['POSTGRES_HOST'],
    port=os.environ['POSTGRES_PORT'],
    database=os.environ['POSTGRES_DB'],
    user=os.environ['POSTGRES_USER'],
    password=os.environ['POSTGRES_PASSWORD']
)

    # Step 1 Record in the register table the current time interval i.e. now and (now - 20) minutes
    dateTimeNow = datetime.now(timezone.utc)
    interval = os.environ['SURVEY_INTERVAL_MINUTES']
    offset = os.environ['INTERVAL_OFFSET']
    minute = getDefinedMinute(interval, offset, dateTimeNow)
    end_dateTime = dateTimeNow.replace(second=0, microsecond=0, minute=minute)           
    start_dateTime = end_dateTime - timedelta(minutes=interval)
    createRegister(connection, start_dateTime, end_dateTime, logging)

    # Step 2 Check in the register table the previous time interval completed otherwise signal error. How do we signal error?
    prevRegisterOutput = checkPreviousRegister(connection, start_dateTime, logging)
    slack_token=os.environ["SLACK_API_TOKEN"]
    slack_channel=os.environ["SLACK_CHANNEL"]
    if prevRegisterOutput == False:
        message = f'Previous batch with end date {end_dateTime} did not complete'
        logging.error(message)
        createSlackPost(slack_token, slack_channel, message)
    elif prevRegisterOutput ==  -1:
        f'Previous batch with end date {end_dateTime} was never started'
        logging.error(message)
        createSlackPost(slack_token, slack_channel, message)
    
    # Step 3 Pull down list of files (not necessarily the files themselves)
    bucket= os.environ["BUCKET_NAME"]
    files_in_s3 = pullFileNames(start_dateTime,end_dateTime, bucket)
    mini_batches = [files_in_s3[i::os.environ['MINI_BATCH_NUMBER']] for i in range(os.environ['MINI_BATCH_NUMBER'])]

    # Step 4 Create Kubernetes ZKValidators
    host = os.environ['HOST']  # Listen on all available network interfaces
    port = os.environ['PORT'] # The port you want to listen on
    server = HTTPServer((host, port), SimpleHTTPRequestHandler)
    print(f"Server started on {host}:{port}")
    logging.info(f"Server started on {host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        print("\nServer stopped.")
        logging.info("Server stopped.")

    # Step 5 Update table at end to say done.
    updateRegister(connection, start_dateTime, logging)

if __name__ == '__main__':
    main()