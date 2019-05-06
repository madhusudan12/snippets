import tempfile
import csv
from dutalib.dbutil import get_db

MORE_COUNT_TABLE = 'more_count'


def get_connection(DB):
    '''
    Gets the curation DB along with cursor object.
    '''
    db = get_db(DB)
    cur = db.cursor()
    return db, cur


def update_other_event_counts(cs, curation_db, event_name):
    query = """
    select event_timestamp::date, a_articlehash, a_articleid, count(1)
    from event 
    where event_timestamp::date = '2019-05-05'
    and event_type = 'OurUniqueMessageEvent'
    and a_globalid in 
    (select a_globalid 
    from event 
    where event_type='OurMessageEvent' and event_timestamp::date = '2019-05-05' and
    a_localid in 
    (select a_inresponsetomsgid from event 
    where event_type = 'ReplyEvent' and a_message like '%:thumbs_up:%' and event_timestamp::date = '2019-05-05') 
    ) group by 2,3,1 ;
    """
    cs.execute(query)
    results = []
    for res in cs.fetchall():
        row = []
        row.append(res[0])
        if res[1] is not None:
            row.append(res[1].strip(""" " """).strip(']').strip('[').split(',')[0].strip(""" "" """))
        else:
            row.append(res[1])
        row.append(res[2])
        row.append(res[3])
        results.append(row)
    csv_file = tempfile.TemporaryFile()
    csv_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_NONE)
    for row in results:
        csv_writer.writerow([row[0], row[1], row[2], row[3]])
    db_conn, c_cur = get_connection('curation')
    csv_file.seek(0)
    c_cur.copy_from(csv_file, "{more_count_table} (event_date, article_hash, more_key_alpha, {event_name})".format(more_count_table=MORE_COUNT_TABLE, event_name=event_name), sep=',')
    
    return results


if __name__=="__main__":
    import snowflake.connector
    ctx = snowflake.connector.connect(
    user='psah',
    password='#UP2DUVs',
    account='DUTA',
    )
    cs = ctx.cursor()
    cs.execute("""USE DATABASE DUTAEVENTS""")
    cs.execute("""USE WAREHOUSE CUSTOMLOADER2""")
    sync(cs)
    cs.close()