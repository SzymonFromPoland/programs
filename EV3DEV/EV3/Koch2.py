#!/usr/bin/env python3


from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.led import Leds
from ev3dev2.button import Button
from time import sleep
import math
import random

mB = LargeMotor(OUTPUT_B)
mC = LargeMotor(OUTPUT_C)

mB.position = 0
mC.position = 0

us1 = UltrasonicSensor(INPUT_2) #lewo
us2 = UltrasonicSensor(INPUT_4) #srodek
us3 = UltrasonicSensor(INPUT_1) #prawo

leftRead = 0
midRead = 0
rightRead = 0

leds = Leds()

btn = Button()

Kp = 2.5
Ki = 0.3
prevError = 0

start = False

###

rotSpeed = 60
lastDir = 0

def move(deltaNorm):
    global midRead
    global lastDir
    global rotSpeed
    

    print(lastDir, deltaNorm)

    if deltaNorm > 0:
        lastDir = rotSpeed
    elif deltaNorm < 0:
        lastDir = -1 * rotSpeed
    
    if midRead < 55:
        mB.on(-100)
        mC.on(-100)

    elif midRead > 55:
        if deltaNorm != 0:
            mB.on(deltaNorm)
            mC.on(deltaNorm * -1)
        elif deltaNorm == 0:
            
            mB.on(lastDir)
            mC.on(lastDir * -1)

###

def pid(currAngle, toAngle):
    global prevError

    error = toAngle - currAngle
    delta = (error * Kp) + (Ki * (error + prevError))
    prevError = error

    deltaNorm = max(min(delta, 100), -100)

    return deltaNorm

###

def load(servoB, servoC):
    if mB.speed < servoB and mC.speed < servoC:
        leds.set_color('LEFT', (1, 0))
        leds.set_color('RIGHT', (0, 1))
    else:
        leds.set_color('LEFT', (0, 1))
        leds.set_color('RIGHT', (0, 1))
    


###
    
S = math.sqrt(2)    

def tracking():
    global midRead
    global S

    MAX_DIST = 60

    leftRead = us1.distance_centimeters if us1.distance_centimeters < MAX_DIST else 1000000
    midRead = us2.distance_centimeters if us2.distance_centimeters < MAX_DIST else MAX_DIST
    rightRead = us3.distance_centimeters if us3.distance_centimeters < MAX_DIST else 1000000

    c1 = math.sqrt((midRead * midRead) + (rightRead * rightRead) - midRead * rightRead * S)
    c2 = math.sqrt((midRead * midRead) + (leftRead * leftRead) - midRead * leftRead * S)
    alpha1 = math.degrees(math.asin((midRead * (S / 2)) / c1))
    alpha2 = math.degrees(math.asin((midRead * (S / 2)) / c2))


    return alpha2 - alpha1

### main ###

leds.set_color('LEFT', (1, 0))
leds.set_color('RIGHT', (1, 0))

while True:
    btn.process()
    if btn.down:

        btn.wait_for_released('down', 10000)
        lastDir = rotSpeed * -1

    if btn.up:

        btn.wait_for_released('up', 10000)
        lastDir = rotSpeed

    if btn.enter:

        btn.wait_for_released('enter', 10000)

        leds.set_color('LEFT', (0, 1))
        leds.set_color('RIGHT', (0, 1))

        sleep(4.8)
        start = True

    load(-30, -30)

    if start == True:
        
        move(pid(tracking(), 0))

    sleep(0.001)