#!/usr/bin/env micropython
from ev3dev2.sensor import INPUT_3, INPUT_2
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.motor import Motor, OUTPUT_C, OUTPUT_D
from ev3dev2.button import Button
from ev3dev2.sound import Sound
from time import sleep, time

us1 = UltrasonicSensor(INPUT_2) # right
us2 = UltrasonicSensor(INPUT_3) # left

m1 = Motor(OUTPUT_C)
m2 = Motor(OUTPUT_D)
m2.polarity = 'inversed'

btn = Button()
sound = Sound()

def clamp(value, min_value, max_value):
    return max(min_value, min(max_value, value))
def drive(speed_left, speed_right):
    speed_left = clamp(speed_left, -100, 100)
    speed_right = clamp(speed_right, -100, 100)
    m1.duty_cycle_sp = speed_left
    m2.duty_cycle_sp = speed_right
    m1.run_direct()
    m2.run_direct()

dist_left = 0
dist_right = 0
drift = 1.5
treshold = 40
last_dir = "LEFT"


sound.play_tone(1500, 0.25)

while True:
    if btn.up:
        last_dir = "LEFT"
        sound.play_tone(1000, 0.25)
    if btn.down:
        last_dir = "RIGHT"
        sound.play_tone(500, 0.25)
    if btn.enter:
        sound.play_tone(1500, 0.25)
        sleep(4.65)
        if last_dir is "LEFT":
            drive(-100,100)
        elif last_dir is "RIGHT":
            drive(100,-100)
        sleep(0.5)
        break

    if btn.left:
        sound.play_tone(1500, 0.25)
        sleep(0.75)
        if last_dir is "LEFT":
            drive(-100,100)
        elif last_dir is "RIGHT":
            drive(100,-100)
        sleep(0.2)
        break

test = False

while True:
    raw_left = min(us2.distance_centimeters_continuous, treshold)
    raw_right = min(us1.distance_centimeters_continuous, treshold)
    dist_left = raw_left < treshold
    dist_right = raw_right < treshold

    print(dist_left, dist_right, test, raw_left, raw_right)

    if dist_left:
        last_dir = "LEFT"
    elif dist_right:
        last_dir = "RIGHT"

    if dist_right or dist_right:
        diff = drift*(raw_left - raw_right)
        if raw_left < 15 and raw_right < 15:
            drive(100,100)
            test = True
            sleep(0.5)
        else:
            drive(100+diff,100-diff)
            test = False
    else:
        if last_dir is "LEFT":
            drive(-50,50)
        elif last_dir is "RIGHT":
            drive(50,-50)



    