#!/usr/bin/python3
import signal
import sys
from time import sleep
import RPi.GPIO as GPIO
import math
import pygame
import os

#os.environ["SDL_VIDEODRIVER"] = "dummy" # or maybe 'fbcon'
#need to run as root for headless mode
os.putenv("SDL_VIDEODRIVER", "dummy")
import pygame.display
pygame.display.init()
#screen = pygame.display.set_mode((1,1))
clock = pygame.time.Clock()

pygame.init()

running = True

joystick = pygame.joystick.Joystick(0)
joystick.init()

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def LEFT_button_callback():
    global stepcounter
    #print(stepcounter)
    GPIO.output(DIR,CCW)
    #ramp up speed on motor
    z = joystick.get_axis(3)
    while z < 0:
        print("in z def", z)
        #delay = lmax-(lmax/(1+math.exp(-k*((stepcounter/acceldelay-6)-smid))))+fastestdelay
        delay = -0.0114*abs(z)+slowestdelay
        print("LEFT input", stepcounter, delay)
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
        stepcounter += 1
        pygame.event.get()
        z = joystick.get_axis(3)
    stepcounter = 0

def RIGHT_button_callback():
    global stepcounter
    #print(stepcounter)
    GPIO.output(DIR,CW)
    #ramp up speed on motor
    z = joystick.get_axis(3)
    while z > 0:
        delay = -0.0114*abs(z)+slowestdelay
        print("RIGHT input", stepcounter, delay)
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
        stepcounter += 1
        pygame.event.get()
        z = joystick.get_axis(3)
    stepcounter = 0

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

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.JOYAXISMOTION:
            print(event)
            x, y, z = joystick.get_axis(0), joystick.get_axis(1), joystick.get_axis(3)
            print (x, y, z)
            if z < 0:
                print ("z lt 0")
                LEFT_button_callback()
            if z > 0:
                RIGHT_button_callback()

        elif event.type == pygame.JOYHATMOTION:
            print(event)
        elif event.type == pygame.JOYBUTTONDOWN:
            print(event)
            b0 = joystick.get_button(0)
            print(b0)
        elif event.type == pygame.JOYBUTTONUP:
            print(event)
            b0 = joystick.get_button(0)
            print(b0)
    clock.tick(20)

pygame.quit()





#GPIO.add_event_detect(LEFT, GPIO.BOTH, callback=LEFT_button_callback)
#GPIO.add_event_detect(RIGHT, GPIO.BOTH, callback=RIGHT_button_callback)

#signal.signal(signal.SIGINT, signal_handler)
#signal.pause()
