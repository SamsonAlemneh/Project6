# Note this was code that Professor MIR posted in the Joint Collaboration which was then converted to python.
# It takes in two hard-coded images for processing


import cv2
import numpy as np
import os

GOOD_MATCH_PERCENT = 0.15 


# Currently hard-coded images.  
# This will have to be updated to handled many images, not sure how the algorithm would handle that.
os.chdir("virotour/opencv/images")
image1 = cv2.imread("1.jpg")
image2 = cv2.imread("2.jpg")

    
# Convert the images to grayscale
imgGray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
imgGray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

# Detect ORB features and compute descriptors
orb = cv2.ORB_create()
keypoints_1, descriptors_1 = orb.detectAndCompute(imgGray1, None)
keypoints_2, descriptors_2 = orb.detectAndCompute(imgGray2, None)

# Match features
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(descriptors_1, descriptors_1)
matches = sorted(matches, key=lambda x: x.distance)
matched_image = cv2.drawMatches(image1, keypoints_1, image2, keypoints_2, matches, None, flags=2)

#Find the best matches
numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
matches = matches[:numGoodMatches]

    

# Filter out the good matches   
matched_image = cv2.drawMatches(image1, keypoints_1, image2, keypoints_2, matches, None)
cv2.imwrite("matches.jpg", matched_image)

# Extract location of good matches
points1 = np.zeros((len(matches), 2), dtype=np.float32)
points2 = np.zeros((len(matches), 2), dtype=np.float32)

# Extract the keypoints from the good matches
for i, match in enumerate(matches):
    points1[i, :] = keypoints_1[match.queryIdx].pt
    points2[i, :] = keypoints_2[match.trainIdx].pt


# Find the homography matrix
h, mask = cv2.findHomography(points2, points1, cv2.RANSAC)
    

# Warp the second image to align with the first image
# I don't think this part is working properly but do we need it?
height, width = image2.shape[:2]
mod_photo = cv2.warpPerspective(image2, h, (width, height))

# Add hotspots to transition between the two images
# Code to add hotspots goes here 
# This is not done.  Not sure what to do here?

# Show the result   
# The transformed image is not quite working
cv2.imshow("Result",mod_photo) 
cv2.imwrite("panorama.jpg", mod_photo)
