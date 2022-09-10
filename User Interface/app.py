import firebase_retrive1
from cgitb import text
from itertools import count
from random import sample
from re import search
import tkinter as tk
from tkinter import *
import os
from unicodedata import name
import cv2
import sys
from PIL import Image, ImageTk
import numpy as np
import shutil
import finegerprint_pipline
import skelaton_process
from tkinter import filedialog
from tkinter.filedialog import askopenfile
import time
from tkinter import messagebox
import pyrebase
from PIL import Image, ImageTk
import firebase_admin
from firebase_admin import storage, credentials
import firebase_retrive1 as fr
import scaling
import biometricfetching
import fpcopy

# database related work-----------------
firebaseConfig = {
    "apiKey": "AIzaSyBDexR0M6wBSeAyfCUJhAkzC9Mi2zjmCNk",
    "authDomain": "firepro-b51c3.firebaseapp.com",
    "databaseURL": "https://firepro-b51c3-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "firepro-b51c3",
    "storageBucket": "firepro-b51c3.appspot.com",
    "messagingSenderId": "316408109669",
    "appId": "1:316408109669:web:103b3b60826b6acc43848c",
    "measurementId": "G-3XZ7JTSPYN",
    "serviceAccount": "firebase-sdk.json"
}
firebase = pyrebase.initialize_app(firebaseConfig)
cred = credentials.Certificate("firebase-sdk.json")
app = firebase_admin.initialize_app(
    cred, {"storageBucket": "firepro-b51c3.appspot.com"})
db = firebase.database()
storage = firebase.storage()
cred = credentials.Certificate("firebase-sdk.json")


# ---------------------------------------------


fileName = os.environ['ALLUSERSPROFILE'] + "\WebcamCap.txt"
cancel = False
is_on = True
is_close = True


