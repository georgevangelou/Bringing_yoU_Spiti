import random
import cardholders_init as ch
from datetime import datetime, timedelta


ROUTE_CARDS = ch.CARDHOLDERS
random.seed(3900)

def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


d1 = datetime.strptime('1/10/2019', '%d/%m/%Y')
d2 = datetime.strptime('8/01/2020', '%d/%m/%Y')

MAP_STATUS_TO_DISCOUNT = {"Student":50, "Handicapped":50, "Elderly":25, "Unemployed":25, "Child":50, "None":0 }
AVAILABLE_MONTH_DURATIONS = [1, 3, 6, 12]
NORMAL_MONTHLY_VALUE = 30
cardholder_ids = list( ch.cardholderDic.keys() ) #get the initialized cardholders' keys to bind to the route cards
insert_str = "INSERT INTO route_card(cardholder_id, start_date, expiration_date, value, discount_type) VALUES "
carDic = {}
for i in range(ROUTE_CARDS):
    
    cardholder_id = cardholder_ids[random.randint(0,len(cardholder_ids)-1)] #get a random cardholder id from currently available
    cardholder_ids.remove(cardholder_id)

    discount_type = MAP_STATUS_TO_DISCOUNT[ch.cardholderDic[cardholder_id][2]] #get the discount type depending on the cardholder's status
    
    start_date = random_date(d1, d2) #pick a random between the predefined ones
    card_duration = AVAILABLE_MONTH_DURATIONS[random.randint(0,len(AVAILABLE_MONTH_DURATIONS)-1)] #pick a random month-duration from the predefined ones
    expiration_date = start_date + timedelta(days = card_duration*30)

    #calculate the correct duration depending on base cost, duration and discount
    value = int(NORMAL_MONTHLY_VALUE * card_duration * (100-discount_type)/100.0) 


    carDic[i] = [cardholder_id,start_date,expiration_date,value,discount_type]

    insert_str += "('" + str(cardholder_id) + "','" + str(start_date) + "','" + str(expiration_date) + "','" + \
      str(value) + "','" + str(discount_type) + "')"

    if (i < ROUTE_CARDS - 1): insert_str += ","
    
insert_str += ";"
with open("strings.txt", 'a') as f: f.write("\n\n" + insert_str)

    
    
    
