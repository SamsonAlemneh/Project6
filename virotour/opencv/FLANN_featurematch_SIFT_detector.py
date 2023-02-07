import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import os

# Code sample from https://docs.opencv.org/4.x/dc/dc3/tutorial_py_matcher.html

os.chdir("virotour/opencv/images")
image1 = cv.imread('1.jpg',cv.IMREAD_GRAYSCALE)          # queryImage
image2 = cv.imread('2.jpg',cv.IMREAD_GRAYSCALE) # trainImage

# Images need to be 8 bit integer values for SIFT to work
img1 = cv.normalize(image1, None, 0, 255, cv.NORM_MINMAX).astype('uint8')
img2 = cv.normalize(image2, None, 0, 255, cv.NORM_MINMAX).astype('uint8')

# Initiate SIFT detector
sift = cv.SIFT_create(nfeatures=2000, nOctaveLayers=3, 
    contrastThreshold=0.03, edgeThreshold=10, sigma=1.6)
# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

# FLANN parameters
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks=50)   # or pass empty dictionary
flann = cv.FlannBasedMatcher(index_params,search_params)
matches = flann.knnMatch(des1,des2,k=2)
# Need to draw only good matches, so create a mask
matchesMask = [[0,0] for i in range(len(matches))]
pts1 = []
pts2 = []
# ratio test as per Lowe's paper
for i,(m,n) in enumerate(matches):
    if m.distance < 0.7*n.distance:
        matchesMask[i]=[1,0]
        pts2.append(kp2[m.trainIdx].pt)
        pts1.append(kp1[m.queryIdx].pt)
        draw_params = dict(matchColor = (0,255,0),
                   singlePointColor = (255,0,0),
                   matchesMask = matchesMask,
                   flags = cv.DrawMatchesFlags_DEFAULT)

pts1  = np.asarray(pts1)
pts2 = np.asarray(pts2)
#img3 = cv.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)




# Find the fundamental matrix by using RANSAC technique
F, mask = cv.findFundamentalMat(pts1,pts2,cv.FM_RANSAC)
#plt.imshow(img3,),plt.show()

# Calculate epilines
valid_matches_left = pts1[mask.ravel() == 1]
valid_matches_right = pts2[mask.ravel() == 1]
epilines_left = cv.computeCorrespondEpilines(valid_matches_right.reshape(-1, 1, 2), 2, F)
epilines_right = cv.computeCorrespondEpilines(valid_matches_left.reshape(-1, 1, 2), 2, F)
