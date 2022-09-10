import time
from tkinter.filedialog import askopenfile
import finegerprint_pipline
import shutil
import numpy
from PIL import Image, ImageTk
import sys
import cv2
from unicodedata import name
import os
from tkinter import *
import tkinter as tk
from random import sample
from itertools import count
from cgitb import text
from ast import Name
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('firebase-sdk.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://firepro-b51c3-default-rtdb.asia-southeast1.firebasedatabase.app/'
})


fileName = os.environ['ALLUSERSPROFILE'] + "\WebcamCap.txt"
cancel = False
is_on = True
is_close = True


def prompt_ok(event=0):
    global cancel, button, button1, button2, is_on
    cancel = True

    button.place_forget()
    # y_scroll = Scrollbar(mainWindow, orient=VERTICAL)
    # y_scroll.grid(row=0, column=1,  sticky=)
    PromtFrame = Frame(mainWindow, bd=4, pady=5)
    # titleFrame.place(x=0, y=350, width=850, height=60)
    PromtFrame.grid(row=3, column=0)
    # Frame for entries
    Eframe = Frame(PromtFrame, bd=4, relief=RIDGE, bg="#1e90ff")
    Eframe.grid(row=0, column=0)

    # inside Eframe
    Name = StringVar()
    nameLabel = Label(Eframe,
                      text="Name", font=('arial', 12, 'bold'), bg="#eb346b", fg="white", width=12)
    nameLabel.grid(row=0, column=0, padx=10, pady=10, sticky=(W))

    NameEntry = Entry(Eframe, textvariable=Name, font=('arial', 15, 'bold'))
    NameEntry.grid(row=0, column=1, padx=10, pady=10, sticky=(W))

    EId = StringVar()
    EIdLabel = Label(Eframe,
                     text="Employee Id", font=('arial', 12, 'bold'), bg="#eb346b", fg="white", width=12)
    EIdLabel.grid(row=1, column=0, padx=10, pady=10, sticky=(W))

    EIdEntry = Entry(Eframe, textvariable=EId, font=('arial', 15, 'bold'))
    EIdEntry.grid(row=1, column=1, padx=10, pady=10, sticky=(W))

    pword = StringVar()
    pwordLabel = Label(Eframe,
                       text="password", font=('arial', 12, 'bold'), bg="#eb346b", fg="white", width=12)
    pwordLabel.grid(row=2, column=0, padx=10, pady=10, sticky=(W))

    pwordEntry = Entry(Eframe, textvariable=pword, font=('arial', 15, 'bold'))
    pwordEntry.grid(row=2, column=1, padx=10, pady=10, sticky=(W))
    pwordEntry.config(show="*")
    is_on = True

    def showpass():
        global is_on
        if is_on:
            pwordEntry.config(show="")
            spbutton1.config(text="hide password")
            is_on = False
        else:
            pwordEntry.config(show="*")
            spbutton1.config(text="Show Password")
            is_on = True

    spbutton1 = tk.Button(Eframe, command=showpass, text="Show Password", font=('arial', 10, 'bold'),
                          bg="orange", fg="white")
    spbutton1.grid(row=3, column=0, padx=10, pady=10, sticky=(W))
    B1Frame = Frame(PromtFrame, bd=4, relief=RIDGE, bg="#9145ba", pady=5)
    # titleFrame.place(x=0, y=350, width=850, height=60)
    B1Frame.grid(row=1, column=0)
    button1 = tk.Button(B1Frame, command=saveAndExit, text="Good Image", font=('arial', 12, 'bold'),
                        bg="orange", fg="white")
    button2 = tk.Button(B1Frame, text="Try Again", command=resume, font=('arial', 12, 'bold'),
                        bg="orange", fg="white")
    button3 = tk.Button(B1Frame, text="Start process", command=run_proceduree, font=('arial', 12, 'bold'),
                        bg="orange", fg="white")
    # button1.place(anchor=tk.CENTER, relx=0.2, rely=0.9, width=150, height=50)
    button1.grid(row=0, column=0, padx=10, pady=10, sticky=(W))
    # button2.place(anchor=tk.CENTER, relx=0.8, rely=0.9, width=150, height=50)
    button2.grid(row=0, column=1, padx=10, pady=10, sticky=(W))
    button3.grid(row=0, column=2, padx=10, pady=10, sticky=(W))
    # button1.focus()

    def insert_it():

        db.child("names").push(Name.get())
        db.child("students").push(EId.get())
        db.child("freshers").push(pword.get())
        tk.messagebox.showinfo(title="registration info",
                               message="your registration is successful..")
    buttonI = tk.Button(mainWindow, command=insert_it, text="Insert in database", font=('arial', 12, 'bold'),
                        bg="orange", fg="white")
    buttonI.grid(row=2, column=2, padx=10, pady=10, sticky=(W))


