import random
from itineraries_init import itinerariesDic #lines in itineraries
from lines_init import LINES, NAMES_EXTRAS
from consistsof_init import conofDic
from datetime import datetime, timedelta

random.seed(3900)

HISTORIES_PER_LINE = 25
insert_str = "INSERT INTO line_history(line_id,bus_stop_id,itinerary_id, arrival) VALUES "
lineHistDic = {}
used_itineraries = []
counter = 1
for line in range(1, LINES*len(NAMES_EXTRAS)):
    for history in range(HISTORIES_PER_LINE):
        itinerary = random.randint(1, max(itinerariesDic.keys()))
        while ((itinerary in used_itineraries) or (line != itinerariesDic[itinerary][0]) ):
            itinerary = random.randint(1, max(itinerariesDic.keys()))
        used_itineraries.append(itinerary)
        ctime = itinerariesDic[itinerary][1]

        for i in range(len(conofDic[line][0])): #conofDic: [line] --> [[stops], [i/i], [eta]]
            stop = conofDic[line][0][i]
            ctime += timedelta(minutes=random.randint(1,10))
            
            lineHistDic[counter] = [line, stop, itinerary, ctime] 
            #lineHistDic: index --> [line, stop, itin, ctime]
            counter += 1

            insert_str += "(" + str(line) + "," + str(stop) + "," + str(itinerary) \
                + ",'" + str(ctime.time()) + "'),"

insert_str = insert_str[:-1] + ";"
with open("strings.txt", 'a') as f: f.write("\n\n" + insert_str)



