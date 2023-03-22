encodingPythonApplicationV2.py

# -*- coding: iso-8859-1 -*-

# It's not a great idea to use a europe only encoding standard

from ast import Str
from asyncio.windows_events import NULL
import os
from os import system, name
import sqlite3
import time
from datetime import datetime
from enum import IntEnum
import threading
import curses


class Position(IntEnum):
    QUESTION = 0,
    FIRSTANS = 1.
    SECONDANS = 2.
    THIRDANS = 3.
    TIMER = 4,
    ANS = 7,
    USRINPUTTEXT = 5
    USRINPUT = 6


# For some reason in curses x and y position are flipped

#global variables
score = 0
startTime = datetime.now()
tui = curses.initscr()

# this is the amount of time in seconds we wait before the timer is updated
timer_update_time = 0.25

# just in case
tui.refresh()

def End():
    print(F"Pisteet: {score}")
    endTime = datetime.now()
    aika = endTime - startTime
    kesto = datetime.now()
    kesto = aika
    curses.endwin()
    print(F"visan kesto = {kesto}")

def user_input():

    ans = ""
    c = ""
    tui.addstr(Position.USRINPUTTEXT,0,"Anna oikea vastaus!")
    #while c != "\n" or c != "10" or c != 10:
    c = tui.getch()
    ans += chr(c)
    tui.addstr(8,0,ans)
    return ans

def update_timer():
    threading.Timer(timer_update_time, update_timer).start()
    kesken = datetime.now()
    tui.addstr(Position.TIMER,0,F"aikaa kulutettu: {kesken - startTime}")
    tui.refresh()

def Quiz():
    global score
    score = 0
    
    try:
        # tää yhdistää sen siihen tietokantaan 
        # laita tähän sinulle toimiva tiedostopolku!!
        connection = sqlite3.connect('tiovisa.db')
        cursor = connection.cursor()
        # tää noutaa ne kymysykset
        sqlite_select_query = """SELECT kysymys, vastaus1, vastaus2, vastaus3, Oikea_vastaus_nro FROM tbl_aineisto ORDER BY RANDOM()"""
        cursor.execute(sqlite_select_query)
        # tää hakee ne kaikki tiedot 
        records = cursor.fetchall()
        startTime = datetime.now()
        print(startTime.strftime("%M:%S"))
        
        lopeta = False
        
        enumerate(records, 1)
        row = 0
        
        while lopeta == False:
            row += 1
            
            # clear_console()
            # print question and answers
            tui.addstr(Position.QUESTION,0,f"{row}. Kysymys: {records[row][0]}")
            tui.addstr(Position.FIRSTANS,0,f"Vastaus 1: {records[row][1]}")
            tui.addstr(Position.SECONDANS,0,f"Vastaus 2: {records[row][2]}")
            tui.addstr(Position.THIRDANS,0,f"Vastaus 3: {records[row][3]}")
            # user input is stored here
            user = None

            update_timer()
            while user not in ["0", "1", "2", "3"]:
                tui.refresh()
                # get user input
                #user = input("Anna oikea vastaus: ")

                user = user_input()
                tui.clear()

                #a = tui.getch()
                # check if user gave 1, 2 or 3, as an answer
                if str(user) not in ["0","1", "2", "3"]:
                    tui.addstr(Position.ANS,0,
F"Virheellinen vastausvaihtoehto. Sopivia vastausvaihtoehtoja ovat 1, 2 ja 3. Anna vastaus uudelleen.")
                    
                elif user == "0": # if user gave 0 terminate the program
                    lopeta = True
                # elif int(user) == records[row][4]:
                elif user == records[row][4]:
                    # if user's give number mathches the number in the database
                    tui.addstr(Position.ANS,0,"Oikea vastaus!")
                    score += 1
                else:
                    tui.addstr(Position.ANS,0,F"Virheellinen vastaus!")

                # time.sleep(1.5)
                if score >= 39:
                    break
            
            #lopettaa pelin jos käyttäjä haluaa
            if lopeta == True or score >= 39:
                cursor.close()
                End()

            #tää laskee pisteitä, toimii. näyttää sen pelin lopussa
            # if score >= 39:
            #     cursor.close()
            #     End()

    except sqlite3.Error as error:
        print("Failed to read data from table", error)
    finally:
        if connection:
            connection.close()
            print("The Sqlite connection is closed")

Quiz()
