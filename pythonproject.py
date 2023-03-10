# -*- coding: iso-8859-1 -*-

from ast import Str
from asyncio.windows_events import NULL
import time
import sqlite3
import os
import sys

# print(os.name)

def getAllRows() :
    def clear_console() :
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    score = 0 #Pisteiden aloitus.
    remaining_time = 60 # 1 minuutti

    try:
        connection = sqlite3.connect('db_tietovisa_python.db') # Yhditää SQLite databaseen
        cursor = connection.cursor()
        sqlite_select_query = """SELECT kysymys, vastaus1, vastaus2, vastaus3, oikea_vastaus_nro FROM tbl_aineisto ORDER BY RANDOM()"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        kysymysnumero = 1 #Alkuarvo kysymysnumerolle

        while remaining_time > 0 and kysymysnumero <= 39:
            clear_console()
            row = records[kysymysnumero-1] # Hakee kysymyksen sekoitetusta lista´sta
            print(f"{kysymysnumero}. Kysymys: {row[0]}") # Tulostaa Kysymyksen ja kysymysnumeron
            print(f"Vastaus 1: {row[1]}") # Tulostaa Vastaus vaihtoehdot
            print(f"Vastaus 2: {row[2]}")
            print(f"Vastaus 3: {row[3]}")
            print("\n") 
            user = None
            start_time = time.time() # Aloittaa ajastimen
            while user not in ["1", "2", "3"]:
                user = input("Anna oikea vastaus: ") # Kysyy käyttäjältä vastausta
                if user not in ["1", "2", "3"]:
                    print("\n")
                    print("Tama ei ole oikea vastausvaihtoehto. Kayta vastausvaihtoehtoja 1, 2 ja 3. Anna vastaus uudelleen.")
                    print("\n")
                elif user == row[4]:
                    print("\n")
                    print("Oikea vastaus!")
                    print("\n")
                    score += 1 #Lisää pisteitä aina kun saat oikean vastauksen.
                    elapsed_time = time.time() - start_time # Calculate the time taken to answer
                    remaining_time += 5 # Add 5 seconds to the remaining time
                    kysymysnumero += 1 #Kasvattaa kysymysnumeroa yhdellä
                else:
                    print("\n")
                    print("Väärä vastaus!")
                    print("\n")
                    remaining_time -= 2 # Vie 2 sekunttia ajasta
                    kysymysnumero += 1 #Kasvattaa kysymysnumeroa yhdellä
                print("\n") # Tulostaa tyhjän rivin, jotta tekstiä olisi helpompi lukea
            print(f"Aikaa jäljellä: {remaining_time} sekuntia")
            print("------------------------------------------------------------------------------------------------------------------------")
            time.sleep(1.5)
        print("\n")
        print("Pisteet:", f"{score}/39") #Tulostaa pisteiden loppumäärän oikeiden vastausten perusteella.
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from table", error) # Ilmoittaa virheistä
        exit()
    finally:
        if connection:
            connection.close()
            print("The Sqlite connection is closed") # Ilmoittaa kun kysely on lopussa

getAllRows()
