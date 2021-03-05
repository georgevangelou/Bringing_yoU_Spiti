############################  USED LIBRARIES  ############################

from tkinter import *
from tkinter import messagebox

import os, sys, time
import mysql.connector

import queries as q
import datetime as d
import functions as f
from constants import DEBUG, HOST, USER, PASSWORD, DATABASE



############################  BUTTON HANDLERS  ############################

def btn1_handler(): 
    '''
    Bus coordinates\n
    '''

    def btn1A_handler():    
        try:
            mydb = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
            mycursor = mydb.cursor()
            line_id = str(entry.get())
            coordinates = q.get_Line_Bus_Coordinates(mycursor, line_id)
            coordinates = [temp[1] for temp in coordinates]
            msg = ["################\nBus position: {}".format(foo) for foo in coordinates]
            messagebox.showinfo("MAP", "\n".join(msg))            
            mydb.close()
        except Exception as e:
            messagebox.showinfo("Exception raised: ", e)

    window2 = Toplevel(window1)
    window2.title("Enter the line_id")
    window2.geometry('300x50+{}+{}'.format(window1.winfo_x()+150, window1.winfo_y()+150))
    window2.resizable(width=False, height=False)
    entry = Entry(window2)
    entry.grid(row=1, column=1)
    btnT1 = Button(window2,text='ENTER',command=btn1A_handler)
    btnT1.grid(row=1, column=2)
 

def btn2_handler(): 
    '''
    Line Timetables\n
    '''

    def get_bus_stops(line_title):
        '''
        Extracts start and stop of line from its name\n
        DEPRECATED
        '''
        bus_stops = line_title.split(" to ")
        express_ind = bus_stops[1].find("(")
        express = False
        if  express_ind> 0:
            express = True
            bus_stops[1] = bus_stops[1][:express_ind-1]
        return bus_stops,express

    def create_timetable(line_info, data, day_type, width=30):

        rows = len(data)
        bus_stops, express = get_bus_stops(line_info[1])
        headers = ["Start: ", "End: "]
        timetable_win = Toplevel(window1)
        if express:
            timetable_win.title("Line "+str(line_info[0])+" on "+day_type+" (EXPRESS)")
        else:
            timetable_win.title("Line "+str(line_info[0])+" on "+day_type)
        timetable_win.resizable(height=False, width=False)
        canvas = Canvas(timetable_win) #CANVAS
        canvas.pack(side=LEFT)
        scrollbar = Scrollbar(timetable_win, command=canvas.yview) #SCROLLBAR
        scrollbar.pack(side=LEFT, fill='y')
        canvas.configure(yscrollcommand = scrollbar.set)
        canvas.bind('<Configure>', lambda event:canvas.configure(scrollregion=canvas.bbox('all')))
        frame = Frame(canvas) #FRAME
        canvas.create_window((0,0), window=frame, anchor='nw')
        for j in range(2):
            e = Entry(frame, width=width, font="Helvetica 10 bold")
            e.insert(0, headers[j]+bus_stops[j])
            e.configure(state="readonly")
            e.grid(row=0,column=j)
        for i in range(rows):
            for j in range(2):
                e = Entry(frame, width=width, font="Helvetica 10")
                e.insert(0, str(data[i][j]))
                e.configure(state="readonly")
                e.grid(row=i+1, column=j)
        timetable_win.mainloop()
    
    def btn2A_handler():    
        try:
            mydb = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
            mycursor = mydb.cursor()
            line_id  = str(entry1.get())
            day_type = str(entry2.get())
            line_info, line_itineraries = q.get_Line_Timetable(mycursor, line_id, day_type)
            itin_table = [[y[1],y[2]] for y in line_itineraries]
            create_timetable(line_info, itin_table, day_type)
        except Exception as e:
            messagebox.showinfo("Exception raised: ", e)

    window2 = Toplevel(window1)
    window2.title("Enter the line_id and day_type")
    window2.geometry('350x60+{}+{}'.format(window1.winfo_x()+150, window1.winfo_y()+150))
    window2.resizable(width=False, height=False)
    entry1 = Entry(window2)
    entry1.grid(row=1, column=1)
    entry2 = Entry(window2)
    entry2.grid(row=2, column=1)
    btnT1 = Button(window2,text='ENTER',command=btn2A_handler)
    btnT1.grid(row=2, column=2)


