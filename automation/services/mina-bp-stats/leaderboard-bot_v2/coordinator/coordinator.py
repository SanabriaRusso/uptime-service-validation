import os
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from kubernetes import client, config
from server import SimpleHTTPRequestHandler
from helper import updateRegister, pullFileNames, getBatchTimings, getRelationList, getPreviousStatehash, getStatehashDF, getExistingNodes
from datetime import datetime, timedelta, timezone
import psycopg2
from dotenv import load_dotenv
import boto3
import pandas as pd

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

    # Step 1 Get previous record and build relations list
    interval = os.environ['SURVEY_INTERVAL_MINUTES']
    prev_batch_end, cur_batch_end, bot_log_id = getBatchTimings(connection, logging, interval)
    cur_timestamp = datetime.now(timezone.utc)
    relation_df, p_selected_node_df = getPreviousStatehash(bot_log_id)
    p_map = getRelationList(relation_df)

    logging.info("script start at {0}  end at {1}".format(prev_batch_end, cur_timestamp))
    
    existing_state_df = getStatehashDF(connection, logging)
    existing_nodes = getExistingNodes(connection, logging)
    logging.info('running for batch: {0} - {1}'.format(prev_batch_end, cur_batch_end))
    script_offset = os.path.commonprefix([str(prev_batch_end.strftime("%Y-%m-%dT%H:%M:%SZ")),
                                            str(cur_batch_end.strftime("%Y-%m-%dT%H:%M:%SZ"))])
    if cur_batch_end > cur_timestamp:
        logging.info('all files are processed till date')
        return
    else:
        master_df = pd.DataFrame() 
        state_hash_df = pd.DataFrame() 
    
        # Step 2 Pull down list of files (not necessarily the files themselves)
        bucket= os.environ["BUCKET_NAME"]
        files_in_s3 = pullFileNames(prev_batch_end,cur_batch_end, bucket)
        mini_batches = [files_in_s3[i::os.environ['MINI_BATCH_NUMBER']] for i in range(os.environ['MINI_BATCH_NUMBER'])]

        # Step 3 Create Kubernetes ZKValidators
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

        # Step 4 Update table at end to say done.
        updateRegister(connection, prev_batch_end, logging)

if __name__ == '__main__':
    main()