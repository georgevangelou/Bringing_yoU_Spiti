from datetime import datetime, timedelta
import random
import lines_init as lines

random.seed(3900)
ITINERARIES = 100
START_HOUR = datetime(year=1,month=1,day=1,hour=6)
END_HOUR = datetime(year=1,month=1,day=1,hour=23)

MINUTE_INTERVALS_WEEKDAYS = [30, 60, 120]
MINUTE_INTERVALS_WEEKENDS = [60, 120, 180]
MINUTE_INTERVALS_HOLIDAYS = [120, 180, 240, 300]
MINUTE_INTERVALS = [MINUTE_INTERVALS_WEEKDAYS,
                    MINUTE_INTERVALS_WEEKENDS,
                    MINUTE_INTERVALS_HOLIDAYS]

TYPE = ["WEEKDAYS", "WEEKENDS", "HOLIDAY"]

insert_str = "INSERT INTO itinerary(line_id,start,type) VALUES "

itinerariesDic = {}
i=1
for line in lines.linesDic:
    for j in range(len(MINUTE_INTERVALS)):
        current_time = START_HOUR
        interval = MINUTE_INTERVALS[j][random.randint(0,len(MINUTE_INTERVALS[j])-1)]
        while current_time < END_HOUR:
            insert_str += "(" + str(line) + ",'" + str(current_time.time())\
            + "','" + TYPE[j] + "'),"
            itinerariesDic[i] = [line, current_time]
            i += 1
            current_time += timedelta(minutes=interval)
    
insert_str = insert_str[:-1]
insert_str += ";"
with open("strings.txt", 'a') as f: f.write("\n\n" + insert_str)
