#!/usr/bin/env micropython

from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C,  LargeMotor, MediumMotor
from ev3dev2.sensor import INPUT_2, INPUT_4
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.led import Leds
from ev3dev2.button import Button
from time import sleep

leds = Leds()
btn = Button()

usRight = UltrasonicSensor(INPUT_2)
usLeft = UltrasonicSensor(INPUT_4)

mRight = LargeMotor(OUTPUT_B)
mLeft = LargeMotor(OUTPUT_C)
mMid = MediumMotor(OUTPUT_A)

MAX_DIST = 60

prevError = 0
distLeft = 0
distRight = 0
enemyAngle = 30
lastEnemyAngle = 0
x = 0
atack = False
start = False

KP = 120
KI = 10

### DRIVE ###

def drive(error):
    global prevError
    global x

    x = ((KP * error) + (KI * (error + prevError))) / 100
    prevError = error

    xNorm = max(min(x, 100), -100)

    rightSpeed = max(-100, -100 + xNorm * 2)
    leftSpeed = max(-100, -100 - xNorm * 2)
    midSpeed = 0.5 * (leftSpeed + rightSpeed)

    

    if atack:
        mMid.on(-100)
        mRight.on(rightSpeed)
        mLeft.on(leftSpeed)

    else:
        mMid.on(midSpeed)
        mRight.on(xNorm) 
        mLeft.on(-xNorm)

    # print(str(round(xNorm)))
        

### TRACKING ###

def tracking():
    global MAX_DIST
    global distLeft
    global distRight
    global enemyAngle
    global atack
    global lastEnemyAngle

    sl = usLeft.distance_centimeters  # 55
    sr = usRight.distance_centimeters # 60

    distLeft = min(sl, MAX_DIST)
    distRight = min(sr, MAX_DIST)

    distMin = min(distLeft, distRight) #55
    distMax = max(distLeft, distRight)

    lastEnemyAngle = enemyAngle
    enemyAngle = ((distLeft - distRight) * 2 * distMin) / MAX_DIST # -9.2
    enemyAngle = max(min(enemyAngle, 30), -30)
    
    if distLeft == MAX_DIST and distRight == MAX_DIST:
        enemyAngle = 30 if lastEnemyAngle > 0 else -30
    
    if abs(enemyAngle) < 30:
        atack = True
    else:
        atack = False   

    drive(enemyAngle)


### MAIN ###
    
leds.set_color('LEFT', (1, 0))
leds.set_color('RIGHT', (1, 0))

while True:
    btn.process()
    print(lastEnemyAngle)

    if start == True:
        
        tracking()

        if btn.enter:
        
            btn.wait_for_released('enter', 10000)

            start = False

            leds.set_color('LEFT', (1, 0))
            leds.set_color('RIGHT', (1, 0))

            mRight.off(brake = False)
            mLeft.off(brake = False)
            mMid.off(brake = False)

    else:

        if btn.down:

            btn.wait_for_released('down', 10000)
            enemyAngle = -30


        if btn.up:

            btn.wait_for_released('up', 10000)
            enemyAngle = 30


        if btn.enter:

            btn.wait_for_released('enter', 10000)

            leds.set_color('LEFT', (0, 1))
            leds.set_color('RIGHT', (0, 1))

            sleep(4.9)
            start = True

    # sleep(0.001)
    # print(str(round(enemyAngle)), str(round(distLeft)), str(round(distRight)), str(round(x)))

