############################  USED LIBRARIES  ############################

import math
import datetime
import functions as f
from operator import itemgetter
from constants import DEBUG



############################  QUERIES  ############################

def get_BusStop_Statistical_TimefromStart(mycursor, bus_stop_id, day_type):
    '''
    stored_TFSs = [line_id, average_time_from_start] \n
    Returns the average time from the start of the itinerary (in minutes) for a bus stop for all lines but a specified day type
    '''

    myquery  = "SELECT i.line_id, AVG(TIME_TO_SEC(subtime(h.arrival, i.start))/60) AS TFS "
    myquery += "FROM line_history h JOIN itinerary i ON h.itinerary_id=i.itinerary_id JOIN line l ON i.line_id=l.line_id JOIN bus_stop b ON h.bus_stop_id=b.bus_stop_id "
    myquery += "WHERE b.bus_stop_id={} AND i.type='{}' AND subtime(h.arrival, i.start)>0 GROUP BY l.line_id ORDER BY TFS".format(str(bus_stop_id), day_type)
    mycursor.execute(myquery)
    myresult = mycursor.fetchall()
    return myresult


def get_BusStop_Statistical_ETAs(mycursor, bus_stop_id, current_time, day_type):
    '''
    etas = [line_id, eta] \n
    Returns the current estimated ETAs for all lines in a bus stop
    ETAs are filtered so that they are in a [0, +oo) minutes domain
    '''
    
    # Pairnoume ola ta itineraries twn grammwn pou pernane apo edw shmera pou exoun ksekinisei prin apo twra
    myquery  = "SELECT i.itinerary_id, i.start, i.line_id FROM itinerary i JOIN consists_of con ON i.line_id=con.line_id "
    myquery += "WHERE i.start<'{}' AND i.type='{}' AND con.bus_stop_id={}".format(current_time, day_type, bus_stop_id)
    mycursor.execute(myquery) 
    current_Itins_Starts_Lines = mycursor.fetchall()

    #line_id, average time from start of all itineraries
    stored_Line_AvTime = get_BusStop_Statistical_TimefromStart(mycursor, bus_stop_id, day_type)
    incoming_buses = []
    for i in range(len(current_Itins_Starts_Lines)): #gia kathe itinerary pou pernaei apo ti stash
        for j in range(len(stored_Line_AvTime)): #vres ena stored average eta pou na tou antistoixei (idia stash)
            if current_Itins_Starts_Lines[i][2]==stored_Line_AvTime[j][0]:
                line_id = stored_Line_AvTime[j][0]
                start = current_Itins_Starts_Lines[i][1]
                mins_from_start = datetime.timedelta(minutes=float(stored_Line_AvTime[j][1]))
                arrival = start + mins_from_start
                try:
                    eta = datetime.datetime.strptime(str(arrival), '%H:%M:%S.%f') - datetime.datetime.strptime(str(current_time), '%H:%M:%S.%f')
                    eta = int(round(eta.total_seconds()/60))
                except:
                    try:
                        eta = datetime.datetime.strptime(str(arrival), '%H:%M:%S') - datetime.datetime.strptime(str(current_time), '%H:%M:%S.%f')
                        eta = int(round(eta.total_seconds()/60))
                    except:
                        if DEBUG: print("Both failed")
                        eta = -1
                if eta >= 0: 
                    if DEBUG:
                        print("From line: ", line_id)
                        print("Start is: ", start)
                        print("Mins from start is: ", mins_from_start)
                        print("Arrival time is: ", arrival)
                        print("Current time is: ", current_time)
                        print("ETA is: ", eta)
                        print()
                    incoming_buses.append([line_id, eta])    
    return incoming_buses


def get_Line_Itineraries(mycursor, line_id, day_type):
    '''
    line_itins = [itin_id, start_time]\n
    Returns the specified line's itineraries of a specific day type\n
    '''

    myquery  = "SELECT i.itinerary_id, i.start FROM itinerary i WHERE i.line_id={} AND i.type='{}'".format(line_id, day_type)
    mycursor.execute(myquery) 
    line_itins = mycursor.fetchall()
    return line_itins


def get_BusStop_Id(mycursor, bus_stop_name):
    '''
    bus_stop_id = [id]\n
    Returns the specified bus stop's id
    '''

    myquery  = "SELECT bus_stop_id FROM bus_stop WHERE name='{}'".format(bus_stop_name)
    mycursor.execute(myquery) 
    bus_stop_id = mycursor.fetchall()
    return bus_stop_id