def prompt_ok(event=0):
    global cancel, button, button1, button2, is_on
    cancel = True

    def Biofinger():
        path = biometricfetching.biometric_captr()
        N = Name.get()
        UID = EId.get()
        Password = pword.get()
        filename = skelaton_process.finger(path)
        url = storage.child(UID+".png").get_url(None)
        data = {"Name": N,
                "UserID": UID,
                "Password": Password,
                "url": url
                }
        db.child("user").push(data)

        storage.child(UID + ".png").put(filename)
        messagebox.showinfo("Information", "Data Inserted")

    def data_with_upload():
        N = Name.get()
        UID = EId.get()
        Password = pword.get()
        filename = skelaton_process.finger(upload_file())
        storage.child(UID + ".png").put(filename)
        url = storage.child(UID+".png").get_url(None)
        data = {"Name": N,
                "UserID": UID,
                "Password": Password,
                "url": url
                }
        db.child("user").push(data)
        messagebox.showinfo("Information", "Data Inserted")

    def data():
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
        scaling.resizing()
        skelaton_process.finger(filepath)
        # mainWindow.quit()
        N = Name.get()
        UID = EId.get()
        Password = pword.get()
        storage.child(UID + ".png").put(filepath)
        url = storage.child(UID+".png").get_url(None)
        data = {"Name": N,
                "UserID": UID,
                "Password": Password,
                "url": url
                }
        db.child("user").push(data)
        messagebox.showinfo("Information", "Data Inserted")

    # button.place_forget()
    # y_scroll = Scrollbar(mainWindow, orient=VERTICAL)
    # y_scroll.grid(row=0, column=1,  sticky=)
    PromtFrame = Frame(mainWindow, bd=4, pady=5)
    # titleFrame.place(x=0, y=350, width=850, height=60)
    PromtFrame.place(x=410, y=140)
    # Frame for entries
    Eframe = Frame(PromtFrame, bd=4, relief=RIDGE, bg="#1e90ff")
    Eframe.grid(row=0, column=0)

    # inside Eframe
    Name = StringVar()
    nameLabel = Label(Eframe,
                      text="Name", font=('arial', 11, 'bold'), bg="#eb346b", fg="white", width=12)
    nameLabel.grid(row=0, column=0, padx=10, pady=10, sticky=(W))

    NameEntry = Entry(Eframe, textvariable=Name, font=('arial', 11, 'bold'))
    NameEntry.grid(row=0, column=1, padx=10, pady=10, sticky=(W))

    EId = StringVar()
    EIdLabel = Label(Eframe,
                     text="Employee Id", font=('arial', 11, 'bold'), bg="#eb346b", fg="white", width=12)
    EIdLabel.grid(row=1, column=0, padx=10, pady=10, sticky=(W))

    EIdEntry = Entry(Eframe, textvariable=EId, font=('arial', 11, 'bold'))
    EIdEntry.grid(row=1, column=1, padx=10, pady=10, sticky=(W))

    pword = StringVar()
    pwordLabel = Label(Eframe,
                       text="password", font=('arial', 11, 'bold'), bg="#eb346b", fg="white", width=12)
    pwordLabel.grid(row=2, column=0, padx=10, pady=10, sticky=(W))

    pwordEntry = Entry(Eframe, textvariable=pword, font=('arial', 11, 'bold'))
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

    def clearTextInput():
        NameEntry.delete(0, END)
        EIdEntry.delete(0, END)
        pwordEntry.delete(0, END)

    spbutton1 = tk.Button(Eframe, command=showpass, text="Show Password", font=('arial', 10, 'bold'),
                          bg="orange", fg="white")
    clearb = tk.Button(Eframe, command=clearTextInput, text="clear", font=('arial', 10, 'bold'),
                       bg="orange", fg="white")
    B1Frame = Frame(PromtFrame, bd=4, relief=RIDGE, bg="#cfcccc", pady=5)
    # titleFrame.place(x=0, y=350, width=850, height=60)
    B1Frame.grid(row=1, column=0)
    savebutton = tk.Button(B1Frame, command=data, text="register User ", font=('arial', 12, 'bold'),
                           bg="orange", fg="white")
    savebutton1 = tk.Button(UFrame, command=data_with_upload, text="register with uploaded image", font=('arial', 12, 'bold'),
                            bg="orange", fg="white")
    match = tk.Button(UFrame, command=matching_finger, text="Fingerprint matching", font=('arial', 12, 'bold'),
                      bg="orange", fg="white")

    loginbuttonbio = Button(mainWindow, text="register with biometric", command=Biofinger, font=('arial', 12, 'bold'),
                            bg="orange", fg="white")
    loginbuttonbio.place(x=180, y=550)

    spbutton1.grid(row=3, column=0, padx=10, pady=10, sticky=(W))
    savebutton.grid(row=0, column=0, padx=10, pady=10, sticky=(W))
    savebutton1.grid(row=0, column=3, padx=10, pady=10, sticky=(W))
    match.grid(row=0, column=4, padx=10, pady=10, sticky=(W))
    clearb.grid(row=3, column=1, padx=10, pady=10, sticky=(W))
    # button1 = tk.Button(B1Frame, command=saveAndExit, text="Good Image", font=('arial', 12, 'bold'),
    #                     bg="orange", fg="white")
    button2 = tk.Button(B1Frame, text="Try Again", command=resume, font=('arial', 12, 'bold'),
                        bg="orange", fg="white")
    button3 = tk.Button(B1Frame, text="Start process", command=run_proceduree, font=('arial', 12, 'bold'),
                        bg="orange", fg="white")
    # button1.place(anchor=tk.CENTER, relx=0.2, rely=0.9, width=150, height=50)
    # button1.grid(row=0, column=0, padx=10, pady=10, sticky=(W))
    # button2.place(anchor=tk.CENTER, relx=0.8, rely=0.9, width=150, height=50)
    button2.grid(row=0, column=1, padx=10, pady=10, sticky=(W))
    button3.grid(row=0, column=2, padx=10, pady=10, sticky=(W))
    # button1.focus()
    PromtLoginFrame = Frame(mainWindow)
    # titleFrame.place(x=0, y=350, width=850, height=60)
    PromtLoginFrame.place(x=820, y=140)
    E_login_frame = Frame(PromtLoginFrame, bd=4, relief=RIDGE, bg="#1e90ff")
    E_login_frame.grid(row=0, column=0, padx=10, pady=10, sticky=(W))

    # inside Eframe

    # EId1 = StringVar()
    # EId_login_Label = Label(E_login_frame,
    #                         text="Employee Id", font=('arial', 11, 'bold'), bg="#eb346b", fg="white", width=12)
    # EId_login_Label.grid(row=1, column=0, padx=10, pady=10, sticky=(W))

    # EId_login_Entry = Entry(E_login_frame, textvariable=EId1,
    #                         font=('arial', 11, 'bold'))
    # EId_login_Entry.grid(row=1, column=1, padx=10, pady=10, sticky=(W))

    # inside Eframe

    EId1 = StringVar()
    EId1Label = Label(E_login_frame,
                      text="Employee Id", font=('arial', 11, 'bold'), bg="#eb346b", fg="white", width=12)
    EId1Label.grid(row=0, column=0, padx=10, pady=10, sticky=(W))

    EId1Entry = Entry(E_login_frame, textvariable=EId1,
                      font=('arial', 11, 'bold'))
    EId1Entry.grid(row=0, column=1, padx=10, pady=10, sticky=(W))

    B1LFrame = Frame(PromtLoginFrame, bd=4, relief=RIDGE, bg="#9145ba", pady=5)
    # titleFrame.place(x=0, y=350, width=850, height=60)
    B1LFrame.grid(row=1, column=0)

    def searchit():
        num = EId1.get()
        firebase_retrive1.database_search(num)
        # messagebox.showinfo("Information", "Login successfully")
    savebutton = tk.Button(B1LFrame, command=searchit, text="Login", font=('arial', 12, 'bold'),
                           bg="orange", fg="white")
    savebutton.grid(row=0, column=0, padx=10, pady=10, sticky=(W))
    tbutton = tk.Button(B1LFrame, text="Try Again", command=run_proceduree, font=('arial', 12, 'bold'),
                        bg="orange", fg="white")
    # button1.place(anchor=tk.CENTER, relx=0.2, rely=0.9, width=150, height=50)
    # button1.grid(row=0, column=0, padx=10, pady=10, sticky=(W))
    # button2.place(anchor=tk.CENTER, relx=0.8, rely=0.9, width=150, height=50)
    tbutton.grid(row=0, column=1, padx=10, pady=10, sticky=(W))
    # button1.focus()


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


