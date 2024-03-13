#!/usr/bin/env micropython

from ev3dev2.motor import OUTPUT_C, OUTPUT_B, OUTPUT_A, LargeMotor, MediumMotor

mRight = LargeMotor(OUTPUT_B)
mLeft = LargeMotor(OUTPUT_C)
mMid = MediumMotor(OUTPUT_A)

Wr = 100
Wl = -50
Wm = 0

while True:
    mLeft.on(Wl)
    mRight.on(Wr)

    mMid.on(0.5 * (Wl + Wr))

    print(mMid.speed)

    