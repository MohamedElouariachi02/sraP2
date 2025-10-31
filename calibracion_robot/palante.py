#!/usr/bin/env python3
import math

from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor
from ev3dev2.led import Leds
from time import sleep
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B
import os
from ev3dev2.sound import Sound
from math import pi

large_motor_l = LargeMotor(OUTPUT_B)
large_motor_r = LargeMotor(OUTPUT_A)
diemetroRueda = 0.055
distanciaRuedas = 0.12


def recto(distancia):
    large_motor_l.on_for_degrees(speed=50, degrees=-360 * 0.5/(2*pi*(diemetroRueda/2)), brake=True, block=False)
    large_motor_r.on_for_degrees(speed=50, degrees=-360 * 0.5/(2*pi*(diemetroRueda/2)), brake=True, block=True)

def giro(angulo):
    large_motor_l.on_for_degrees(speed=50, degrees=360 * angulo, brake=True, block=False)
    large_motor_r.on_for_degrees(speed=50, degrees=-360 * angulo, brake=True, block=True)


os.system('setfont Lat15-TerminusBold14')

sound = Sound()
for i in range(4):
    recto(0.5)
    giro(2.89)



sound.beep()
sleep(1)

alpha = 50 / 5.5


sleep(1)
sound.beep()

