# pip install --user --requirement requirements.txt
# python finegerprint_pipline.py


from ast import Return
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


def finger(filename):
    sample = cv.imread(
        filename, 0)

    cv.imshow('my image', sample)
    sample = cv.resize(sample, (256, 256))

    blur = cv.GaussianBlur(sample, (3, 3), 0)
    # cv.imshow('smooth', blur)

    thresh = cv.adaptiveThreshold(blur, 255,
                                  cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 21, 10)
    # cv.imshow("Mean Adaptive Thresholding", thresh)
    blur = cv.GaussianBlur(thresh, (3, 3), 0)
    # cv.imshow('smooth', blur)

    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    image_sharp = cv.filter2D(src=blur, ddepth=-1, kernel=kernel)
    # cv.imshow('sharp', image_sharp)

    # normalization - removes the effects of sensor noise and finger pressure differences.
    normalized_img = normalize(image_sharp, float(100), float(100))
    # cv.imshow('normalise', normalized_img)

    # clahe = cv.createCLAHE(clipLimit=60, tileGridSize=(8, 8))
    # cl = clahe.apply(normalized_img)
    # cv.imshow('clahe', cl)

    # otsu
    threshold_img = normalized_img
    _, threshold_im = cv.threshold(normalized_img, 200, 255, cv.THRESH_OTSU)
    # cv.imshow('otsu', threshold_im)

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
    # cv.imshow('orientation', orientation_img)

    # find the overall frequency of ridges in Wavelet Domain
    freq = ridge_freq(normim, mask, angles, block_size,
                      kernel_size=5, minWaveLength=5, maxWaveLength=15)

    # create gabor filter and do the actual filtering
    gabor_img = gabor_filter(normim, angles, freq)
    # cv.imshow('gabor img', gabor_img)

    blur = cv.GaussianBlur(gabor_img, (5, 5), 0)
    # cv.imshow('smooth', blur)

    ret, thresh2 = cv.threshold(blur, 150, 255, cv.THRESH_BINARY_INV)

    skeleton = cv.ximgproc.thinning(
        thresh2, thinningType=cv.ximgproc.THINNING_ZHANGSUEN)
    cv.imshow('skeleton', skeleton)
    file = "output/imageCap0.png"
    # return file
    cv.imwrite(file, skeleton)
    cv.waitKey(100)
    cv.destroyAllWindows()
    filestr = str(file)
    return filestr
