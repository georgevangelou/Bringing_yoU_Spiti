import random

random.seed(3900)
MAX_COORDINATES = 1000
BUS_STOPS = 60
DIFFERENT = 3

NAMES = ["Square", "Stadium", "Bridge", "Washington", "Pool", "Road",
         "Highway to bell", "KYPES", "Circus", "Church", "Town Hall",
         "Zoo", "Pasalimani", "Tsoukaleika", "Vraxneika", "Kallithea",
         "Summoners Rift", "Mordor", "Minas Tirith", "Gondor", "Durotar",
         "Duskwood", "Westfall", "Helms Deep", "Moria", "Icecrown",
         "Dalaran", "Isenstar", "Kineta"]
ZONES = [1, 2, 3]


insert_str = "INSERT INTO bus_stop(bus_stop_coordinates,name,zone) VALUES "
bustopsDic = {}
insertedDic = {}
for i in range(BUS_STOPS):
    x = random.randint(0, MAX_COORDINATES) #create a random map position
    y = random.randint(0, MAX_COORDINATES)
    coor = str(x) + "," + str(y)

    n1 = random.randint(0,len(NAMES)-1) #create a random name (2-parts)
    n2 = random.randint(1,DIFFERENT)
    name = NAMES[n1] + " " + str(n2)
    while name in insertedDic:
        n1 = random.randint(0,len(NAMES)-1) #create a random name (2-parts)
        n2 = random.randint(1,DIFFERENT)
        name = NAMES[n1] + " " + str(n2)
    
    insertedDic[name] = 1
    
    z = random.randint(0,len(ZONES)-1) #pick a random zone 
    zone = ZONES[z]
    
    insert_str += "('" + coor + "','" + name + "'," + str(zone) + ")"
    bustopsDic[i] = [coor, name, zone]
    if (i < BUS_STOPS - 1): insert_str += ","
    
insert_str += ";"

with open("strings.txt", 'a') as f: f.write("\n\n" + insert_str)



