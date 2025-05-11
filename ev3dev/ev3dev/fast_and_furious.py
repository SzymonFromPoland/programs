#!/usr/bin/env micropython

from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import Sensor
from ev3dev2.motor import Motor, OUTPUT_C, OUTPUT_D
from ev3dev2.button import Button
from ev3dev2.sound import Sound
from time import sleep, time

def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def clamp(value, min_value, max_value):
    return max(min_value, min(max_value, value))

def drive(speed_right, speed_left):
    speed_left = clamp(speed_left, -100, 100)
    speed_right = clamp(speed_right, -100, 100)
    motL.duty_cycle_sp = speed_left
    motR.duty_cycle_sp = speed_right
    motL.run_direct()
    motR.run_direct()

motL = Motor(OUTPUT_C)
motR = Motor(OUTPUT_D)
motL.polarity = 'inversed'

sensor = Sensor(INPUT_1)
btn = Button()
sound = Sound()

# Calibration values
BLACK_VALUE = 4750
WHITE_VALUE = 2500
setpoint = (BLACK_VALUE + WHITE_VALUE) / 2

# PID constants
Kp = 0.05
Ki = 0.0
Kd = 0.1

integral = 0
last_error = 0
base_speed = 60

while not btn.any():
    value = sensor.value()
    print(value)
    error = value - setpoint
    integral += error
    derivative = error - last_error

    correction = Kp * error + Ki * integral + Kd * derivative

    speed_left = base_speed + correction
    speed_right = base_speed - correction

    drive(speed_right, speed_left)

    last_error = error