def upload_file():
    global filename, img
    f_types = [('Jpg Files', '*.jpg'),
               ('PNG Files', '*.png'),
               ('Tif Files', '*.tif'),
               ('bmp Files', '*.bmp')]   # type of files to select
    filename = tk.filedialog.askopenfilename(filetypes=f_types)

    img = Image.open(filename)  # read the image file
    img = img.resize((190, 190))  # new width & height
    img = ImageTk.PhotoImage(img)
    e1 = tk.Label(mainWindow)
    e1.place(x=10, y=549)
    e1.image = img
    e1['image'] = img
    return filename


def matching_finger():
    filename = skelaton_process.finger(upload_file())
    fpcopy.finger(filename)


def resume(event=0):
    global button1, button2, button, lmain, cancel

    cancel = False

    # button1.place_forget()
    # button2.place_forget()

    mainWindow.bind('<Return>', prompt_ok)
    button.place(x=50, y=430)
    lmain.after(10, show_frame)


def open_file():
    file_path = askopenfile(mode='r')
    if file_path is not None:
        pass


def run_proceduree():
    # os.startfile('finegerprint_pipline.py')
    # Or
    # subprocess.call("finegerprint_pipline.py")
    # finegerprint_pipline.finger()
    skelaton_process.finger()
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


# def open_close_camera():
    # global is_close

    def open_camera():
        global is_close
        # show_frame()
        mainWindow.bind('<Return>', prompt_ok)
        # button.place(bordermode=tk.INSIDE, relx=0.5, rely=0.9,
        #              anchor=tk.CENTER, width=300, height=50)
        lmain.after(10, show_frame)
        is_close = False

    # def close_camera():
    #     global is_close
    #     cap.release()
    #     lmain.destroy()
    #     button.destroy()
    #     button_changeCam.destroy()
    #     button4.configure(text="Start Camera")
    #     is_close = True

    # if(is_close):
    #     open_camera()
    # else:
    #     close_camera()


