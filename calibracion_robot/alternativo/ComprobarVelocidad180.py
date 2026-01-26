#!/usr/bin/env python3
import math
import os
import time
from math import pi
from time import sleep

from ev3dev2.led import Leds
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_D, LargeMotor, MediumMotor
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import ColorSensor, TouchSensor, UltrasonicSensor
from ev3dev2.sound import Sound

from lib.movement import girar, girar_solo_derecha, girar_solo_izquierda, recto, parar, subir_brazo, DISTANCIA_RUEDAS, DIAMETRO_RUEDA, PERIMETRO_RUEDA

large_motor_l = LargeMotor(OUTPUT_B)
large_motor_r = LargeMotor(OUTPUT_A)
arm_motor = MediumMotor(OUTPUT_D)

ultrasonic_sensor = UltrasonicSensor(INPUT_2)
color_sensor = ColorSensor(INPUT_1)


if __name__ == "__main__":
    signo = -1
    for _ in range(2):
        signo *= -1
        for velocidad in range(10, 21, 5):
            sound = Sound()
            sound.beep()
            sleep(1)
            grados = 90 * signo
            girar(grados, velocidad, True)
            print("Se probo a girar con: ", velocidad, " y un angulo de: ", grados)
            sleep(8)
