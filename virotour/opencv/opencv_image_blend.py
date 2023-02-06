import cv2 as cv
import numpy as np
import time
import os

# References
# Source from https://hackthedeveloper.com/transition-effect-opencv-python/
# https://docs.opencv.org/2.4/doc/tutorials/core/adding_images/adding_images.html
# https://www.youtube.com/watch?v=636d_GqkmM8
os.chdir("virotour/opencv/images")

while True:
    
    image1 = cv.imread('1.jpg')
    image2 = cv.imread('2.jpg')
    
    for i in np.linspace(0,1,100):
        alpha = i
        beta = 1 - alpha
        output = cv.addWeighted(image1,alpha,image2,beta,0)
        cv.imshow('Transition Effect ',output)
        time.sleep(0.00001)
        if cv.waitKey(1) == 27:
            break
    cv.destroyAllWindows()