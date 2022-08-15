# pip install --user --requirement requirements.txt
# python finegerprint_pipline.py

# import fingerprint_enhancer
import cv2 as cv
# from glob import glob
import os
import numpy as np
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


sample = cv.imread('sample_inputs/test.tiff', 0)

stacked_img = np.stack((sample,)*3, axis=-1)

detect_SP = walking(sample)

if min(detect_SP['core'].shape) != 0:
    for i in range(0, detect_SP['core'].shape[0]):
        centre = (int(detect_SP['core'][i, 0]), int(detect_SP['core'][i, 1]))
        stacked_img = cv.circle(stacked_img, centre, 10, (0, 0, 255), 2)

if min(detect_SP['delta'].shape) != 0:
    for j in range(0, detect_SP['delta'].shape[0]):
        x = int(detect_SP['delta'][j, 0])
        y = int(detect_SP['delta'][j, 1])
        pts = np.array([[x, y-10], [x-9, y+5], [x+9, y+5]])
        stacked_img = cv.polylines(stacked_img, [pts], True, (0, 255, 0), 2)

# cv.imwrite('results/img1.bmp', stacked_img)  # make changes here
cv.imshow('core point', stacked_img)
print(detect_SP)


block_size = 16
# pipe line picture re https://www.cse.iitk.ac.in/users/biometrics/pages/111.JPG
# normalization -> orientation -> frequency -> mask -> filtering

# normalization - removes the effects of sensor noise and finger pressure differences.
normalized_img = normalize(sample, float(100), float(100))
cv.imshow('normalise', normalized_img)
# color threshold
# threshold_img = normalized_img
# _, threshold_im = cv.threshold(normalized_img,127,255,cv.THRESH_OTSU)
# cv.imshow('color_threshold', normalized_img); cv.waitKeyEx()

# ROI and normalisation
(segmented_img, normim, mask) = create_segmented_and_variance_images(
    normalized_img, block_size, 0.2)

# orientations
angles = orientation.calculate_angles(
    normalized_img, W=block_size, smoth=False)
orientation_img = orientation.visualize_angles(
    segmented_img, mask, angles, W=block_size)
cv.imshow('orientation', orientation_img)

# find the overall frequency of ridges in Wavelet Domain
freq = ridge_freq(normim, mask, angles, block_size,
                  kernel_size=5, minWaveLength=5, maxWaveLength=15)

# create gabor filter and do the actual filtering
gabor_img = gabor_filter(normim, angles, freq)
cv.imshow('gabor img', gabor_img)

# thinning oor skeletonize
thin_image = skeletonize(gabor_img)
cv.imshow('thinning', thin_image)

# minutias
minutias = calculate_minutiaes(thin_image)
cv.imshow('minutias', minutias)

# singularities
singularities_img = calculate_singularities(
    thin_image, angles, 1, block_size, mask)
cv.imshow('thinning', thin_image)


best_score = 0

filename = None

image = None

kp1, kp2, mp = None, None, None

# sample = fingerprint_enhancer.enhance_Fingerprint(
#     sample)		# enhance the fingerprint image
# # cv.imshow('enhanced_image', sample)

# Matching -----------------------------------------------------
for file in [file for file in os.listdir("output")]:
    fingerprint_image = cv.imread("output/" + file)
    sift = cv.SIFT_create()

    keypoints_1, descriptors_1 = sift.detectAndCompute(sample, None)
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
        result = cv.drawMatches(sample, kp1, fingerprint_image, kp2, mp, None)


print("BEST MATCH: " + str(filename))

print("SCORE: " + str(best_score))

cv.imshow("Result", result)


# # visualize pipeline stage by stage
# output_imgs = [sample, normalized_img, segmented_img,
#                orientation_img, gabor_img, thin_image, minutias, singularities_img]
# for i in range(len(output_imgs)):
#     if len(output_imgs[i].shape) == 2:
#         output_imgs[i] = cv.cvtColor(output_imgs[i], cv.COLOR_GRAY2RGB)
# results = np.concatenate([np.concatenate(output_imgs[:4], 1), np.concatenate(
#     output_imgs[4:], 1)]).astype(np.uint8)
# cv.imshow('res', results)
#     return results

cv.waitKeyEx()

cv.destroyAllWindows()


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
