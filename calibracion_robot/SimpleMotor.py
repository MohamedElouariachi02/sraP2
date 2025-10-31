#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, OUTPUT_B
from time import sleep


large_motor = LargeMotor(OUTPUT_B)

grados = 1000

large_motor.on_for_degrees(speed=20, degrees=grados1M, brake=True, block=False)
