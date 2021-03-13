from __future__ import print_function
from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import imutils
import time
import cv2
import numpy as np
import os
import moter as M
import tensorflow as tf
from tensorflow import keras
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=100, help="# of frames to loop over for FPS test")
ap.add_argument("-d", "--display", type=int, default=0, help="Whether or not frames should be displayed")
args = vars(ap.parse_args())

vs = PiVideoStream().start()
time.sleep(2.0)
fps = FPS().start()

def maskedges(img):
    # Convert naar HSV kleurenwaardes
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #cv2.imshow("HSV", imgHSV)

    # Knipt alles behalve wit eruit
    lower_white = np.array([0, 0, 164])
    upper_white = np.array([135, 18, 255])
    mask = cv2.inRange(imgHSV, lower_white, upper_white)
    #cv2.imshow("Mask", mask)
    return mask
    

def getcam():
    
    frame = vs.read()
    frame = imutils.resize(frame, width=400)
    frame = maskedges(frame)
    # check to see if the frame should be displayed to our screen
    if args["display"] > 0:
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
    # update the FPS counter
    fps.update()
    
    return frame


