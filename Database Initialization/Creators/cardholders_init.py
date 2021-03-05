import random

random.seed(3900)
CARDHOLDERS = 10

ID_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

NAMES_M = ["Giannhs", "Kostas", "Loukas", "Zaxarias", "Laertis", "Alkinoos", "Giorgos", "Antonis"]
NAMES_F = ["Katerina", "Nikh", "Elpida", "Maria", "Kleio", "Ismini", "Euterpi", "Penelope"]
SURNAMES_M = ["Liopas", "Panagiotou", "Karakitsos", "Evangelou", "Roussos", \
              "Peftikoglou", "Sifakis", "Avgos", "Manousakis", "Bogdanos", "Mitsotakis", "Karagkounis"]
SURNAMES_F = ["Avrami", "Panagiotou", "Anagnostopoulou", "Psora", "Konstantinou",\
              "Dimitriadi", "Giolou", "Kokkinou", "Papageorgakopoulou", "Stamatiadi", "Papagiorgi"]
STATUS = ["Student", "Handicapped", "Elderly", "Unemployed", "Child", "None"]


insert_str = "INSERT INTO cardholder(cardholder_id, name, surname, status) VALUES "
cardholderDic = {}
for i in range(CARDHOLDERS):

    letter1 = ID_LETTERS[random.randint(0, len(ID_LETTERS)-1)]
    letter2 = ID_LETTERS[random.randint(0, len(ID_LETTERS)-1)]
    num = [str(random.randint(0, 9)) for k in range(6)]
    id_number = letter1 + letter2 + ' ' + ''.join(num)
    
    if random.randint(0, 1)==0:
        N = NAMES_M
        S = SURNAMES_M
    else:
        N = NAMES_F
        S = SURNAMES_F
    name = N[random.randint(0, len(N)-1)]
    sur = S[random.randint(0, len(S)-1)]

    s = STATUS[random.randint(0, len(STATUS) - 1)]
    
    cardholderDic[id_number] = [name, sur, s]
    insert_str += "('" + id_number + "','" + name + "','" +\
        sur + "','" + s + "')"
    if (i < CARDHOLDERS - 1): insert_str += ","
    
insert_str += ";"


with open("strings.txt", 'a') as f:
    f.write("\n\n" + insert_str)

    
    
    
