#!/usr/bin/env micropython

from ev3dev2.sensor import INPUT_4
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.motor import Motor, OUTPUT_C, OUTPUT_D
from ev3dev2.button import Button
from ev3dev2.sound import Sound
from time import sleep, time

def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def drive(speed_left, speed_right):
    motL.duty_cycle_sp = speed_left
    motR.duty_cycle_sp = speed_right

    motL.run_direct()
    motR.run_direct()

line_sensor = ColorSensor(INPUT_4)

motL = Motor(OUTPUT_C)
motR = Motor(OUTPUT_D)
motR.polarity = 'inversed'

btn = Button()
sound = Sound()

last_time = time()

store_correct = []

light_value = 0
color_upper = 51
color_lower = 9
correct = 0
speed = 40
speed2 = 40
sensitivity = 2.4
calibrate = False
store = True
timer = 0

if calibrate:   
    sound.play_tone(1000, 0.5)
    color_upper = line_sensor.reflected_light_intensity

    sleep(1)

    sound.play_tone(1000, 0.5)
    color_lower = line_sensor.reflected_light_intensity

while True:
    start_time = time()

    raw_light_value = line_sensor.reflected_light_intensity
    light_value = map_value(raw_light_value, color_lower, color_upper, 0, 100)

    correct = (50 - light_value) / sensitivity

    current_time = time()
    delay = current_time - last_time
    last_time = current_time

    if store:
        store_correct.append(correct)

    if btn.enter:
        break
        sleep(0.4)

    print(round(delay * 1000, 0), " ms - ", round(light_value, 2), " correct: ", round(correct, 3))

    if correct < 0:
        drive(speed, speed + correct)
    else:
        drive(speed - correct, speed)

    elapsed = time() - start_time
    sleep_time = 0.05 - elapsed
    if sleep_time > 0:
        sleep(sleep_time)

drive(0,0)

sleep(3)

count = 0

while True:
    start_time = time()
    current_time = time()
    delay = current_time - last_time
    last_time = current_time

    if count == len(store_correct) - 1:
        break

    correct = store_correct[count]

    if correct < 0:
        drive(speed * (speed2/speed), speed * (speed2/speed) + correct * (speed2/speed))
    else:
        drive(speed * (speed2/speed) - correct * (speed2/speed), speed * (speed2/speed))

    print(round(delay * 1000, 0), " ms - ", correct)

    elapsed = time() - start_time
    sleep_time = (0.05 / (speed2/speed)) - elapsed
    if sleep_time > 0:
        sleep(sleep_time)

    count += 1