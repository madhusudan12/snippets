import arrow
last_group_reset_time=arrow.utcnow()
last_log_time = arrow.utcnow()
groups=set()

else:
groups.add(message_payload['group_id'])
current_time = arrow.utcnow()
time_diff = (current_time - last_log_time).seconds
reset_time_diff = (current_time - last_group_reset_time).seconds
if time_diff >= 3600:
    diff_hours = reset_time_diff // 3600
    log.info("skipping {0} groups from past {1} hours".format(len(groups), reset_time_diff))
    last_log_time = current_time
    if diff_hours >= 24:
        groups.clear()
        last_group_reset_time = current_time


def receive_read_receipt_message(topics, partition):

    topics = ["events_"+topic for topic in topics]
    workers_cache = get_workers_cache()
    consumer = get_consumer(topics, partition)

    start_tick = arrow.utcnow()
    last_group_reset_time=arrow.utcnow()
    last_log_time = arrow.utcnow()
    groups=set()
    while True:
        for msg in consumer:
            try:
                message_payload = json.loads(msg.value)
            except:
                log.error("Skipping read receipt payload: %s", msg.value)
                continue

            if (arrow.utcnow()-start_tick).seconds >= 2*60*60:
                workers_cache = get_workers_cache()
                start_tick = arrow.utcnow()

            if within_time_window(message_payload.get('t', None)):
                if message_payload['participant'] in workers_cache:
                    continue
                if group_cache.add(EVENT_PREFIX+message_payload['group_id'], "", ttl=seconds_to_utc_0000()):
                    if user_cache.add(user_key_prefix+message_payload['participant'], "", ttl=seconds_to_utc_0000()):
                        process_message(message_payload)
            else:
                groups.add(message_payload['group_id'])
                current_time = arrow.utcnow()
                time_diff = (current_time - last_log_time).seconds
                reset_time_diff = (current_time - last_group_reset_time).seconds
                if time_diff >= 3600:
                    diff_hours = reset_time_diff // 3600
                    log.info("skipping {0} groups from past {1} hours".format(len(groups), reset_time_diff))
                    last_log_time = current_time
                    if diff_hours >= 24:
                        groups.clear()
                        last_group_reset_time = current_time








