import pigpio
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
Ena,In1,In2 = 2,3,4
GPIO.setup(Ena,GPIO.OUT)
GPIO.setup(In1,GPIO.OUT)
GPIO.setup(In2,GPIO.OUT)
pwm = GPIO.PWM(Ena,100)
p = pigpio.pi()
p.set_mode(18, pigpio.OUTPUT)
p.set_PWM_frequency(18,50)
pwm.start(0)
p.set_servo_pulsewidth(18,1910)
def MoveF(speed):
    GPIO.output(In1,GPIO.HIGH)
    GPIO.output(In2,GPIO.LOW)
    pwm.ChangeDutyCycle(speed)
def MoveB(speed):
    GPIO.output(In1,GPIO.LOW)
    GPIO.output(In2,GPIO.HIGH)
    pwm.ChangeDutyCycle(speed)
    p.set_servo_pulsewidth(18,1910)
def MoveL(angle):
    p.set_servo_pulsewidth(18,angle)

def MoveR(angle):
    p.set_servo_pulsewidth(18,angle)

def Stop():
    pwm.ChangeDutyCycle(0)
    p.set_servo_pulsewidth(18,1910)
    
def Stop2():
    pwm.ChangeDutyCycle(0)