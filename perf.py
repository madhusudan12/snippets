    
    
    
if __name__ == "__main__":    
    import snowflake.connector
    ctx = snowflake.connector.connect(
    user='psah',
    password='#UP2DUVs',
    account='DUTA',
    )
    cs = ctx.cursor()
    cs.execute("""USE DATABASE DUTAEVENTS""")
    cs.execute("""USE WAREHOUSE CUSTOMLOADER2""")
    cs.execute("""SELECT e1.event_timestamp::date, e1.a_articlehash, e1.a_articleid, count(1)
FROM event e1 
JOIN event e2 ON (e1.a_globalid = e2.a_globalid)
JOIN event e3 ON (e2.a_localid = e3.a_inresponsetomsgid)
WHERE e3.event_type = 'ReplyEvent' 
  AND e3.a_message like '%:thumbs_up:%' 
  AND e3.event_timestamp::date = '2019-05-07'
  AND e2.event_type='OurMessageEvent' 
  AND e2.event_timestamp::date = '2019-05-07'
  AND e1.event_timestamp::date = '2019-05-07'
  AND e1.event_type = 'OurUniqueMessageEvent'
GROUP BY 2,3,1 order by 2;""")

    res1 = cs.fetchall()


    cs.execute("""select event_timestamp::date, a_articlehash, a_articleid, count(1)
    from event 
    where event_timestamp::date = '2019-05-07'
    and event_type = 'OurUniqueMessageEvent'
    and a_globalid in 
    (select a_globalid 
    from event 
    where event_type='OurMessageEvent' and event_timestamp::date = '2019-05-07' and
    a_localid in 
    (select a_inresponsetomsgid from event 
    where event_type = 'ReplyEvent' and a_message like '%:thumbs_up:%' and event_timestamp::date = '2019-05-07') 
    ) group by 2,3,1 order by 2 ;""")

    res2 = cs.fetchall()
    cnt = 0
    for i in range(len(res1)):
        if not res1[i] == res2[i]:
            print(res1[i],res2[i])
            cnt += 1

    print(cnt)