def saveAndExit(event=0):
    global prevImg
    global count

    if (len(sys.argv) < 2):
        count = 0
        filepath = "output/imageCap"+str(count)+".png"
        count = count + 1
    else:
        filepath = sys.argv[1]

    print("Output file to: " + filepath)
    prevImg.save(filepath)
    shutil.copy(filepath, "sample_inputs")
    # mainWindow.quit()


def resume(event=0):
    global button1, button2, button, lmain, cancel

    cancel = False

    button1.place_forget()
    button2.place_forget()

    mainWindow.bind('<Return>', prompt_ok)
    # button.place(bordermode=tk.INSIDE, relx=0.5, rely=0.9,
    #              anchor=tk.CENTER, width=300, height=50)
    button.grid(row=0, column=0)
    lmain.after(10, show_frame)


def open_file():
    file_path = askopenfile(mode='r')
    if file_path is not None:
        pass


def run_proceduree():
    # os.startfile('finegerprint_pipline.py')
    # Or
    # subprocess.call("finegerprint_pipline.py")
    finegerprint_pipline.finger()
    # mainWindow.quit()


def changeCam(event=0, nextCam=-1):
    global camIndex, cap, fileName

    if nextCam == -1:
        camIndex += 1
    else:
        camIndex = nextCam
    del(cap)
    cap = cv2.VideoCapture(camIndex)

    # try to get a frame, if it returns nothing
    success, frame = cap.read()
    if not success:
        camIndex = 0
        del(cap)
        cap = cv2.VideoCapture(camIndex)

    f = open(fileName, 'w')
    f.write(str(camIndex))
    f.close()


try:
    f = open(fileName, 'r')
    camIndex = int(f.readline())
except:
    camIndex = 0

cap = cv2.VideoCapture(camIndex)
capWidth = cap.get(3)
capHeight = cap.get(4)

success, frame = cap.read()
if not success:
    if camIndex == 0:
        print("Error, No webcam found!")
        sys.exit(1)
    else:
        changeCam(nextCam=0)
        success, frame = cap.read()
        if not success:
            print("Error, No webcam found!")
            sys.exit(1)


def open_close_camera():
    global is_close

    def open_camera():
        global is_close
        # show_frame()
        mainWindow.bind('<Return>', prompt_ok)
        # button.place(bordermode=tk.INSIDE, relx=0.5, rely=0.9,
        #              anchor=tk.CENTER, width=300, height=50)
        lmain.after(10, show_frame)
        is_close = False

    def close_camera():
        global is_close
        cap.release()
        lmain.destroy()
        button.destroy()
        button_changeCam.destroy()
        button4.configure(text="Start Camera")
        is_close = True

    if(is_close):
        open_camera()
    else:
        close_camera()


mainWindow = tk.Tk(screenName="Camera Capture")
mainWindow.bind('<Escape>', lambda e: mainWindow.quit())
# main upper heading
title_register_Frame = Frame(mainWindow, bd=4, relief=RIDGE, bg="#fcba03")
# titleFrame.place(x=0, y=350, width=850, height=60)
title_register_Frame.grid(row=0, column=0)

