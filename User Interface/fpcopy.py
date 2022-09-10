# pip install --user --requirement requirements.txt
# python finegerprint_pipline.py

# import fingerprint_enhancer
import cv2 as cv
# from glob import glob
import os
from utils.poincare import calculate_singularities
from utils.segmentation import create_segmented_and_variance_images
from utils.normalization import normalize
from utils.gabor_filter import gabor_filter
from utils.frequency import ridge_freq
from utils import orientation
from utils.crossing_number import calculate_minutiaes
# from tqdm import tqdm
from utils.skeletonize import skeletonize
from walking import walking, walkonce, checkstable, mergeneighbors
from unittest import result
import firebase_admin
from firebase_admin import credentials, storage
import numpy
from numpy import asarray
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
# app = firebase_admin.initialize_app(
#     cred, {"storageBucket": "firepro-b51c3.appspot.com"})
db = firebase.database()
storage = firebase.storage()


def finger(fm):
    sample = cv.imread(fm, 0)
    cv2.imshow('my img', sample)
    sample = cv2.resize(sample, (256, 256))

    # stacked_img = numpy.stack((sample,)*3, axis=-1)

    best_score = 0

    filename = None

    image = None

    kp1, kp2, mp = None, None, None

    # sample = fingerprint_enhancer.enhance_Fingerprint(
    #     sample)		# enhance the fingerprint image
    # # cv.imshow('enhanced_image', sample)

# Matching -----------------------------------------------------
    results = db.child('user').get()
    for result in results.each():
        employees = result.val()['url']
        f = urllib.request.urlopen(employees)
        img_PIL = numpy.array(Image.open(f))
        fingerprint_image = img_PIL
        sift = cv.SIFT_create()

        keypoints_1, descriptors_1 = sift.detectAndCompute(sample, None)
        keypoints_2, descriptors_2 = sift.detectAndCompute(
            fingerprint_image, None)

        matches = cv.FlannBasedMatcher(dict(algorithm=1, trees=18), dict()).knnMatch(
            descriptors_1, descriptors_2, k=2)
        match_points = []

        for p, q in matches:
            if p.distance < 0.1*q.distance:
                match_points.append(p)

        keypoint = 0

        if len(keypoints_1) < len(keypoints_2):
            keypoint = len(keypoints_1)
        else:
            keypoint = len(keypoints_2)

        if len(match_points) / keypoint*180 > best_score:
            best_score = len(match_points) / keypoint*100
            filename = result.val()['UserID']
            image = fingerprint_image
            kp1, kp2, mp = keypoints_1, keypoints_2, match_points
            result = cv.drawMatches(
                sample, kp1, fingerprint_image, kp2, mp, None)
        else:
            print("Best Match Not Found")

    print("BEST MATCH Employee ID " + str(filename))

    print("SCORE: " + str(best_score))

    cv.imshow("Result", result)

    cv.waitKey(0)


# cv.destroyAllWindows()

# if __name__ == '__main__':
#     # open images
#     img_dir = './sample_inputs/*'
#     output_dir = './output/'
#     def open_images(directory):
#         images_paths = glob(directory)
#         return np.array([cv.imread(img_path,0) for img_path in images_paths])

#     images = open_images(img_dir)

#     # image pipeline
#     os.makedirs(output_dir, exist_ok=True)
#     for i, img in enumerate(tqdm(images)):
#         results = fingerprint_pipline(img)
#         cv.imwrite(output_dir+str(i)+'.png', results)
#         # cv.imshow('image pipeline', results); cv.waitKeyEx()
