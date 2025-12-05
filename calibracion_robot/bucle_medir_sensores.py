#!/usr/bin/env python3
from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor, ColorSensor
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B
from ev3dev2.sound import Sound
from ev3dev2.led import Leds
from time import sleep
from math import pi
import math
import os


os.system('setfont Lat15-TerminusBold14')

ultrasonic_sensor = UltrasonicSensor(INPUT_2)
color_sensor = ColorSensor(INPUT_1)

sound = Sound()
sound.beep()

while True:
    print("---")
    print("distancia: " + str(ultrasonic_sensor.distance_centimeters) + " cm")
    print("intensidad: " + str(color_sensor.reflected_light_intensity) + " %")
    sleep(1)
