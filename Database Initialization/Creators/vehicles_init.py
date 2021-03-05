import random
import stations_init

random.seed(3900)
VEHICLES = 60
MAX_COORDINATES = 1000
CLASS_LETTERS = 'ABC'
BRANDS = ["MERCEDES", "MITSUBISHI", "VOLVO", "FORD", "PORSCHE"]
MODELS = ["BA", "BS", "US"]
PLATE_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

insert_str = "INSERT INTO vehicle(license_plate, station_id, brand, model, vehicle_coordinates," + \
    " availability, passengers_number, max_passengers_number, class) VALUES "

STATION_IDS = ["NULL"]
for station in stations_init.stationsDic:
    STATION_IDS.append(station)

vehiclesDic = {}
for i in range(VEHICLES):
    
    letter1 = PLATE_LETTERS[random.randint(0, len(PLATE_LETTERS)-1)]
    letter2 = PLATE_LETTERS[random.randint(0, len(PLATE_LETTERS)-1)]
    letter3 = PLATE_LETTERS[random.randint(0, len(PLATE_LETTERS)-1)]
    num = [str(random.randint(0, 9)) for k in range(4)]
    license_plate = letter1 + letter2 + letter3 + ' ' + ''.join(num)

    if random.random()>0.5:
        station_id = STATION_IDS[random.randint(1, len(STATION_IDS)-1)] + 1
    else:
        station_id = STATION_IDS[0] #50% possibility for NULL

    x = random.randint(0, MAX_COORDINATES) #create a random map position
    y = random.randint(0, MAX_COORDINATES)
    vehicle_coordinates = str(x) + "," + str(y)

    brand = BRANDS[random.randint(0, len(BRANDS)-1)]
    model = MODELS[random.randint(0, len(MODELS)-1)] 
    model2 = model + ' ' + str(random.randint(0, 10000))

    max_passengers_number = 10 * random.randint(4 ,10)
    availability = "true"
    passengers_number = 0
    if station_id=="NULL": #if the vehicle is not in a station, it is not available
        availability = "false"
        passengers_number = random.randint(0, max_passengers_number)
    elif random.randint(0,5) < 3: #if the vehicle is in a station we may decide if it is available or not
        availability =  "false"

    switcher = {MODELS[0]:CLASS_LETTERS[0], MODELS[1]:CLASS_LETTERS[1], MODELS[2]:CLASS_LETTERS[2]}
    vehicle_class = switcher[model]
    
    
    insert_str += "('" + license_plate + "'," + str(station_id) + ",'" + brand + "','" + model2 + "','" + \
       vehicle_coordinates + "'," + availability + "," + str(passengers_number)+ "," + str(max_passengers_number) + \
           ",'" + vehicle_class + "')"

    vehiclesDic[i] = [license_plate,str(station_id),brand,model2,vehicle_coordinates,availability,str(passengers_number),str(max_passengers_number),vehicle_class]
    if (i < VEHICLES - 1): insert_str += ","
    
insert_str += ";"
with open("strings.txt", 'a') as f: f.write("\n\n" + insert_str)

    
    
    
