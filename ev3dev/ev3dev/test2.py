#!/usr/bin/env micropython

from ev3dev2.sensor import INPUT_4
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.motor import Motor, OUTPUT_C, OUTPUT_D
from ev3dev2.button import Button
from ev3dev2.sound import Sound
from time import sleep, time

def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
def clamp(value, min_value, max_value):
    return max(min_value, min(max_value, value))
def drive(speed_left, speed_right):
    speed_left = clamp(speed_left, -100, 100)
    speed_right = clamp(speed_right, -100, 100)
    motL.duty_cycle_sp = speed_left
    motR.duty_cycle_sp = speed_right
    motL.run_direct()
    motR.run_direct()

motL = Motor(OUTPUT_C)
motR = Motor(OUTPUT_D)
motL.polarity = 'inversed'

line_sensor = ColorSensor(INPUT_4)
btn = Button()
sound = Sound()

color_upper = 0
color_lower = 0

Kp_line = 0.65 # 0.65
Ki_line = 0.0  # 0.0
Kd_line = 0.9  # 0.8

integral_line = 0
last_error_line = 0

base_speed = 100
last_time = time()
ref_time = last_time
ats = None
lsl = False

sleep(1)

while True:
    current_time = time()
    delay = current_time - last_time
    timer = current_time - ref_time

    light_value_raw = line_sensor.reflected_light_intensity
    # light_value = map_value(light_value_raw, color_lower, color_upper, 0, 100)
    light_value = light_value_raw

    error_line = 3600 - light_value
    integral_line += error_line
    derivative_line = error_line - last_error_line
    correction_line = (Kp_line * error_line) + (Ki_line * integral_line) + (Kd_line * derivative_line)
    correction_line = correction_line * (122/(color_upper-color_lower))
    last_error_line = error_line

    if light_value >= 3600 + 5:
        if ats is None:
            ats = current_time
        elif current_time - ats >= 1.25:
            lsl = True
    else:
        ats = None
        lsl = False

    left_speed = base_speed - correction_line
    right_speed = base_speed + correction_line

    if lsl:
        left_speed = base_speed
        right_speed = min(base_speed-5, timer * 30 + 10)
    else:
        timer = 0
        ref_time = time()

    drive(right_speed, left_speed)

    print("delay: ", delay*1000, "correction:", correction_line, "line:", light_value, "locked:", lsl)
    last_time = current_time
