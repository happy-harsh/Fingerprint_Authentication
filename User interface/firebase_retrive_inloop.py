from unittest import result
import firebase_admin
from firebase_admin import credentials, storage
import numpy as np
import cv2
import pyrebase
import urllib.request
from PIL import Image
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


def database_search(empID):
    cred = credentials.Certificate("firebase-sdk.json")
    bucket = storage.bucket()
    blob = bucket.get_blob(empID+".png")  # blob
    arr = np.frombuffer(blob.download_as_string(), np.uint8)  # array of bytes
    img = cv2.imdecode(arr, cv2.COLOR_BGR2BGR555)  # actual image

    cv2.imshow('image', img)
    cv2.waitKey(0)


results = db.child('user').get()
for result in results.each():
    employees = result.val()['url']
    f = urllib.request.urlopen(employees)
    img_PIL = Image.open(f)
    img_PIL.show()
