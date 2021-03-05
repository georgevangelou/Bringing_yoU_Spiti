import random
import drivers_init, vehicles_init, lines_init, itineraries_init

def randomItem(lista):
    length = len(lista)
    return lista[random.randint(0,length-1)]


def canDrive(dr_id, c_id):
    diploma = drivers_init.driversDic[dr_id][2]
    classh =  vehicles_init.vehiclesDic[c_id][-1]
    if   diploma=='C': return True
    elif classh=='C':  return False
    elif diploma=='B': return True
    elif classh=='B':  return False
    return True



random.seed(3900)
insert_str = "INSERT INTO executes(license_plate, itinerary_id, line_id, driver_id) VALUES "
execDic = {}

start_time = 0
end_time = 0


vehicle_plates = [vehicles_init.vehiclesDic[kappa][0] for kappa in vehicles_init.vehiclesDic.keys()]
vehicle_class = [vehicles_init.vehiclesDic[kappa][-1] for kappa in vehicles_init.vehiclesDic.keys()]

driver_ids = [kappa for kappa in drivers_init.driversDic.keys()]
driver_class = [drivers_init.driversDic[kappa][2] for kappa in drivers_init.driversDic.keys()] #get the license degree of each driver
EXECUTIONS = 49

for i in range(EXECUTIONS):
    
    itinId = 10*i+1    #get an itinerary's id
    line_id = itineraries_init.itinerariesDic[itinId][0]    #get the line of the itinerary

    lic_plate = randomItem(vehicle_plates)   #get a vehicle's license plate
    driver_id = randomItem(driver_ids)  #get the id of a driver
    car_id = vehicle_plates.index(lic_plate)

    while (canDrive(driver_id, car_id)==False):
        lic_plate = randomItem(vehicle_plates)   #get a vehicle's license plate
        driver_id = randomItem(driver_ids)  #get the id of a driver
        car_id = vehicle_plates.index(lic_plate)
    
    
    vehicle_class.pop(vehicle_plates.index(lic_plate)); vehicle_plates.remove(lic_plate)
    driver_class.pop(driver_ids.index(driver_id)); driver_ids.remove(driver_id)

    insert_str += "('" + str(lic_plate) + "'," + str(itinId) + "," + str(line_id) + ",'"  + str(driver_id) + "')"

    if (i < EXECUTIONS - 1): insert_str += ","
    
insert_str += ";"
with open("strings.txt", 'a') as f: f.write("\n\n" + insert_str)


