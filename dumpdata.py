from datetime import date, timedelta

import snowflake.connector as sf

EVENT_TABLE = 'event_test'
DUTA_POINTS_DAILY_USER_TABLE = 'duta_points_daily_users_test'
DUTA_POINTS_WEEKLY_USER_TABLE = 'duta_points_weekly_users_test'
DAILY_ACTIVE_GROUPS_TABLE='daily_active_groups_test'
yesterday = date.today()-timedelta(1)


def dump_daily_duta_points_table(sf_conn):

    try:
        with sf_conn.cursor() as cur:
            fetch_query = "SELECT date FROM {0} WHERE date=%s".format(DUTA_POINTS_DAILY_USER_TABLE)
            cur.execute(fetch_query, (yesterday,))
            result = cur.fetchall()
            if result and len(result):
                msg = "Data of the day {0} is inserted in table {1} already".format(yesterday, DUTA_POINTS_DAILY_USER_TABLE)
                print(msg)
            else:
                query = """
                INSERT INTO {0}(date,user_count,messages_count) 
                SELECT event_timestamp::date, COUNT(DISTINCT a_fromphonenumber), COUNT(*)
                FROM {1} 
                WHERE (event_type='PointsMsgStarEvent' OR event_type='PointsMsgReadReceipt') AND event_timestamp::date = %s 
                GROUP BY event_timestamp::date; 
                """.format(DUTA_POINTS_DAILY_USER_TABLE, EVENT_TABLE)
                rows = cur.execute(query, (yesterday,))
                sf_conn.commit()
                if rows.rowcount == 0:
                    msg = "There is no daily duta points data found on {0}".format(yesterday)
                else:
                    msg = "Downloaded records of the day {0} from snowflake and inserted into table {1}".format(yesterday, DUTA_POINTS_DAILY_USER_TABLE)
                print(msg)
    except Exception as e:
        msg = "Failed while fetching or inserting the data. Got exception {}".format(e)
        print(msg)
        return False


def dump_weekly_duta_points_table(sf_conn):

    try:
        with sf_conn.cursor() as cur:
            fetch_query = "SELECT date FROM {0} WHERE date=%s".format(DUTA_POINTS_WEEKLY_USER_TABLE)
            cur.execute(fetch_query, (yesterday,))
            result = cur.fetchall()
            if result and len(result):
                msg = "Data of the day {0} is inserted in table {1} already".format(yesterday, DUTA_POINTS_WEEKLY_USER_TABLE)
                print(msg)
            else:
                query = """
                INSERT INTO {0} (date,user_count,messages_count) 
                SELECT  event_timestamp::date, COUNT(DISTINCT a_fromphonenumber), COUNT(*) 
                FROM {1}
                WHERE (event_type='WeeklyDigestMsgStarEvent' OR event_type='WeeklyDigestMsgReadReceipt') 
                AND event_timestamp::date = %s 
                GROUP BY event_timestamp::date;
                """.format(DUTA_POINTS_WEEKLY_USER_TABLE, EVENT_TABLE)
                sf_conn.commit()
                rows = cur.execute(query, (yesterday,))
                if rows.rowcount == 0:
                    msg = "No weekly Digest message sent for the users on {0}".format(yesterday)
                else:
                    msg = "Downloaded records of the day {0} from snowflake and inserted into table {1}".format(yesterday, DUTA_POINTS_WEEKLY_USER_TABLE)
                print(msg)
    except Exception as e:
        msg = "Failed while fetching or inserting the data. Got exception {}".format(e)
        print(msg)
        return False


def dump_daily_active_groups_data(sf_conn):
    try:
        with sf_conn.cursor() as cur:
            fetch_query = "SELECT date FROM {0} WHERE date=%s".format(DAILY_ACTIVE_GROUPS_TABLE)
            cur.execute(fetch_query, (yesterday,))
            result = cur.fetchall()
            if result and len(result):
                msg = "daily active groups data on {0} is already inserted in table {1}".format(yesterday, DAILY_ACTIVE_GROUPS_TABLE)
                print(msg)
            else:
                query = """
                INSERT INTO {0}(date,active_groups_count)
                SELECT event_timestamp::date, COUNT(DISTINCT a_groupid)
                FROM {1}
                WHERE event_type='MessageReadReceipt' AND event_timestamp::date = %s
                GROUP BY event_timestamp::date;
                """.format(DAILY_ACTIVE_GROUPS_TABLE, EVENT_TABLE)
                sf_conn.commit()
                rows = cur.execute(query, (yesterday,))
                if rows.rowcount == 0:
                    msg = "There are no records found for daily active groups on {0}".format(yesterday)
                else:
                    msg = "Downloaded records of the day {0} from snowflake and inserted into table {1}".format(yesterday, DAILY_ACTIVE_GROUPS_TABLE)
                print(msg)
    except Exception as e:
        msg = "Failed while fetching or inserting the data. Got exception {}".format(e)
        print(msg)
        return False


if __name__ == '__main__':
    try:
        sf_conn = sf.connect(user='subash', password='310766Anju', account='DUTA')
        sf_conn.cursor().execute("USE warehouse CUSTOMLOADER2")
        sf_conn.cursor().execute("USE DUTAEVENTS")
    except Exception as e:
        msg = "Cannot open snowflake Got exception {}".format(e)
        sf_conn.close()
        print(msg)
    dump_daily_duta_points_table(sf_conn)
    dump_weekly_duta_points_table(sf_conn)
    dump_daily_active_groups_data(sf_conn)
    sf_conn.close()