def btn3_handler():
    '''
    Available routes\n
    '''

    try:
        mydb = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        mycursor = mydb.cursor()
        lines_info = q.get_All_Lines_Information(mycursor)
        msg = ["################\nLine id: {}  Name: {}".format(foo[0], foo[1]) for foo in lines_info]
        messagebox.showinfo("Lines", "\n".join(msg))
        mydb.close()
        #window2.destroy()
    except Exception as e:
        messagebox.showinfo("Exception raised: ", e)
    return


def btn4_handler(): 
    '''
    Card status\n
    '''

    def btn4A_handler():
        try:
            mydb = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
            mycursor = mydb.cursor()
            card_id = str(entry.get())
            current_date = d.datetime.now()
            current_zone = -1
            isValid, msg, zones = q.get_Cards_Status(mycursor, card_id, current_date, current_zone)
            c = "Your card is: " + msg 
            if isValid: c += "\nIts eligible zones are: " + str(zones)
            messagebox.showinfo("Card status", c)
            mydb.close()
            window2.destroy()
        except Exception as e:
            messagebox.showinfo("Exception raised:", e)
            
    window2 = Toplevel(window1)
    window2.title("Enter your card id:")
    window2.geometry('290x50+{}+{}'.format(window1.winfo_x()+150, window1.winfo_y()+150))
    window2.resizable(width=False, height=False)
    entry = Entry(window2)
    entry.grid(row=1, column=1)
    btnT1 = Button(window2,text='ENTER',command=btn4A_handler)
    btnT1.grid(row=1, column=2)


def btn5_handler(): 
    '''
    Closest bus stops\n
    '''

    def btn5A_handler():    
        try:
            mydb = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
            mycursor = mydb.cursor()
            line_id = str(entry1.get())
            if line_id=='': line_id='-1'
            line_id = int(line_id)
            #personCoordinates = f.get_My_Coordinates()
            temp = str(entry2.get()).split(",")
            personCoordinates = [int(i) for i in temp]
            nearest_stops = q.get_Closest_BusStops(mycursor, personCoordinates, maxDist=200, line_id=line_id)
            msg = ["################\nBus stop name: {}  Distance from you: {} meters".format(foo[1], int(foo[2])) for foo in nearest_stops]
            messagebox.showinfo("MAP", "\n".join(msg))
            mydb.close()
        except Exception as e:
            messagebox.showinfo("Exception raised: ", e)

    window2 = Toplevel(window1)
    window2.title("Enter the line_id and your position:")
    window2.geometry('380x60+{}+{}'.format(window1.winfo_x()+150, window1.winfo_y()+150))
    window2.resizable(width=False, height=False)
    entry1 = Entry(window2)
    entry1.grid(row=1, column=1)
    entry2 = Entry(window2)
    entry2.grid(row=2, column=1)
    btnT1 = Button(window2,text='ENTER',command=btn5A_handler)
    btnT1.grid(row=2, column=2)


