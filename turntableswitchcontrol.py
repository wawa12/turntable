#!/usr/bin/python3
# this program is normally run from /etc/rc.local at startup
import signal
import sys
from time import sleep
import RPi.GPIO as GPIO
import math

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def LEFT_button_callback(LEFT):
    global stepcounter
    #print(stepcounter)
    GPIO.output(DIR,CCW)
    #ramp up speed on motor
    while GPIO.input(LEFT) == GPIO.LOW:
        delay = lmax-(lmax/(1+math.exp(-k*((stepcounter/acceldelay-6)-smid))))+fastestdelay
        print("LEFT input", stepcounter, delay)
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
        stepcounter += 1
    while GPIO.input(LEFT) == GPIO.HIGH and stepcounter > 0:
        if stepcounter > 1450: #1450 steps to full speed
            stepcounter = 1451
            delay = lmax-(lmax/(1+math.exp(-k*((stepcounter/acceldelay-6)-smid))))+fastestdelay
        delay = lmax-(lmax/(1+math.exp(-k*((stepcounter/acceldelay-6)-smid))))+fastestdelay
        print("LEFT output", stepcounter, delay)
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
        stepcounter -= 2
    #stepcounter = 0

def RIGHT_button_callback(RIGHT):
    global stepcounter
    #print(stepcounter)
    GPIO.output(DIR,CW)
    #ramp up speed on motor
    while GPIO.input(RIGHT) == GPIO.LOW:
        delay = lmax-(lmax/(1+math.exp(-k*((stepcounter/acceldelay-6)-smid))))+fastestdelay
        print("RIGHT input", stepcounter, delay)
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
        stepcounter += 1
    while GPIO.input(RIGHT) == GPIO.HIGH and stepcounter > 0:
        if stepcounter > 1450: #1450 steps to full speed
            stepcounter = 1451
            delay = lmax-(lmax/(1+math.exp(-k*((stepcounter/acceldelay-6)-smid))))+fastestdelay
        delay = lmax-(lmax/(1+math.exp(-k*((stepcounter/acceldelay-6)-smid))))+fastestdelay
        print("RIGHT output", stepcounter, delay)
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
        stepcounter -= 2
    #stepcounter = 0

DIR = 20 #Direction GPIO pin (38)
STEP = 21 #Step GPIO pin (40)
LEFT = 19 #left dir pin
RIGHT = 16 #right dir pin
CW = 1 #Clockwise Rotation
CCW = 0 #Counterclockwise Rotation
SPR = 32 #Steps per Revolution
GR = 64 #gear ratio

fastestdelay = 0.0006
stepcounter = 0
slowestdelay = fastestdelay*20 #(0.012)

#sigmoid curve variables
lmax = slowestdelay #L curves maximum value)
smid = 0 #constant, sigmoids midpoint
k = 0.2 #k, steepness of sigmoid curve
acceldelay = 35 #?seems to delay curve

#GPIO pin setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.output(DIR, CW)

GPIO.setup(LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(LEFT, GPIO.BOTH, callback=LEFT_button_callback)
GPIO.add_event_detect(RIGHT, GPIO.BOTH, callback=RIGHT_button_callback)

signal.signal(signal.SIGINT, signal_handler)
signal.pause()
