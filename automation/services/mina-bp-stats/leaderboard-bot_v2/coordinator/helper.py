import psycopg2
from slack import WebClient
from slack.errors import SlackApiError
import os
import boto3
from datetime import datetime, timedelta, timezone
import pandas as pd


ERROR = 'Error: {0}'

def getDefinedMinute(interval, offset, start_dateTime):
    interval_range= list(range(offset, 60, interval))
    smallest_diff = 60
    smallest_candidate = 60
    for candidate in interval_range:
        diff = start_dateTime.minute - candidate
        if diff >0 & diff<smallest_diff:
            smallest_diff - diff
            smallest_candidate = candidate
    return smallest_candidate

def createRegister(conn, start_date, end_date, logger):
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""INSERT INTO uptime_reports.register(start_date, end_date)
                VALUES ({start_date}, {end_date});"""
                            )
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(ERROR.format(error))
        return -1
    finally:
        cursor.close()

def checkPreviousRegister(conn, start_date, logger):
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""SELECT done
                DROM uptime_reports.register
                WHERE end_date = {start_date};"""
                            )
        return cursor.fetchone()[0]
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(ERROR.format(error))
        return -1
    finally:
        cursor.close()

def updateRegister(conn, start_date, logger):
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""UPDATE uptime_reports.register(
                set done = TRUE,
                WHERE start_date = {start_date};"""
                            )
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(ERROR.format(error))
        return -1
    finally:
        cursor.close()

def createSlackPost(token, channel, message):
        client = WebClient(token=token)
        try:
            response = client.chat_postMessage(
            channel=channel,
            text=message)
        except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'

def pullFileNames(start_dateTime, end_dateTime, bucket_name, test=False):
    script_offset = os.path.commonprefix([str(start_dateTime.strftime("%Y-%m-%dT%H:%M:%SZ")), str(end_dateTime.strftime("%Y-%m-%dT%H:%M:%SZ"))])
    prefix_date = start_dateTime.strftime("%Y-%m-%d")
    prefix = None
    if test:
        prefix = 'sandbox/submissions/' + prefix_date + '/' + script_offset
    else:
        prefix = 'submissions/' + prefix_date + '/' + script_offset
    s3 = boto3.resource('s3')
    s3_bucket = s3.Bucket(bucket_name)
    return [f.key for f in s3_bucket.objects.filter(Prefix=prefix).all() if blobChecker(start_dateTime, end_dateTime, f)]

def blobChecker(start_date, end_date, blob):
    file_timestamp = blob.key.split('/')[3].rsplit('-', 1)[0]
    file_epoch = datetime.strptime(file_timestamp,  "%Y-%m-%dT%H:%M:%SZ").timestamp()
    return file_epoch < end_date.timestamp() and (file_epoch >= start_date.timestamp())

def getBatchTimings(conn, logger, interval):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, end_date FROM bot_logs ORDER BY end_date DESC limit 1 ")
        result = cursor.fetchone()
        bot_log_id = result[0]
        prev_epoch = result[1]

        prev_batch_end = datetime.fromtimestamp(prev_epoch, timezone.utc)
        cur_batch_end = prev_batch_end + timedelta(minutes=interval)
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(ERROR.format(error))
        return -1
    finally:
        cursor.close()
    return prev_batch_end, cur_batch_end, bot_log_id

def getPreviousStatehash(conn, logger, bot_log_id):
    cursor = conn.cursor()
    try:
        sql_query = """select  ps.value parent_statehash, s1.value statehash, b.weight
            from bot_logs_statehash b join statehash s1 ON s1.id = b.statehash_id 
		    join statehash ps on b.parent_statehash_id = ps.id where bot_log_id =%s"""
        cursor.execute(sql_query, (bot_log_id,))
        result = cursor.fetchall()

        df = pd.DataFrame(result, columns=['parent_state_hash', 'state_hash', 'weight'])
        previous_result_df = df[['parent_state_hash', 'state_hash']]
        p_selected_node_df = df[['state_hash', 'weight']]
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(ERROR.format(error))
        cursor.close()
        return -1
    finally:
        cursor.close()
    return previous_result_df, p_selected_node_df

def getRelationList(df):
    relation_list = []
    for child, parent in df[['state_hash', 'parent_state_hash']].values:
        if parent in df['state_hash'].values:
            relation_list.append((parent, child))
    return relation_list

def getStatehashDF(conn, logger):
    cursor = conn.cursor()
    try:
        cursor.execute("select value from statehash")
        result = cursor.fetchall()
        state_hash = pd.DataFrame(result, columns=['statehash'])
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(ERROR.format(error))
        return -1
    finally:
        cursor.close()
    return state_hash

def getExistingNodes(conn, logger):
    cursor = conn.cursor()
    try:
        cursor.execute("select block_producer_key from nodes")
        result = cursor.fetchall()
        nodes = pd.DataFrame(result, columns=['block_producer_key'])
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(ERROR.format(error))
        cursor.close()
        return -1
    finally:
        cursor.close()
    return nodes