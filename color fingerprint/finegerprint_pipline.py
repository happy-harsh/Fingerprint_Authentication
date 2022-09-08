import cv2
import cv2 as cv
import os
import numpy as np
from utils.poincare import calculate_singularities
from utils.segmentation import create_segmented_and_variance_images
from utils.normalization import normalize
from utils.gabor_filter import gabor_filter
from utils.frequency import ridge_freq
from utils import orientation
from utils.crossing_number import calculate_minutiaes

# after registrating input your color image
# this code will match the color fingerprint kept in ip folder with the one in the skeleton form of itself
image = cv.imread(
    'ip/r_mid_left.jpeg')


def center_crop(img, dim):
    """Returns center cropped image
    Args:
    img: image to be center cropped
    dim: dimensions (width, height) to be cropped
    """
    width, height = img.shape[1], img.shape[0]

    # process crop width and height for max available dimension
    crop_width = dim[0] if dim[0] < img.shape[1] else img.shape[1]
    crop_height = dim[1] if dim[1] < img.shape[0] else img.shape[0]
    mid_x, mid_y = int(width/2), int(height/2)
    cw2, ch2 = int(crop_width/2), int(crop_height/2)
    crop_img = img[mid_y-ch2:mid_y+ch2, mid_x-cw2:mid_x+cw2]
    return crop_img


# image = cv2.imread('natfig9.jpeg')

ccrop_img = center_crop(image, (300, 500))
# scale_img = scale_image(image, factor=1.5)

cv2.imshow("crop.jpg", ccrop_img)
# cv2.imshow("scaled.jpg", scale_img)


# Removing the background
height, width = ccrop_img.shape[:2]

# Create a mask holder
mask = np.zeros(ccrop_img.shape[:2], np.uint8)

# Grab Cut the object
bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)

# Hard Coding the Rect… The object must lie within this rect.
rect = (15, 15, width-20, height-15)
cv2.grabCut(ccrop_img, mask, rect, bgdModel,
            fgdModel, 25, cv2.GC_INIT_WITH_RECT)
mask = np.where((mask == 2) | (mask == 0), 0, 1).astype("uint8")
img1 = ccrop_img*mask[:, :, np.newaxis]

# Get the background
background = cv2.absdiff(ccrop_img, img1)

# Change all pixels in the background that are not black to white
background[np.where((background > [0, 0, 0]).all(axis=2))] = [255, 255, 255]

# Add the background and the image
final = background + img1

# To be done – Smoothening the edges….
# final1 = cv2.resize(final, (500, 500))
cv2.imshow('image', final)
# cv2.imwrite("input.jpg", final1)


gray_image = cv2.cvtColor(final, cv2.COLOR_BGR2GRAY)
cv2.imshow('Grayscale', gray_image)

# normalization - removes the effects of sensor noise and finger pressure differences.
normalized_img = normalize(gray_image, float(100), float(100))
cv.imshow('normalise', normalized_img)


clahe = cv.createCLAHE(clipLimit=80, tileGridSize=(130, 130))
cl = clahe.apply(normalized_img)
cv.imshow('clahe', cl)


blur = cv.GaussianBlur(cl, (3, 3), 0)
cv.imshow('smooth', blur)


thresh = cv.adaptiveThreshold(blur, 255,
                              cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 21, 10)
cv.imshow("Mean Adaptive Thresholding", thresh)


blur = cv.GaussianBlur(thresh, (3, 3), 0)
cv.imshow('smooth', blur)


# # normalization -> orientation -> frequency -> mask -> filtering


kernel = np.array([[0, -1, 0],
                   [-1, 5, -1],
                   [0, -1, 0]])
image_sharp = cv.filter2D(src=blur, ddepth=-1, kernel=kernel)
cv.imshow('sharp', image_sharp)


# otsu
_, threshold_im = cv.threshold(image_sharp, 200, 255, cv.THRESH_OTSU)
cv.imshow('otsu', threshold_im)

# threshold_im = cv.adaptiveThreshold(normalized_img, 255,
#                                     cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 21, 10)
# cv.imshow("Mean Adaptive Thresholding", threshold_im)

block_size = 16
# ROI and normalisation
(segmented_img, normim, mask) = create_segmented_and_variance_images(
    threshold_im, block_size, 0.2)

# orientations
angles = orientation.calculate_angles(
    threshold_im, W=block_size, smoth=False)
orientation_img = orientation.visualize_angles(
    segmented_img, mask, angles, W=block_size)
cv.imshow('orientation', orientation_img)

# find the overall frequency of ridges in Wavelet Domain
freq = ridge_freq(normim, mask, angles, block_size,
                  kernel_size=5, minWaveLength=5, maxWaveLength=15)

# create gabor filter and do the actual filtering
gabor_img = gabor_filter(normim, angles, freq)
cv.imshow('gabor img', gabor_img)

blur = cv.GaussianBlur(gabor_img, (5, 5), 0)
cv.imshow('smooth', blur)

ret, thresh2 = cv.threshold(blur, 150, 255, cv.THRESH_BINARY_INV)


# # thinning oor skeletonize
# thin_image = skeletonize(gabor_img)
# cv.imshow('thinning', thin_image)

skeleton = cv.ximgproc.thinning(
    thresh2, thinningType=cv.ximgproc.THINNING_ZHANGSUEN)
cv.imshow('skeleton', skeleton)
# cv.imwrite('db/rmf1.jpeg', skeleton)

# thresh1 = cv.adaptiveThreshold(skeleton, 255,
#                                cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 15, 10)
# cv.imshow("Mean Adaptive Thresholding", thresh1)
#cv.imwrite('db/llf.jpeg', skeleton)
# inversion = np.invert(thresh1)
# cv.imshow("inversion", inversion)
# # minutias
minutias = calculate_minutiaes(skeleton)
# file = 'realminu.jpg'
# cv.imshow('minutias', minutias)


# singularities
singularities_img = calculate_singularities(
    skeleton, angles, 1, block_size, mask)
cv.imshow('singularities', singularities_img)

cv.waitKeyEx()

# matching code---------------------------------------------------------------------------------------------------


best_score = 0

filename = None

image = None

kp1, kp2, mp = None, None, None

result = None


for file in [file for file in os.listdir("db")]:
    fingerprint_image = cv.imread("db/" + file)
    sift = cv.SIFT_create()

    keypoints_1, descriptors_1 = sift.detectAndCompute(skeleton, None)
    keypoints_2, descriptors_2 = sift.detectAndCompute(fingerprint_image, None)

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
        filename = file
        image = fingerprint_image
        kp1, kp2, mp = keypoints_1, keypoints_2, match_points
        result = cv.drawMatches(
            skeleton, kp1, fingerprint_image, kp2, mp, None)


print("BEST MATCH: " + str(filename))

print("SCORE: " + str(best_score))

cv.imshow("Result", result)


cv.waitKeyEx()

cv.destroyAllWindows()
