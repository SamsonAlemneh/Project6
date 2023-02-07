# Note this was code that Professor MIR posted in the Joint Collaboration which was then converted to python.
# It takes in two hard-coded images for processing

import cv2
import numpy as np
import os
import itertools


def remove_filename_from_file(input):
    return os.path.splitext(input)[0]


def drawlines(img1, img2, lines, pts1, pts2):
    ''' img1 - image on which we draw the epilines for the points in img2
        lines - corresponding epilines '''
    r, c = img1.shape
    img1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
    img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
    for r, pt1, pt2 in zip(lines, pts1, pts2):
        color = tuple(np.random.randint(0, 255, 3).tolist())
        x0, y0 = map(int, [0, -r[2] / r[1]])
        x1, y1 = map(int, [c, -(r[2] + r[0] * c) / r[1]])
        img1 = cv2.line(img1, (x0, y0), (x1, y1), color, 1)
        img1 = cv2.circle(img1, tuple(pt1), 5, color, -1)
        img2 = cv2.circle(img2, tuple(pt2), 5, color, -1)
    return img1, img2


def compare(imageName1, imageName2):
    '''
	takes in two images, and returns a set of correspondences between the two images matched using ORB features,
	 sorted from best to worst match using an L2 norm distance.
	'''
    # Currently hard-coded images.
    # This will have to be updated to handled many images, not sure how the algorithm would handle that.
    img1 = cv2.imread(imageName1, 0)
    img2 = cv2.imread(imageName2, 0)

    # Initiate SIFT detector
    sift = cv2.SIFT_create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)
    # FLANN parameters
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)  # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    pts1 = []
    pts2 = []
    # ratio test as per Lowe's paper
    for i, (m, n) in enumerate(matches):
        if m.distance < 0.8 * n.distance:
            pts2.append(kp2[m.trainIdx].pt)
            pts1.append(kp1[m.queryIdx].pt)

    # Compute fundamental matrix
    pts1 = np.int32(pts1)
    pts2 = np.int32(pts2)
    F, mask = cv2.findFundamentalMat(pts1, pts2, cv2.FM_LMEDS)
    # We select only inlier points
    pts1 = pts1[mask.ravel() == 1]
    pts2 = pts2[mask.ravel() == 1]

    # Find epilines corresponding to points in right image (second image) and
    # drawing its lines on left image
    lines1 = cv2.computeCorrespondEpilines(pts2.reshape(-1, 1, 2), 2, F)
    lines1 = lines1.reshape(-1, 3)
    img5, img6 = drawlines(img1, img2, lines1, pts1, pts2)

    # Find epilines corresponding to points in left image (first image) and
    # drawing its lines on right image
    lines2 = cv2.computeCorrespondEpilines(pts1.reshape(-1, 1, 2), 1, F)
    lines2 = lines2.reshape(-1, 3)
    img3, img4 = drawlines(img2, img1, lines2, pts2, pts1)

    # Write output
    id1 = remove_filename_from_file(imageName1)
    id2 = remove_filename_from_file(imageName2)
    cv2.imwrite(os.path.join("results", "{}_{}_left_to_right_epilines.jpg".format(id1, id2)), img3)
    # cv2.imwrite(os.path.join("results", "{}_{}_left_points.jpg".format(id1, id2)), img4)
    cv2.imwrite(os.path.join("results", "{}_{}_right_to_left_epilines.jpg".format(id1, id2)), img5)
    # cv2.imwrite(os.path.join("results", "{}_{}_right_points.jpg".format(id1, id2)), img6)


if __name__ == "__main__":
    os.chdir("./images")
    try:
        os.mkdir("./results")
    except:
        print("Results directory already exists")

    num_images = 7
    images = ["{}.jpg".format(x) for x in range(1, num_images + 1)]
    # Create pairs of images (1, 1), (1, 2), (1, 3)...
    combinations = itertools.product(images, images)
    # Remove duplicates, for e.g. [(1, 2), (2, 1)] => [(1, 2)]
    distinct_combinations = set((a, b) if a <= b else (b, a) for a, b in combinations)
    # Remove self references, for e.g. [(1, 1)] => []
    iter_set = [x for x in distinct_combinations if (x[0] != x[1])]
    # Sort list to process in-order
    iter_set = sorted(iter_set, key=lambda x: (x[0], x[1]), reverse=False)

    print("Combinations to process: {}".format(iter_set))
    for i, j in iter_set:
        print("Initiating {} vs {}".format(i, j))
        compare(i, j)
        # break