mainWindow = tk.Tk(screenName="Camera Capture")
mainWindow.bind('<Escape>', lambda e: mainWindow.quit())
mainWindow.geometry("1200x1200")
# main upper heading
title_register_Frame = Frame(mainWindow, bd=4, relief=RIDGE, bg="#fcba03")
# titleFrame.place(x=0, y=350, width=850, height=60)
title_register_Frame.place(x=410, y=75)

# login------------------------------------------------------------------

title_login_Frame = Frame(mainWindow, bd=4, relief=RIDGE, bg="#fcba03")
# titleFrame.place(x=0, y=350, width=850, height=60)
title_login_Frame.place(x=820, y=75)
title_in_frameLabel_l = Label(title_login_Frame, text="If you are existing user you can LOGIN here", font=(
    'arial', 12, 'bold'), bg="#e32dc5", fg="white", relief=RIDGE, padx=5, pady=5)
title_in_frameLabel_l.pack()

BFrame = Frame(mainWindow, bd=4, pady=5)
# titleFrame.place(x=0, y=350, width=850, height=60)


title_in_frameLabel = Label(title_register_Frame, text="If you are new user you can REGISTER here", font=(
    'arial', 12, 'bold'), bg="#e32dc5", fg="white", relief=RIDGE, padx=5, pady=5)
title_in_frameLabel.pack()
lmain = Label(mainWindow, compound=tk.CENTER,
              anchor=tk.CENTER, relief=tk.RAISED, height=350, width=250)
title_label = Label(mainWindow, text="XCODERS_ETX FingerPrint Authantication Application", bg="#F67280", fg="white", font=('arial', 23, 'bold'),
                    anchor=tk.CENTER)
title_label.place(x=300, y=10)
button = Button(mainWindow, text="Capture", command=prompt_ok, font=('arial', 12, 'bold'),
                bg="orange", fg="white")
button4 = Button(BFrame, text="Close Camera", font=('arial', 12, 'bold'),
                 bg="orange", fg="white")
button_changeCam = tk.Button(
    mainWindow, text="Switch Camera", command=changeCam, font=('arial', 12, 'bold'),
    bg="orange", fg="white")

UFrame = Frame(mainWindow, bd=4, bg="yellow")
# titleFrame.place(x=0, y=350, width=850, height=60)
image_upload_t = Label(UFrame, font=('arial', 12, 'bold'), bg="sky blue",
                       fg="black", pady=5, text="Upload FingerPrint Image")
image_upload_t.grid(row=0, column=0, padx=10, pady=10, sticky=(W))

image_chose_btn = Button(UFrame, text="Choose File", font=('arial', 12, 'bold'),
                         bg="orange", fg="white", command=upload_file
                         )
image_chose_btn.grid(row=0, column=1, pady=10, sticky=(W))
upld = Button(UFrame, text="Upload image", font=(
    'arial', 12, 'bold'), bg="orange", command=prompt_ok, fg="white")
upld.grid(row=0, column=2, padx=5, sticky=(W))
lmain.place(x=0, y=60)
# button.place(bordermode=tk.INSIDE, relx=0.5, rely=0.9,
#              anchor=tk.CENTER, width=300, height=50)
button.place(x=50, y=430)
# button4.grid(row=3, column=0, padx=10, pady=10, sticky=(W))

# button.focus()
# button_changeCam.place(bordermode=tk.INSIDE, relx=0.85,
#                        rely=0.1, anchor=tk.CENTER, width=150, height=50)
button_changeCam.place(x=185, y=430)
UFrame.place(x=0, y=485)


biobutton = Button(mainWindow, text="capture with bimetric", command=prompt_ok, font=('arial', 12, 'bold'),
                   bg="orange", fg="white")

registerbuttonbio = Button(mainWindow, text="login with biometric", command=prompt_ok, font=('arial', 12, 'bold'),
                           bg="orange", fg="white")
biobutton.place(x=0, y=550)
# registerbuttonbio.place(x=400, y=550)


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
