import tempfile
import csv
import arrow

from dutalib.dbutil import get_db
from dutalib.dbutil import DBSession
from dutalib.config import get_config

MORE_COUNT_TABLE = 'more_count'
BLOGGER_PUBLISHED_TABLE = 'blogger_published'

def get_connection(DB):
    '''
    Gets the curation DB along with cursor object.
    '''
    db = get_db(DB)
    cur = db.cursor()
    return db, cur


def update_published_for_other_events(curation_db, day, type):

    update_query = """
        UPDATE {blogger_published_table} as bp
        SET {event_name} = CAST(mc.event_count AS INTEGER)
        FROM ( SELECT article_hash, sum({event_name}) as event_count 
        FROM more_count
        GROUP BY article_hash
        ) as mc(article_hash, event_count)
        WHERE mc.article_hash = bp.article_hash
        mc.{event_name}
        AND bp.article_hash in ( SELECT article_hash FROM more_count WHERE event_date = '{day}' )
        """.format(blogger_published_table=BLOGGER_PUBLISHED_TABLE, event_name=type, day=day)
    curation_db.execute(update_query)

    pass

def update_other_event_counts(cs, curation_db, day, event_name, type):

    query = """
    select event_timestamp::date, a_articlehash, a_articleid, count(1)
    from event 
    where event_timestamp::date = '{day}'
    and event_type = 'OurUniqueMessageEvent'
    and a_globalid in 
    (select a_globalid 
    from event 
    where event_type='OurMessageEvent' and event_timestamp::date = '{day}' and
    a_localid in 
    (select a_inresponsetomsgid from event 
    where event_type = 'ReplyEvent' and a_message like '{type}' and event_timestamp::date = '{day}') 
    ) group by 2,3,1 ;
    """.format(day=day, type = type)
    cs.execute(query)
    results = []
    for res in cs.fetchall():
        if res[1] is not None:
            hashes = res[1].strip(""" " """).strip(']').strip('[').split(',')
            for hash in hashes:
                row = []
                row.append(res[0])
                row.append(hash.strip(""" "" """))
                row.append(res[2])
                row.append(res[3])
                results.append(row)
                print(row)
    print(len(results))
    csv_file = tempfile.TemporaryFile()
    csv_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_NONE)
    for row in results:
        csv_writer.writerow([row[0], row[1], row[2], row[3]])
    db_conn, c_cur = get_connection('curation')
    csv_file.seek(0)
    c_cur.copy_from(csv_file, "{more_count_table} (event_date, article_hash, more_key_alpha, {event_name})".format(more_count_table=MORE_COUNT_TABLE, event_name=event_name), sep=',')
    csv_file.close()
    db_conn.commit()
    db_conn.close()
    update_published_for_other_events(curation_db, day, type)
    return


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
    # curation_db = DBSession("curation")
    curation_db = ''
    yesterday = arrow.utcnow().shift(days=-1).date()
    update_other_event_counts(cs, curation_db, yesterday, 'liked', '%:thumbs_up:%')
    # update_other_event_counts(cs, curation_db, yesterday, 'disliked', '')

    cs.close()