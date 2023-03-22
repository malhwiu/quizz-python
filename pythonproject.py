# -*- coding: iso-8859-1 -*-

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

# these are y positions for where we write our text
class Position(IntEnum):
    QUESTION = 2
    FIRST_ANS = 3
    SECOND_ANS = 4
    THIRD_ANS = 5
    TIMER = 6
    USR_INPUT_TEXT = 7
    USR_INPUT = 8
    ANS = 9
# For some reason in curses x and y position are flipped

# global variables
score = 0
start_time = datetime.now()
# this is for question and answeres
tui = curses.initscr()

num_rows, num_cols = tui.getmaxyx()
# this is for user input
input_box = curses.newwin(4, num_cols-2, 8, 1)

# this is the amount of time in seconds we wait before the timer is updated
TIMER_UPDATE_TIME = 0.25
# This is used as the default x position for the windows
X_POS = 3
max_score = 3
ans_len = 0

def clear_windows():
    tui.clear()
    input_box.clear()

def update_screen():
    # The order in which the windows are refreshed matters
    tui.border()
    tui.refresh()

    input_box.border()
    input_box.box()
    input_box.refresh()

def End():
    end_time = datetime.now()
    aika = end_time - start_time
    kesto = datetime.now()
    kesto = aika

    curses.endwin()
    print(f"Pisteet: {score}")
    print(f"Visan kesto = {kesto}")
    exit()

def user_input():
    global ans_len
    ans = ""
    c = ""
    # write this on the window' border
    input_box.addstr(0, X_POS, "Anna oikea vastaus!")
    # 
    # get charachters until user presses enter
    # TODO: properly handle backspace 
    while c != "\n":
        c = chr(input_box.getch())

        if c == 8: # if use pressed backspace
            ans = ans[:-1]
        else:
            ans += c

        ans_len = len(ans)
        # input_box.clear()
        input_box.addstr(1, X_POS, ans)

    # clear window from charachters
    input_box.clear()
    return ans[0] # return the first charachter

def update_timer():
    threading.Timer(TIMER_UPDATE_TIME, update_timer).start()
    kesken = datetime.now()
    tim = kesken - start_time
    tui.addstr(Position.TIMER, X_POS, f"aikaa kulutettu: {tim.seconds} sekunttia")

    input_box.noutrefresh()
    tui.noutrefresh()
    curses.setsyx(9,X_POS+ ans_len + 1)
    curses.doupdate()

def update_screen_with_question(question):
   # print question and answers
   tui.addstr(Position.QUESTION,  X_POS,f"{question[0]}. Kysymys: {question[1]}")
   tui.addstr(Position.FIRST_ANS, X_POS,f"Vastaus 1: {question[2]}")
   tui.addstr(Position.SECOND_ANS,X_POS,f"Vastaus 2: {question[3]}")
   tui.addstr(Position.THIRD_ANS, X_POS,f"Vastaus 3: {question[4]}")
    
def Quiz():
    global score
    score = 0

    try:
        # tää yhdistää sen siihen tietokantaan
        # laita tähän sinulle toimiva tiedostopolku!!
        connection = sqlite3.connect("db_tietovisa_python.db")
        cursor = connection.cursor()
        # tää noutaa ne kymysykset
        sqlite_select_query = "SELECT kysymys, vastaus1, vastaus2, vastaus3, Oikea_vastaus_nro FROM tbl_aineisto ORDER BY RANDOM()"
        cursor.execute(sqlite_select_query)
        # tää hakee ne kaikki tiedot
        records = cursor.fetchall()
        #startTime = datetime.now()
        
        lopeta = False

        enumerate(records, 1)
        row = 0

        while lopeta == False:
            row += 1

            # make an array with our questions
            update_screen_with_question([row,
                                         records[row][0],
                                         records[row][1],
                                         records[row][2],
                                         records[row][3]
                                         ])

            # user input is stored here
            user = None
            if True == lopeta:
                update_timer()

            # ask for input until the user give 0,1,2 or 3
            while user not in ["0", "1", "2", "3"]:
                update_screen()
                
                # get user input
                user = user_input()
                clear_windows()
                
                # check if user did not give 1, 2 or 3, as an answer
                if str(user) not in ["0", "1", "2", "3"]:
                    update_screen_with_question([row,
                                         records[row][0],
                                         records[row][1],
                                         records[row][2],
                                         records[row][3]
                                         ])
                    tui.addstr(
                        Position.ANS+3,
                        X_POS,
                        "Virheellinen vastausvaihtoehto. Sopivia vastausvaihtoehtoja ovat 1, 2 ja 3. Anna vastaus uudelleen.",
                    )

                # this does not work correctly
                elif user == "0":  # if user gave 0 terminate the program
                    lopeta = True

                elif user == records[row][-1]:
                    # if user's give number mathches the number in the database
                    tui.addstr(Position.ANS + 3, X_POS, "Oikea vastaus!")
                    score += 1
                else:
                    tui.addstr(Position.ANS + 3, X_POS, "Virheellinen vastaus!")

                if score >= max_score:
                    break

            # lopettaa pelin jos käyttäjä haluaa
            if lopeta == True or score >= max_score:
                cursor.close()
                End()

    except sqlite3.Error as error:
        print("Failed to read data from table", error)
    finally:
        if connection:
            connection.close()
            print("The Sqlite connection is closed")

Quiz()
