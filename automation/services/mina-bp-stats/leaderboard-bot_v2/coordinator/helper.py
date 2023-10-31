import psycopg2

ERROR = 'Error: {0}'

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

# def checkPreviousRegister(conn, start_date, end_date, logger):
#     try:
#         cursor = conn.cursor()
#         cursor.execute(
#             f"""SELECT uptime_reports.register(start_date, end_date)
#                 VALUES ({start_date}, {end_date});"""
#                             )
#     except (Exception, psycopg2.DatabaseError) as error:
#         logger.error(ERROR.format(error))
#         return -1
#     finally:
#         cursor.close()

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