def get_Line_Timetable(mycursor, line_id, day_type):
    '''
    line_info = [line_id, name, start, stop]\n
    line_itins = [[itin_id, start_time, end_time]]\n
    Returns the specified line's timetable of a specific day type\n
    '''

    line_info = get_Line_Information(mycursor, line_id)
    line_itins = [list(t) for t in get_Line_Itineraries(mycursor, line_id, day_type)]
    last_stop_name = line_info[3]
    last_stop_id = get_BusStop_Id(mycursor, last_stop_name)[0][0]
    tfs_to_last_stop = get_BusStop_Statistical_TimefromStart(mycursor, last_stop_id, day_type)[0][1]
    if DEBUG:
        print("tfs_to_last_stop: {}".format(tfs_to_last_stop))
    for i in range(len(line_itins)):
        end_time = line_itins[i][1] + datetime.timedelta(minutes=int(round(tfs_to_last_stop)))
        line_itins[i].append(end_time)

    return line_info, line_itins


def get_BusStop_Lines(mycursor, bus_stop_id):
    '''
    Returns all lines that stop at a specific bus stop
    '''

    myquery  = "SELECT l.line_id FROM consists_of con WHERE con.bus_stop_id={}".format(bus_stop_id)
    mycursor.execute(myquery)
    myresult = mycursor.fetchall()
    myresult = [b for a in myresult for b in a]
    return myresult


def get_Line_Bus_Coordinates(mycursor, line_id):
    '''
    Returns the coordinates of all buses currently executing itineraries for a specific line
    '''

    myquery = "SELECT v.license_plate as `BUS_ID`, v.vehicle_coordinates AS `BUS_POSITION` FROM vehicle v JOIN executes e ON v.license_plate=e.license_plate JOIN line l ON e.line_id=l.line_id " \
                + "WHERE l.line_id={}".format(line_id)
    mycursor.execute(myquery)
    myresult = mycursor.fetchall()
    return myresult


def get_Line_Information(mycursor, line_id):
    '''
    line_info = [line_id, line_name, start, stop] \n
    Returns all information about a line
    '''

    myquery  = "SELECT l.line_id, l.name, l.start, l.stop FROM line l WHERE l.line_id='{}'".format(str(line_id))
    mycursor.execute(myquery)
    line_info = mycursor.fetchall()[0]
    return line_info


def get_All_Lines_Information(mycursor):
    '''
    lines_info = [line_id, line_name, start, stop] \n
    Returns all information about all lines
    '''

    myquery  = "SELECT l.line_id, l.name, l.start, l.stop FROM line l"
    mycursor.execute(myquery)
    lines_info = mycursor.fetchall()
    return lines_info


def get_Line_Name(mycursor, line_id):
    '''
    Returns the name of a line
    '''

    myquery = "SELECT name FROM line WHERE line_id={}".format(str(line_id))
    mycursor.execute(myquery)
    myresult = mycursor.fetchall()
    return myresult


def get_Cardholders_Information(mycursor, cardholder_id):
    '''
    Returns all information concerning a specific cardholder
    '''

    myquery = "SELECT * FROM `cardholder` WHERE cardholder_id='{}'".format(cardholder_id)
    mycursor.execute(myquery)
    myresult = mycursor.fetchall()
    return myresult


def get_Cards_Status(mycursor, card_id, current_date, current_zone=-1):
    '''
    result = [isValid, notes] \n
    Returns true only if specified card is time and zone eligible
    '''

    myquery  = "SELECT c.cardholder_id, c.name, c.surname, r.start_date, r.expiration_date, z.zone_id FROM cardholder c JOIN route_card r ON c.cardholder_id=r.cardholder_id "
    myquery += "JOIN zones z ON r.card_id=z.card_id WHERE r.card_id='{}'".format(card_id)
    mycursor.execute(myquery)
    myresult = mycursor.fetchall()
    start_date = myresult[0][3]
    expiration_date = myresult[0][4]
    zones = [i[5] for i in myresult]
    if current_date<start_date or current_date>expiration_date: 
        return False, "Expired", zones
    if current_zone>=0: 
        if (current_zone not in zones): 
            return False, "Non-eligible for current zone", zones
    return True, "Valid", zones


def get_Closest_BusStops(mycursor, personCoordinates, maxDist=100, line_id=-1):
    '''
    nearest_stops = [[stop_id, stop_name, distance]]\n
    Returns id, names and distance of nearest bus stops
    '''

    myquery  = "SELECT s.bus_stop_id as BUS_STOP_ID, s.name as BUS_STOP_NAME, s.bus_stop_coordinates as BUS_STOP_COORDINATES FROM bus_stop s "
    if (line_id>0): myquery += "JOIN consists_of co ON s.bus_stop_id=co.bus_stop_id WHERE co.line_id={}".format(line_id)
    mycursor.execute(myquery)
    myresult = mycursor.fetchall()
    nearest_stops = []
    for bus_stop in myresult:
        stop_id = bus_stop[0]
        stop_name = bus_stop[1]
        stop_coordinates = bus_stop[2].split(",")
        stop_x = int(stop_coordinates[0])
        stop_y = int(stop_coordinates[1])
        person_x = personCoordinates[0]
        person_y = personCoordinates[1]
        distance = math.sqrt( (stop_x-person_x)**2 + (stop_y-person_y)**2 )
        if distance<maxDist: 
            nearest_stops.append([stop_id, stop_name, distance])
    return sorted(nearest_stops, key = itemgetter(2))


