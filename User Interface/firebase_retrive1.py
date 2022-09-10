from unittest import result
import firebase_admin
from firebase_admin import credentials, storage
import numpy as np
import cv2
import pyrebase


def database_search(empID):
    cred = credentials.Certificate("firebase-sdk.json")
    bucket = storage.bucket()
    blob = bucket.get_blob(empID+".png")  # blob
    arr = np.frombuffer(blob.download_as_string(), np.uint8)  # array of bytes
    img = cv2.imdecode(arr, cv2.COLOR_BGR2BGR555)  # actual image

    cv2.imshow('image', img)
    cv2.waitKey(0)
