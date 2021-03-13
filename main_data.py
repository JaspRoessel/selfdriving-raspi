import pygame
import RPi.GPIO as GPIO
from time import sleep
import data as D
import motor as M
import cv2


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
Ena,In1,In2 = 2,3,4
Enb,In3,In4 = 17,22,27
GPIO.setup(18,GPIO.OUT)
GPIO.setup(Ena,GPIO.OUT)
GPIO.setup(In1,GPIO.OUT)
GPIO.setup(In2,GPIO.OUT)


def init():
    pygame.init()
    win = pygame.display.set_mode((100,100))

def getKey(keyName):
    ans = False
    for eve in pygame.event.get():pass
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame,'K_{}'.format(keyName))
    if keyInput [myKey]:
        ans = True
    pygame.display.update()

    return ans

def stuur(st):
    print(st)
    global ow
    ow = st
    return st

def main():
    if getKey('LEFT'):
        M.MoveL(2130)
        stuur(1)
        M.MoveF(28)
    elif getKey('RIGHT'):
        M.MoveR(1690)
        stuur(3)
        M.MoveF(28)
    elif getKey('DOWN'):
        M.MoveB(50)
    else:
        M.Stop()
        stuur(2)
        M.MoveF(24)


i = 0
if __name__ == '__main__':
    init()
    while True:
        while i < 47000:
            M.MoveF(100)
            i += 1
        main()
        D.data(ow)