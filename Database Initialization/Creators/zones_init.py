import random
import cards_init

random.seed(3900)
DRIVERS = 25
ZONE_IDS = [1,2,3]

insert_str = "INSERT INTO zones(zone_id, card_id) VALUES "
zonesDic = {}
i=0
for card_id in cards_init.carDic:
    temp_ids = ZONE_IDS.copy()
    how_many = random.randint(1,3)

    selected_zones = []
    for j in range(how_many):
        selected_zones.append(temp_ids.pop(random.randint(0,len(temp_ids)-1)))
        
    selected_zones.sort()

    for j in range(how_many):
        insert_str += "(" + str(selected_zones[j]) + "," + str(card_id+1) + ")"
        if j<how_many-1: insert_str += ","
        
    if (i < len(cards_init.carDic) - 1): insert_str += ","
    i+=1
    
insert_str += ";"

with open("strings.txt", 'a') as f:
    f.write("\n\n" + insert_str)



