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
import motor as M
import tensorflow as tf
from tensorflow import keras
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24

#belangrijk voor camera
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=100)
ap.add_argument("-d", "--display", type=int, default=1) #default=1: show beeld aan, default=0: show beeld uit
args = vars(ap.parse_args())

###############################################
#Vul hier het ai_model in
model = tf.keras.models.load_model('modelA.h5')
###############################################

#Beeld klaarmaken voor het model
def preProcess(img):
    img = img[54:120,:]
    img = np.reshape(img, (88, 100, 3)) / 255
    return img

#Filtert de lijn
def maskedges(img):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

###############################################       check colorfinder.py
#Vul de maximale en minimale kleurenwaardes in#
    lower_white = np.array([0, 45, 195])
    upper_white = np.array([179, 255, 255])
###############################################

    mask = cv2.inRange(imgHSV, lower_white, upper_white)
    return mask

def getsensor():
    GPIO.output(TRIG, False)
    time.sleep(0.00001)

    GPIO.output(TRIG, True)

    time.sleep(0.00001)

    GPIO.output(TRIG, False)

    pulse_start = 0
    pulse_end = 0
    while GPIO.input(ECHO)==0:
        pulse_start = time.time()


    while GPIO.input(ECHO)==1:
        pulse_end = time.time()

    time.sleep(0.0001)
    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150
    distance = round(distance)

    print ("Distance: " + str(distance) + "cm")

    return distance


print("[Camera Opstarten]")
vs = PiVideoStream().start()
time.sleep(6.0)
fps = FPS().start()
i = 0

print ("Distance Measurement In Progress")

GPIO.setup(TRIG,GPIO.OUT)

GPIO.setup(ECHO,GPIO.IN)

GPIO.output(TRIG, False)

print ("Waiting For Sensor To Settle")

time.sleep(2)

while True:
    #beeldverwerking
    frame = vs.read()
    frame = imutils.resize(frame, width=400)
    frame = maskedges(frame)

    if args["display"] > 0:
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
    fps.update()

    #beeld klaarmaken voor model
    frame = np.asarray(frame)
    frame = preProcess(frame)
    frame = np.array([frame])

    #stuurrichting voorspellen via model
    sturen = (model.predict(frame))
    print(sturen)
    top = np.argmax(sturen) #1 = links, 2 = rechtdoor, 3 = rechts
    print(top)
    sensor = getsensor()


    #motor opstarten
    while i < 15000:
        M.MoveF(100)
        i += 1

######################################################################
#snelheid = s, s configureren/fine_tunen naar keuze, s = 23 standaard#
    s = 30
######################################################################


    if sensor <= 20:    # Als auto binnen bepaale afstand wat ziet dan stop
        M.Stop2()
        print("stop")

    else:

        if top == 1: #links

            M.MoveL(2130)
            print("links")
            M.MoveF(s + 2)

        elif top == 3: #rechts
            M.MoveR(1690)
            print("rechts")
            M.MoveF(s + 2)

        elif top == 2: #rechtdoor

            M.Stop()
            print("rechtdoor")
            M.MoveF(s)

### OPLETTEN MET SCRIPT STOPPEN: AUTO KNALT DOOR
