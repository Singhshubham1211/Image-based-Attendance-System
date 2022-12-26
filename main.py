from cProfile import label
from tkinter import messagebox
from tkinter.font import BOLD
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import tkinter as tk
from tkinter import *
import pandas as pd
import csv
from tkinter import ttk


path = 'Training_images'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)


def findEncodings(images):
    encodeList = []


    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        print(encode)
        encodeList.append(encode)
    return encodeList


def markAttendance(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()

        
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
            if name not in nameList:
                now = datetime.now()
                dtString = now.strftime('%H:%M')
                f.writelines(f'\n{name},{dtString}')

def add():
    mname = var.get()
    if(mname==""):
        return messagebox.showwarning("Not updated", "Blank Empty")
        

    messagebox.showinfo("Update", "Attendence Marked")
    markAttendance(mname)


def webcam():
    encodeListKnown = findEncodings(images)
    print('Encoding Complete')

    cap = cv2.VideoCapture(0)

    while (True):
        success, img = cap.read()

        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            #print(faceDis)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                #print(name)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                markAttendance(name)
                

        cv2.imshow('Webcam', img)
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
        # cv2.waitKey(1)

def removeDup():
    data = pd.read_csv("Attendance.csv")
    data = data.drop_duplicates(keep="first")
    print(data)
    data.to_csv('file1.csv',index=False)
    showAtten()
    # showAtten
    # with open('Attendance_without_dupes.csv', 'w', encoding='UTF8') as f:
    #     writer = csv.writer(f)

    # # write the header
    #     # writer.writerow(header)

    # # write the data
    #     writer.writerow(data)

def showAtten():
    
    win = Toplevel(window)
    win.geometry("600x600")
    TableMargin = Frame(win, width=500)
    TableMargin.pack(side=TOP)
    scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
    scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
    tree = ttk.Treeview(TableMargin, columns=("Name", "Time"), height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('Name', text="Name", anchor=W)
    tree.heading('Time', text="Time", anchor=W)
    #tree.heading('Address', text="Address", anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=200)
    #tree.column('#2', stretch=NO, minwidth=0, width=200)
    #tree.column('#3', stretch=NO, minwidth=0, width=300)
    tree.pack()

    with open('file1.csv') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            Name = row['Name']
            Time = row['Time']
            
            tree.insert("", 0, values=(Name, Time))


window = tk.Tk()
window.geometry('500x500')
window.title("Attendance Window")
var = StringVar()
btn1 = tk.Button(window,text = 'take attendence',width  = 25,command = webcam).place(x=160,y=250)
labl_0 = Label(window, text="Attendance Form",width=20,font=("bold", 20))  
labl_0.place(x=90,y=53)  
manual = Label(window,text="Manual Attendance",font=(BOLD,10)).place(x=180,y=100)
a = Label(window ,text = "Name").place(x=150,y=130)  
a1 = Entry(window,textvariable=var).place(x=200,y=130)  
btn = tk.Button(window ,text="Submit",command=add).place(x=220,y=170)
label2 = Label(window,text="Automatic Attendance",font=(BOLD,10)).place(x=180,y=220)
btn3 = tk.Button(window,text="Show Attendance",command=removeDup).place(x=200,y=400)
window.mainloop()