# login------------------------------------------------------------------

title_login_Frame = Frame(mainWindow, bd=4, relief=RIDGE, bg="#fcba03")
# titleFrame.place(x=0, y=350, width=850, height=60)
title_login_Frame.grid(row=0, column=1)
title_in_frameLabel_l = Label(title_login_Frame, text="If you are existing user you can LOGIN here", font=(
    'arial', 12, 'bold'), bg="#e32dc5", fg="white", relief=RIDGE, padx=5, pady=5)
title_in_frameLabel_l.pack()
E_login_frame = Frame(mainWindow, bd=4, relief=RIDGE, bg="#1e90ff")
E_login_frame.grid(row=1, column=1)

# inside Eframe

EId1 = StringVar()
EId_login_Label = Label(E_login_frame,
                        text="Employee Id", font=('arial', 12, 'bold'), bg="#eb346b", fg="white", width=12)
EId_login_Label.grid(row=1, column=0, padx=10, pady=10, sticky=(W))

EId_login_Entry = Entry(E_login_frame, textvariable=EId1,
                        font=('arial', 15, 'bold'))
EId_login_Entry.grid(row=1, column=1, padx=10, pady=10, sticky=(W))
BFrame = Frame(mainWindow, bd=4, relief=RIDGE, bg="#1e90ff", pady=5)
# titleFrame.place(x=0, y=350, width=850, height=60)
BFrame.grid(row=2, column=0)

title_in_frameLabel = Label(title_register_Frame, text="If you are new user you can REGISTER here", font=(
    'arial', 12, 'bold'), bg="#e32dc5", fg="white", relief=RIDGE, padx=5, pady=5)
title_in_frameLabel.pack()
lmain = Label(mainWindow, compound=tk.CENTER,
              anchor=tk.CENTER, relief=tk.RAISED, height=250, width=250)
button = Button(BFrame, text="Capture", command=prompt_ok, font=('arial', 12, 'bold'),
                bg="orange", fg="white")
button4 = Button(BFrame, text="Close Camera", command=open_close_camera, font=('arial', 12, 'bold'),
                 bg="orange", fg="white")
button_changeCam = tk.Button(
    BFrame, text="Switch Camera", command=changeCam, font=('arial', 12, 'bold'),
    bg="orange", fg="white")


image_upload_t = Label(BFrame, font=('arial', 12, 'bold'), bg="white",
                       fg="black", pady=5, text="Upload FingerPrint Image")
image_upload_t.grid(row=1, column=0, padx=10, pady=15, sticky=(W))

image_chose_btn = Button(BFrame, text="Choose File", font=('arial', 12, 'bold'),
                         bg="orange", fg="white", command=lambda: open_file()
                         )
image_chose_btn.grid(row=1, column=1, pady=10, sticky=(W))
upld = Button(BFrame, text="Upload image", font=(
    'arial', 12, 'bold'), bg="orange", command=saveAndExit, fg="white")
upld.grid(row=1, column=2, pady=10, sticky=(W))
lmain.grid(row=1, column=0)
# button.place(bordermode=tk.INSIDE, relx=0.5, rely=0.9,
#              anchor=tk.CENTER, width=300, height=50)
button.grid(row=0, column=0, padx=10, pady=10, sticky=(W))
button4.grid(row=0, column=2, padx=10, pady=10, sticky=(W))

# button.focus()
# button_changeCam.place(bordermode=tk.INSIDE, relx=0.85,
#                        rely=0.1, anchor=tk.CENTER, width=150, height=50)
button_changeCam.grid(row=0, column=1, padx=10, pady=10, sticky=(W))


def show_frame():
    global cancel, prevImg, button

    _, frame = cap.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

    prevImg = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=prevImg)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    if not cancel:
        lmain.after(10, show_frame)


show_frame()
mainWindow.mainloop()
