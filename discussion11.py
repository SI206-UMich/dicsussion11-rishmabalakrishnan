import unittest
import sqlite3
import json
import os
# starter code

# Create Database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


# Creates list of species ID's and numbers
def create_species_table(cur, conn):

    species = ["Rabbit",
    "Dog",
    "Cat",
    "Boa Constrictor",
    "Chinchilla",
    "Hamster",
    "Cobra",
    "Parrot",
    "Shark",
    "Goldfish",
    "Gerbil",
    "Llama",
    "Hare"
    ]

    cur.execute("DROP TABLE IF EXISTS Species")
    cur.execute("CREATE TABLE Species (id INTEGER PRIMARY KEY, title TEXT)")
    for i in range(len(species)):
        cur.execute("INSERT INTO Species (id,title) VALUES (?,?)",(i,species[i]))
    conn.commit()

# TASK 1
# CREATE TABLE FOR PATIENTS IN DATABASE
def create_patients_table(cur, conn):
    # create a new table with the following feeds:
    # pet id, name (string), species_id (number), age (integer), cuteness (integer), aggressiveness (number)
    cur.execute('CREATE TABLE IF NOT EXISTS Patients (pet_id, INTEGER, name TEXT, species_id INTEGER, age INTEGER, cuteness INTEGER, aggressiveness INTEGER)')
    conn.commit()

# ADD FLUFFLE TO THE TABLE
def add_fluffle(cur, conn):
    # name = Fluffle, species = "Rabbit", age = 3, cuteness = 90, aggressiveness = 100
    cur.execute('INSERT OR IGNORE INTO Patients (pet_id, name, species_id, age, cuteness, aggressiveness) VALUES (?, ?, ?, ?, ?, ?)', (0, 'Fluffle', 0, 3, 90, 100))
    conn.commit()

# TASK 2
# CODE TO ADD JSON TO THE TABLE
# ASSUME TABLE ALREADY EXISTS
def add_pets_from_json(filename, cur, conn):
    
    # WE GAVE YOU THIS TO READ IN DATA
    f = open(filename)
    file_data = f.read()
    f.close()
    json_data = json.loads(file_data)

    # THE REST IS UP TO YOU
    pet_index = 1
    
    for pet in json_data:
        species = pet['species']
        cur.execute("SELECT id FROM Species WHERE title='" + species + "'")
        for row in cur:
            species_id = row[0]
            # print(species_id)
        cur.execute('INSERT OR IGNORE INTO Patients (pet_id, name, species_id, age, cuteness, aggressiveness) VALUES (?, ?, ?, ?, ?, ?)', (pet_index, pet['name'], species_id, pet['age'], pet['cuteness'], pet['aggressiveness']))
        pet_index += 1
        conn.commit()

# TASK 3
# CODE TO OUTPUT NON-AGGRESSIVE PETS
def non_aggressive_pets(aggressiveness, cur, conn):
    cur.execute("SELECT name FROM Patients WHERE aggressiveness < '" + str(aggressiveness) + "'")
    non_aggressive = []
    for row in cur:
        non_aggressive.append(row)
    conn.commit()

def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('animal_hospital.db')
    create_species_table(cur, conn)

    create_patients_table(cur, conn)
    add_fluffle(cur, conn)
    add_pets_from_json('pets.json', cur, conn)
    ls = (non_aggressive_pets(10, cur, conn))
    print(ls)
    
    
if __name__ == "__main__":
    main()