def create_New_Card(mycursor, cardholder_id, start_date, card_duration, zones):
    '''
    Creates a new card 
    '''

    myquery  = "SELECT c.card_id FROM route_card c WHERE c.cardholder_id='{}' ".format(cardholder_id)
    mycursor.execute(myquery)
    mycursor.fetchall()
    if mycursor.rowcount>0 and DEBUG:
        print("Cardholder already posseses a card.") 
        return
    myquery  = "SELECT h.cardholder_id, h.status FROM cardholder h WHERE h.cardholder_id='{}'".format(cardholder_id)
    mycursor.execute(myquery)
    myresult = mycursor.fetchall()
    cardholder_type = myresult[0][1]
    expiration_date = str(datetime.datetime.strptime(start_date,  '%Y-%m-%d %H:%M:%S') + datetime.timedelta(days = card_duration*30))
    discount_type, value = f.get_Card_Value(cardholder_type, card_duration)
    myquery  = "INSERT INTO route_card(cardholder_id,start_date,expiration_date,value,discount_type) "
    myquery += "VALUES ('{}', '{}', '{}', '{}', '{}')".format(cardholder_id, start_date, expiration_date, value, discount_type)
    mycursor.execute(myquery)

    myquery  = "SELECT c.card_id FROM route_card c WHERE c.cardholder_id='{}'".format(cardholder_id)
    mycursor.execute(myquery)
    myresult = mycursor.fetchall()
    card_id = myresult[0][0]
    create_Zones(mycursor, card_id, zones)
    return card_id


def create_Zones(mycursor, card_id, zones):
    '''
    Deletes existing zones of a card and creates new
    '''

    myquery  = "DELETE FROM zones WHERE card_id={}".format(card_id)
    mycursor.execute(myquery)
    for zone in zones:
        myquery  = "INSERT INTO zones(zone_id,card_id) VALUES({},{})".format(zone, card_id)
        mycursor.execute(myquery)
    return


def renew_Card(mycursor, card_id, start_date, card_duration, zones):
    '''
    Renews a card status of an existing cardholder
    '''

    myquery  = "SELECT h.cardholder_id, h.status FROM cardholder h JOIN route_card r ON h.cardholder_id=r.cardholder_id WHERE r.card_id={}".format(card_id)
    mycursor.execute(myquery)
    myresult = mycursor.fetchall()
    cardholder_type = myresult[0][1]
    expiration_date = str(datetime.datetime.strptime(start_date,  '%Y-%m-%d %H:%M:%S') + datetime.timedelta(days = card_duration*30))
    discount_type, value = f.get_Card_Value(cardholder_type, card_duration)
    myquery  = "UPDATE route_card c SET c.start_date="
    myquery += "'{}', c.expiration_date='{}', c.value={}, c.discount_type={} WHERE c.card_id={}".format(start_date, expiration_date, value, discount_type, card_id)
    mycursor.execute(myquery)
    create_Zones(mycursor, card_id, zones)
    return


def create_New_Cardholder(mycursor, cardholder_id, name, surname, status):
    '''
    Creates a new cardholder
    '''

    myquery  = "SELECT h.cardholder_id FROM cardholder h WHERE h.cardholder_id='{}' ".format(cardholder_id)
    mycursor.execute(myquery)
    mycursor.fetchall()
    if mycursor.rowcount>0:
        print("Cardholder already exists.") 
        return
    myquery  = "INSERT INTO cardholder(cardholder_id,name,surname,status) VALUES('{}', '{}', '{}', '{}')".format(cardholder_id, name, surname, status)
    mycursor.execute(myquery)
    return


def create_New_Cardholder_and_Card(mycursor, cardholder_id, name, surname, status, start_date, card_duration, zones):
    '''
    Creates a new cardholder and his first card
    '''

    create_New_Cardholder(mycursor, cardholder_id, name, surname, status)
    new_card_id = create_New_Card(mycursor, cardholder_id, start_date, card_duration, zones)
    return new_card_id


def change_Cardholder_Status(mycursor, cardholder_id, status):
    '''
    Changes the status of an existing cardholder
    '''

    myquery  = "UPDATE cardholder h SET h.status='{}' WHERE h.cardholder_id='{}'".format(status, cardholder_id)
    mycursor.execute(myquery)
    mycursor.fetchall()
    return


def update_Line_History(mycursor):
    '''
    TODO: To be, or not to be?
    Updates the line history
    '''

    return
