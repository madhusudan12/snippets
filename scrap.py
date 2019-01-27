import time
import datetime
import arrow
import logging
def func():
    print("before")
    time.sleep(10)
    print('after')

# d1=arrow.utcnow()
# func()
# d2=arrow.utcnow()
# print((d2-d1).seconds)
#
log=logging.getLogger(__name__)


a=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]


last_group_reset_time=arrow.utcnow()
last_log_time = arrow.utcnow()
groups=set()
while True:
    for i in range(30):
        if i%2 == 0:
            pass
        else:
            groups.add(a[i])
            current_time = arrow.utcnow()
            time_diff = (current_time - last_log_time).seconds
            reset_time_diff = (current_time - last_group_reset_time).seconds
            if time_diff >= 60 :
                diff_hours = reset_time_diff // 60
                print ("skipping {0} groups from past {1} hours".format(len(groups), diff_hours))
                last_log_time = current_time
                if diff_hours >= 3:
                    groups.clear()
                    print('this should be empty as one day completed')
                    print(groups)
                    last_group_reset_time = current_time