def btn6_handler(): 
    '''
    Bus stop arrivals with ETAs\n
    '''

    def btn6A_handler():    
        try:
            mydb = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
            mycursor = mydb.cursor()
            bus_stop_id = str(entry.get())
            current_time = d.datetime.now().time()
            if d.datetime.now().weekday()<6: day_type = 'WEEKDAYS'
            else: day_type = 'WEEKENDS'
            etas = q.get_BusStop_Statistical_ETAs(mycursor, bus_stop_id, current_time, day_type)
            msg = ["################\nLine number: {}  ETA: {} minutes".format(foo[0], int(foo[1])) for foo in etas]
            if len(msg)>0: messagebox.showinfo("ETAS", "\n".join(msg))
            else: messagebox.showinfo("ETAS", "(no arrivals currently expected)")
            mydb.close()
        except Exception as e:
            messagebox.showinfo("Exception raised: ", e)

    window2 = Toplevel(window1)
    window2.title("Enter the bus stop id:")
    window2.geometry('300x50+{}+{}'.format(window1.winfo_x()+150, window1.winfo_y()+150))
    window2.resizable(width=False, height=False)
    entry = Entry(window2)
    entry.grid(row=1, column=1)
    btnT1 = Button(window2,text='ENTER',command=btn6A_handler)
    btnT1.grid(row=1, column=2)


def btn7_handler(): 
    '''
    New cardholder and card\n
    '''

    def btn7A_handler(cardholder_id, name, surname, status, start_date, card_duration, zones):
        try:
            mydb = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
            mycursor = mydb.cursor()
            new_card_id = q.create_New_Cardholder_and_Card(mycursor, cardholder_id, name, surname, status, start_date, card_duration, zones) 
            mydb.commit()
            mydb.close()
            msg = "# \nCard id assigned: {}".format(new_card_id)
            messagebox.showinfo("New Card id", msg)           
        except Exception as e:
            messagebox.showinfo("Exception raised: ", e)

    def get_var(pointer):
        window2 = Tk()
        window2.title("Enter {}".format(pointer))
        window2.geometry('300x50+{}+{}'.format(window1.winfo_x()+150, window1.winfo_y()+150))
        window2.resizable(width=False, height=False)
        entry = Entry(window2)
        entry.grid(row=1, column=1)
        btnT1 = Button(window2,text='ENTER',command=lambda: set_var(window2, entry, pointer))
        btnT1.grid(row=1, column=2)

    def set_var(mywindow, entry, pointer): 
        global adt, name, surname, status, card_duration, zones
        temp = entry.get()
        if pointer=="id":
            adt = temp
            get_var("name")
        elif pointer=="name": 
            name = temp
            get_var("surname")
        elif pointer=="surname": 
            surname = temp
            get_var("status")
        elif pointer=="status": 
            status = temp
            get_var("duration")
        elif pointer=="duration":
            card_duration = int(temp)
            get_var("zones")
        elif pointer=="zones":
            zones = temp.split(",")
            if DEBUG: print(name+", "+surname+", "+status+", "+str(card_duration)+", "+str(zones))
            btn7A_handler(adt, name, surname, status, start_date, card_duration, zones)        
        mywindow.destroy()

    adt = ""
    name = ""
    surname = ""
    status = ""
    start_date = d.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    card_duration = 0
    zones = []
    get_var("id")
    return


def btn8_handler():
    '''
    Renew card\n
    '''

    def btn8A_handler(card_id, start_date, card_duration, zones):  
        #renew_Card(mycursor, card_id, start_date, card_duration, zones)
        try:
            mydb = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
            mycursor = mydb.cursor()
            q.renew_Card(mycursor, card_id, start_date, card_duration, zones)
            mydb.commit()
            mydb.close()
        except Exception as e:
            messagebox.showinfo("Exception raised: ", e)

    def get_var(pointer):
        window2 = Tk()
        window2.title("Enter {}".format(pointer))
        window2.geometry('300x50+{}+{}'.format(window1.winfo_x()+150, window1.winfo_y()+150))
        window2.resizable(width=False, height=False)
        entry = Entry(window2)
        entry.grid(row=1, column=1)
        btnT1 = Button(window2,text='ENTER',command=lambda: set_var(window2, entry, pointer))
        btnT1.grid(row=1, column=2)

    def set_var(mywindow, entry, pointer): 
        global card_id, card_duration, zones
        temp = entry.get()
        if pointer=="id":
            card_id = temp
            get_var("duration")
        elif pointer=="duration":
            card_duration = int(temp)
            get_var("zones")
        elif pointer=="zones":
            zones = temp.split(",")
            if DEBUG: print(str(card_id)+", "+start_date+", "+str(card_duration)+", "+str(zones))
            btn8A_handler(card_id, start_date, card_duration, zones)      
        mywindow.destroy()
    
    card_id = ""
    start_date = d.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    card_duration = 0
    zones = []
    get_var("id")
    return


