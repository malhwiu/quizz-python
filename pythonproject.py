# -*- coding: iso-8859-1 -*-

from ast import Str
from asyncio.windows_events import NULL
import os
from os import system, name
import sqlite3
import time
from datetime import datetime
import threading

#global variablet
score = 0
startTime = datetime.now()

def End():
    print("\nPisteet:", f"{score}/39")
    endTime = datetime.now()
    aika = endTime - startTime
    kesto = datetime.now()
    kesto = aika
    print("visan kesto =", kesto)

def Quiz():
    #python on outo nii tollee koska ei osaa muuttaa niitä muuten
    global score
    score = 0
    
    def clear_console():
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')  
    try:
        #tää yhdistää sen siihen tietokantaan 
        #laita tähän sinulle toimiva tiedostopolku!!---?
        connection = sqlite3.connect('C:\\dbs\\tiovisa.db')
        cursor = connection.cursor()
        #tää noutaa ne kymysykset
        sqlite_select_query = """SELECT kysymys, vastaus1, vastaus2, vastaus3, oikea_vastaus FROM tbl_aineisto ORDER BY RANDOM()"""
        cursor.execute(sqlite_select_query)
        #tää hakee ne kaikki tiedot 
        records = cursor.fetchall()
        startTime = datetime.now()
        print(startTime.strftime("%M:%S"))
        
        lopeta = False
        
        enumerate(records, 1)
        row = 0
        
        while lopeta == False:
            row += 1
            
            clear_console()
            #ja tää on for lause joka printtaa ne kysymykset, niin monta kertaa kuin rivejä löytyy tietokannasta.
            print(f"{row}. Kysymys: {records[row][0]}")
            print(f"Vastaus 1: {records[row][1]}")
            print(f"Vastaus 2: {records[row][2]}")
            print(f"Vastaus 3: {records[row][3]}")
            print("\n")
            #tää user on käyttäjän inputin nimi
            user = None
            
            kesken = datetime.now()
            print("aikaa kulutettu :", kesken - startTime)
            
            while user not in ["0", "1", "2", "3"]:
                user = input("Anna oikea vastaus: ")
                
                if user not in ["0","1", "2", "3"]:
                    print("\nVirheellinen vastausvaihtoehto. Sopivia vastausvaihtoehtoja ovat 1, 2 ja 3. Anna vastaus uudelleen.")
                    print("\n")
                elif user == "0": #lopettaa tietovisan jos antaa 0:n vastaukseksi
                    lopeta = True
                elif int(user) == records[row][4]:
                    print("\nOikea vastaus!")
                    print("\n")
                    score += 1
                else:
                    print("\nVirheellinen vastaus!")
                    print("\n")
                time.sleep(1.5)
                if score >= 39:
                    break

            #lopettaa pelin jos käyttäjä haluaa
            if lopeta == True:
                cursor.close()
                End()
            #tää laskee pisteitä, toimii. näyttää sen pelin lopussa
            if score >= 39:
                cursor.close()
                End()

    except sqlite3.Error as error:
        print("Failed to read data from table", error)
    finally:
        if connection:
            connection.close()
            print("The Sqlite connection is closed")

Quiz()