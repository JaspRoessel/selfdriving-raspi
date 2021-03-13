from __future__ import print_function
import cv2
import numpy as np
from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import imutils
import time
import os

ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=100, help="# of frames to loop over for FPS test")
ap.add_argument("-d", "--display", type=int, default=1, help="Whether or not frames should be displayed")
args = vars(ap.parse_args())

vs = PiVideoStream().start()
time.sleep(2.0)
fps = FPS().start()

frameWidth = 400
frameHeight = 300
cap = cv2.VideoCapture(1)
cap.set(3, frameWidth)
cap.set(4, frameHeight)


def empty(a):
    pass


cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640, 240)
cv2.createTrackbar("HUE Min", "HSV", 0, 179, empty)
cv2.createTrackbar("HUE Max", "HSV", 20, 179, empty)
cv2.createTrackbar("SAT Min", "HSV", 0, 255, empty)
cv2.createTrackbar("SAT Max", "HSV", 255, 255, empty)
cv2.createTrackbar("VALUE Min", "HSV",105, 255, empty)
cv2.createTrackbar("VALUE Max", "HSV", 255, 255, empty)

cap = cv2.VideoCapture(0)
frameCounter = 0

while True:
    #frameCounter += 1
    #if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frameCounter:
     #   cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
      #  frameCounter = 0

    img = vs.read()
    img = imutils.resize(img, width=400)
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    fps.update()
    h_min = cv2.getTrackbarPos("HUE Min", "HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
    v_max = cv2.getTrackbarPos("VALUE Max", "HSV")
    print(h_min)


    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHsv, lower, upper)
    result = cv2.bitwise_and(img, img, mask=mask)

    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    kernel_erode = np.ones((3, 3), np.uint8)
    eroded_mask = cv2.erode(mask, kernel_erode, iterations=1)
    kernel_dilate = np.ones((5, 5), np.uint8)
    dmask = cv2.dilate(eroded_mask, kernel_dilate, iterations=1)
    hStack = np.hstack([img, mask, result, dmask])

    cv2.imshow('Horizontal Stacking', hStack)
    if cv2.waitKey(1) and 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()