def btn9_handler():
    '''
    Line Information\n
    '''

    #get_Line_Information(mycursor, line_id)
    def btn9A_handler():    
        try:
            mydb = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
            mycursor = mydb.cursor()
            line_id = str(entry.get())
            line_info = q.get_Line_Information(mycursor, line_id)
            line_id = str(line_info[0]); line_name = line_info[1]; start = line_info[2]; stop = line_info[3]
            msg = ["Number: "+line_id, "Name: "+line_name, "First stop: "+start, "Last stop: "+stop]
            messagebox.showinfo("Line {} information".format(line_id), "\n".join(msg))            
            mydb.close()
        except Exception as e:
            messagebox.showinfo("Exception raised: ", e)

    window2 = Toplevel(window1)
    window2.title("Enter the line_id")
    window2.geometry('300x50+{}+{}'.format(window1.winfo_x()+150, window1.winfo_y()+150))
    window2.resizable(width=False, height=False)
    entry = Entry(window2)
    entry.grid(row=1, column=1)
    btnT1 = Button(window2,text='ENTER',command=btn9A_handler)
    btnT1.grid(row=1, column=2)
    return



############################  MAIN PROGRAM  ############################

if __name__=="__main__":
    # Setting the main window
    window1 = Tk()
    window1.title("Bringing U Spiti (B.U.S.)")
    window1.geometry('800x600+300+150')
    window1.resizable(width=False, height=False)

    # Setting the background
    bg_image = PhotoImage(file="background.gif")
    bg_label = Label(window1, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)


    # Creating the main buttons
    HEIGHT = 1
    WIDTH = 20
    PADx = 3
    PADy = 2

    #object.place(x=110, y=0) or object.grid(row=20, column=2)
    btn1 = Button(window1,text='Current Bus Positions', command=btn1_handler, height = HEIGHT, width = WIDTH)
    btn1.grid(row=1, column=1, padx=PADx, pady=PADy)
    btn2 = Button(window1,text='Line Timetables', command=btn2_handler, height = HEIGHT, width = WIDTH)
    btn2.grid(row=1, column=2, padx=PADx, pady=PADy)
    btn3 = Button(window1,text='Available routes', command=btn3_handler, height = HEIGHT, width = WIDTH)
    btn3.grid(row=1, column=3, padx=PADx, pady=PADy)
    btn4 = Button(window1,text='Card status', command=btn4_handler, height = HEIGHT, width = WIDTH)
    btn4.grid(row=1, column=4, padx=PADx, pady=PADy)
    btn5 = Button(window1,text='Nearest Stops', command=btn5_handler, height = HEIGHT, width = WIDTH)
    btn5.grid(row=2, column=1, padx=PADx, pady=PADy)
    btn6 = Button(window1,text='Arrivals', command=btn6_handler, height = HEIGHT, width = WIDTH)
    btn6.grid(row=2, column=2, padx=PADx, pady=PADy)
    btn7 = Button(window1,text='New customer', command=btn7_handler, height = HEIGHT, width = WIDTH)
    btn7.grid(row=2, column=3, padx=PADx, pady=PADy)
    btn8 = Button(window1,text='Renew card', command=btn8_handler, height = HEIGHT, width = WIDTH)
    btn8.grid(row=2, column=4, padx=PADx, pady=PADy)
    btn9 = Button(window1,text='Line Information', command=btn9_handler, height = HEIGHT, width = WIDTH)
    btn9.grid(row=3, column=1, padx=PADx, pady=PADy)

    window1.mainloop()


