import random

random.seed(696969)
DRIVERS = 100

ID_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

NAMES_M = ["Giannhs", "Kostas", "Loukas", "Zaxarias", "Laertis", "Alkinoos", "Giorgos", "Antonis",
           "Xrisanthos", "Andreas"]
NAMES_F = ["Katerina", "Nikh", "Elpida", "Maria", "Kleio", "Ismini", "Euterpi", "Penelope", "Elvira"]
SURNAMES_M = ["Liopas", "Panagiotou", "Karakitsos", "Evangelou", "Roussos", \
              "Peftikoglou", "Sifakis", "Avgos", "Manousakis", "Bogdanos", "Mitsotakis", "Karagkounis",
              "Meletis"]
SURNAMES_F = ["Avrami", "Panagiotou", "Anagnostopoulou", "Psora", "Konstantinou",\
              "Dimitriadi", "Giolou", "Kokkinou", "Papageorgakopoulou", "Stamatiadi", "Papagiorgi",
              "Papantoni", "Algeri"]
DEG = ['A', 'B', 'C']


insert_str = "INSERT INTO driver(driver_id, name, surname, license_degree) VALUES "
driversDic = {}
for i in range(DRIVERS):
    letter1 = ID_LETTERS[random.randint(0, len(ID_LETTERS)-1)]
    letter2 = ID_LETTERS[random.randint(0, len(ID_LETTERS)-1)]
    num = [str(random.randint(0, 9)) for k in range(6)]
    id_number = letter1 + letter2 + ' ' + ''.join(num)
    
    if random.randint(0, 10)>0:
        N = NAMES_M
        S = SURNAMES_M
    else:
        N = NAMES_F
        S = SURNAMES_F
    name = N[random.randint(0, len(N)-1)]
    sur = S[random.randint(0, len(S)-1)]

    s = DEG[random.randint(0, len(DEG) - 1)]
    
    driversDic[id_number] = [name, sur, s] # id_number: [name, surname, license degree]
    insert_str += "('" + id_number + "','" + name + "','" +\
        sur + "','" + s + "')"
    if (i < DRIVERS - 1): insert_str += ","
    
insert_str += ";"

with open("strings.txt", 'a') as f:
    f.write("\n\n" + insert_str)



