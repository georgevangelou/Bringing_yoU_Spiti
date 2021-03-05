import random
import bus_stops_init as bs

random.seed(3900)
MAX_COORDINATES = 1000
LINES = 7


NAMES_EXTRAS = ["(EXPRESS)", ""]
insert_str = "INSERT INTO line(name,start,stop) VALUES "
linesDic = {}

for i in range(LINES):
    while(1):
        k = random.randint(0, bs.BUS_STOPS-1)
        start = bs.bustopsDic[k][1]
        k = random.randint(0, bs.BUS_STOPS-1)
        stop = bs.bustopsDic[k][1]
        if start!=stop: break

    temp_extras = NAMES_EXTRAS.copy()
    for j in range(len(NAMES_EXTRAS) ):
        name = start + " to " + stop + ' ' + temp_extras.pop(random.randint(0, len(temp_extras)-1))
        insert_str += "('" + name + "','" + start + "','" + stop + "')"
        if j != len(NAMES_EXTRAS)-1:
            insert_str += ","
        linesDic[i*len(NAMES_EXTRAS)+j+1] = [name, start, stop]
        
    if (i < LINES - 1): insert_str += ","
    
insert_str += ";"
with open("strings.txt", 'a') as f: f.write("\n\n" + insert_str)



