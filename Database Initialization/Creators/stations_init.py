import random

random.seed(3900)
MAX_COORDINATES = 1000
NAMES = ["Psarofai", "Ities", "Aroi", "Kentrikos"]
STATIONS = len(NAMES)

MIN_CAPACITY = 10
MAX_CAPACITY = 100

insert_str = "INSERT INTO station(station_coordinates, name, capacity) VALUES "
stationsDic = {}
for i in range(STATIONS):
    x = random.randint(0, MAX_COORDINATES) #create a random map position
    y = random.randint(0, MAX_COORDINATES)
    station_coordinates = str(x) + "," + str(y)
    name = NAMES.pop(random.randint(0,len(NAMES)-1))
    capacity = random.randint(MIN_CAPACITY,MAX_CAPACITY)

    stationsDic[i] = [station_coordinates,name,capacity]
    
    insert_str += "('" + station_coordinates + "','" + name + "'," + str(capacity) + ")"
    
    if (i < STATIONS - 1): insert_str += ","
    
insert_str += ";"
with open("strings.txt", 'a') as f: f.write("\n\n" + insert_str)

    
    
    
