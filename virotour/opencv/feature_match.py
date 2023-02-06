# Note this was code that Professor MIR posted in the Joint Collaboration which was then converted to python.
# It takes in two hard-coded images for processing


from blending import Blender
import glob
import cv2
import numpy as np
import os
from tqdm import tqdm
import itertools


def remove_filename_from_file(input):
	return os.path.splitext(input)[0]


def compare(imageName1, imageName2, nFeaturesReturn = 30):
	'''
	takes in two images, and returns a set of correspondences between the two images matched using ORB features,
	 sorted from best to worst match using an L2 norm distance.
	'''
	# Currently hard-coded images.
	# This will have to be updated to handled many images, not sure how the algorithm would handle that.
	img1 = cv2.imread(imageName1)
	img2 = cv2.imread(imageName2)
	id1 = remove_filename_from_file(imageName1)
	id2 = remove_filename_from_file(imageName2)

	kp1, des1 = orb.detectAndCompute(img1,None)
	kp2, des2 = orb.detectAndCompute(img2,None)
	matches = bf.match(des1,des2)
	matches = sorted(matches, key = lambda x:x.distance)
	correspondences = []
	for match in matches:
		correspondences.append((kp1[match.queryIdx].pt, kp2[match.trainIdx].pt))
	print("{} v. {} found {} matches".format(id1, id2, len(correspondences)))
	# src = np.float32([ m[0] for m in correspondences[:nFeaturesReturn] ]).reshape(-1,1,2)
	# dst = np.float32([ m[1] for m in correspondences[:nFeaturesReturn] ]).reshape(-1,1,2)
	return np.array(correspondences[:nFeaturesReturn])

if __name__ == "__main__":
	os.chdir("./images")
	orb = cv2.ORB_create()
	bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

	num_images = 7
	images = ["{}.jpg".format(x) for x in range(1, num_images + 1)]
	print(images)
	for i, j in itertools.product(images, images):
		if i != j:
			compare(i, j)
			# break
