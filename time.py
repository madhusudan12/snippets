from datetime import datetime
f = open('times.txt',mode='r')
f2 = open('temp.tsv',mode='w')
f2.write("year\tmonth\tbuild_at\tbuild_time")
f2.write("\n")
last_time = datetime.strptime("11:56:48","%H:%M:%S")
year = 2016
month = 1
for line in f.readlines():
    time = line.split()[-2].strip()
    time = datetime.strptime(time,"%H:%M:%S")
    diff_time = time - last_time
    f2.write(str(year) + "\t" + str(month)+ "\t" + str(time).split()[1] + "\t" + str(diff_time))
    f2.write("\n")
    last_time = time
    month = month + 1
    if month > 12 :
        year = year + 1
        month = 1

