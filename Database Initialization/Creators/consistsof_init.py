import random
random.seed(3900)

import bus_stops_init
STOPS = bus_stops_init.BUS_STOPS
stopsDic = bus_stops_init.bustopsDic

import lines_init
SIZE = lines_init.LINES
linesDic = lines_init.linesDic
EXTRAS = lines_init.NAMES_EXTRAS



def getRandStop(currentStops, finalStop):
    newStop = random.randint(1, STOPS)
    while ((newStop in currentStops) or (newStop==finalStop)):
        newStop = random.randint(1, STOPS)
    return newStop


STOPS_PER_LINE = [15, 25]

#insert_str = "INSERT INTO consists_of(line_id, bus_stop_id, i/i, eta_from_itinerary_start) VALUES "
insert_str = "INSERT INTO consists_of(line_id, bus_stop_id, sequence_index) VALUES "
conofDic = {}
for i in range(SIZE):

    initialStop_Name = linesDic[i*len(EXTRAS)+1][1]
    finalStop_Name   = linesDic[i*len(EXTRAS)+1][2]

    initialStop = -1
    finalStop = -1
    for k in range(STOPS):
        if stopsDic[k][1]==initialStop_Name:
            initialStop = k+1
        elif stopsDic[k][1]==finalStop_Name:
            finalStop = k+1
    
    stops_of_line = [initialStop]
    NormLineSize = random.randint(STOPS_PER_LINE[0], STOPS_PER_LINE[1])
    ExprLineSize = random.randint(int(NormLineSize/4), int(NormLineSize/2))

    for j in range(NormLineSize-2): #NORMAL LINE
        stops_of_line.append(getRandStop(stops_of_line, finalStop))
    stops_of_line.append(finalStop) 

    stops_of_express = stops_of_line.copy()
    for j in range(NormLineSize-ExprLineSize): #EXPRESS LINE
        removed = random.randint(1, len(stops_of_express)-2)
        stops_of_express.pop(removed)


    #(line_id, bus_stop_id, i/i, eta_from_itinerary_start)
    conofDic[1+i*len(EXTRAS) + 0] = [[],[],[]] #[line] --> [[stops], [i/i], [eta]]
    conofDic[1+i*len(EXTRAS) + 1] = [[],[],[]] #[line] --> [[stops], [i/i], [eta]]

    for w in range(len(stops_of_express)):
        insert_str += "(" + str(1 + i*len(EXTRAS) + 0) + "," + str(stops_of_express[w]) + "," + str(1 + w) + ")," #MHPWS NA MHN EXOUME NULL TA ETAs ?
        conofDic[1+i*len(EXTRAS) + 0][0].append(stops_of_express[w])
        conofDic[1+i*len(EXTRAS) + 0][1].append(w)

    for w in range(len(stops_of_line)):
        insert_str += "(" + str(1 + i*len(EXTRAS) + 1) + "," + str(stops_of_line[w]) + "," + str(1 + w) + "),"
        conofDic[1+i*len(EXTRAS) + 1][0].append(stops_of_line[w])
        conofDic[1+i*len(EXTRAS) + 1][1].append(w)


insert_str = insert_str[:-1] + ";"
with open("strings.txt", 'a') as f: f.write("\n\n" + insert_str)



    
