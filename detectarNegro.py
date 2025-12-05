#!/usr/bin/env python3
import math
import os
from math import pi
from time import sleep

from ev3dev2.led import Leds
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, LargeMotor
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import ColorSensor, TouchSensor, UltrasonicSensor
from ev3dev2.sound import Sound

large_motor_l = LargeMotor(OUTPUT_B)
large_motor_r = LargeMotor(OUTPUT_A)

ultrasonic_sensor = UltrasonicSensor(INPUT_2)
color_sensor = ColorSensor(INPUT_1)

DIAMETRO_RUEDA = 0.055
DISTANCIA_RUEDAS = 0.12
PERIMETRO_RUEDA = pi * DIAMETRO_RUEDA

def recto(distancia_m, velocidad=25):
    vueltas_rueda = distancia_m / PERIMETRO_RUEDA
    grados_motor = vueltas_rueda * 360

    large_motor_l.on_for_degrees(speed=velocidad, degrees=grados_motor, brake=True, block=False)
    large_motor_r.on_for_degrees(speed=velocidad, degrees=grados_motor, brake=True, block=True)

def girar(grados_robot, velocidad=25):
    # perímetro del círculo que trazan las ruedas al girar
    perimetro_giro_robot = pi * DISTANCIA_RUEDAS
    distancia_a_recorrer = (grados_robot / 360) * perimetro_giro_robot
    
    # distancia a grados del motor
    vueltas_rueda = distancia_a_recorrer / PERIMETRO_RUEDA
    grados_motor = vueltas_rueda * 360

    large_motor_l.on_for_degrees(speed=velocidad, degrees=grados_motor, brake=True, block=False)
    large_motor_r.on_for_degrees(speed=velocidad, degrees=-grados_motor, brake=True, block=True)


os.system('setfont Lat15-TerminusBold14')

sound = Sound()
sound.beep()

nombre_archivo = 'datos_robot.csv'

blanco = 0
for i in range(10):
    blanco += color_sensor.reflected_light_intensity

blanco /= 10

while color_sensor.reflected_light_intensity < (blanco * 0.7):
    recto(1)



sound.beep()
print(f"Guardado en {nombre_archivo}")

sound.beep()
sleep(1)
