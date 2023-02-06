import cv2
import numpy as np
import os

# NOTE this python script is not working

os.chdir("virotour/opencv/images")
# Load the images
images = []
for i in range(1, 8): 
    image = cv2.imread(f"{i}.jpg")
    #image = cv2.resize(image, (100,100))
    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    images.append(image)



# Create the feature detector and descriptor extractor
orb = cv2.ORB_create()

 

# Detect and extract features from the first image
keypoints_1, descriptors_1 = orb.detectAndCompute(images[0], None)

 

# Prepare an empty list to store the keypoints and descriptors of all images
keypoints = [keypoints_1]
descriptors = [descriptors_1]

 

# Detect and extract features from the remaining images
for i in range(1, 7): 
    keypoints_i, descriptors_i = orb.detectAndCompute(images[i], None)
    keypoints.append(keypoints_i)
    descriptors.append(descriptors_i)

 

# Match the descriptors of the first image with the descriptors of all other images
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = []
for i in range(1,7): 
    matches_i = bf.match(descriptors_1, descriptors[i])
    matches.append(matches_i)

 

# Find the homography matrix for each pair of images
homographies = []
for i in range(6): 
    src_pts = np.float32([keypoints_1[m.queryIdx].pt for m in matches[i]]).reshape(-1, 1, 2)
    dst_pts = np.float32([keypoints[i+1][m.trainIdx].pt for m in matches[i]]).reshape(-1, 1, 2)

 

    homography, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    homographies.append(homography)

 

# Create a black canvas for the final panoramic image
canvas_width = int(max([images[i].shape[1] for i in range(2)]) * 1.5)
canvas_height = int(sum([images[i].shape[0] for i in range(2)]) / 2)
panorama = np.zeros((canvas_height, canvas_width, 3), dtype="uint8")

 

# Copy the first image to the canvas
panorama[:images[0].shape[0], :images[0].shape[1]] = images[0]

 

# Warp the remaining images and place them on the canvas
pan_bottom = images[0].shape[0]
for i in range(6): 
    pan_top = pan_bottom
    pan_bottom = pan_top + images[i+1].shape[0]

 

    warped_image = cv2.warpPerspective(images[i+1], homographies[i], (canvas_width, canvas_height))

 
    #Commented out code not working
    # Create a mask for the warped image
    #mask = np.zeros_like(warped_image)
 

    #mask[pan_top:pan_bottom, :warped_image.shape[1]] = warped_image

 

    # Blend the warped image with the existing panorama using alpha blending
    #panorama = cv2.addWeighted(panorama, 1, mask, 1, 0)

 

# Crop the final panoramic image to remove black borders
pan_top, pan_bottom, pan_left, pan_right = 0, canvas_height, canvas_width, 0
for i in range(panorama.shape[0]):
    if np.sum(panorama[i, :, :]) != 0:
        pan_top = i
        break
for i in range(panorama.shape[0]-1, 0, -1):
    if np.sum(panorama[i, :, :]) != 0:
        pan_bottom = i
        break
for i in range(panorama.shape[1]):
    if np.sum(panorama[:, i, :]) != 0:
        pan_left = i
        break
for i in range(panorama.shape[1]-1, 0, -1):
    if np.sum(panorama[:, i, :]) != 0:
        pan_right = i
        break
panorama = panorama[pan_top:pan_bottom, pan_left:pan_right]

 

# Save the final panoramic image
cv2.imwrite("panorama.jpg", panorama)