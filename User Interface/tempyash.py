from tkinter import *
from tkinter import messagebox
import pyrebase

root = Tk()
root.geometry("480x240")
root.title("Fingerprint App")

firebaseConfig = {
    "apiKey": "AIzaSyBDexR0M6wBSeAyfCUJhAkzC9Mi2zjmCNk",
    "authDomain": "firepro-b51c3.firebaseapp.com",
    "databaseURL": "https://firepro-b51c3-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "firepro-b51c3",
    "storageBucket": "firepro-b51c3.appspot.com",
    "messagingSenderId": "316408109669",
    "appId": "1:316408109669:web:103b3b60826b6acc43848c",
    "measurementId": "G-3XZ7JTSPYN"
}
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()


def data():

    Name = e1.get()
    UserID = e2.get()
    Password = e3.get()
    data = {"Name": Name,
            "UserID": UserID,
            "Password": Password
            }
    db.child("user").push(data)
    messagebox.showinfo("Information", "Data Inserted")


l1 = Label(root, text="Fingerprint App", font="time 17 bold")
l1.grid(row=0, column=0)

e1 = Entry(root, text="Name", font="time 17 bold")
e1.grid(row=1, column=0)

e2 = Entry(root, text="User ID", font="time 17 bold")
e2.grid(row=2, column=0)

e3 = Entry(root, text="Password", font="time 17 bold")
e3.grid(row=3, column=0)

# e2=Entry(root,width=27,bd=2,font="time 13 bold")
# e2.place(x=200,y=93)

button = Button(root, text="Submit", command=data, fg="black",
                bg="Orange", font="time 15 bold", width=34)
button.grid(row=4, column=0)

root.mainloop()
