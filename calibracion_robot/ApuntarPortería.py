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
    large_motor_r.on_for_degrees(speed=velocidad, degrees=grados_motor, brake=True, block=False)

def parar():
    large_motor_l.off(brake=True)
    large_motor_r.off(brake=True)

def girar(grados_robot, velocidad=25, block=False):
    # perímetro del círculo que trazan las ruedas al girar
    perimetro_giro_robot = pi * DISTANCIA_RUEDAS
    distancia_a_recorrer = (grados_robot / 360) * perimetro_giro_robot
    
    # distancia a grados del motor
    vueltas_rueda = distancia_a_recorrer / PERIMETRO_RUEDA
    grados_motor = vueltas_rueda * 360

    large_motor_l.on_for_degrees(speed=velocidad, degrees=grados_motor, brake=True, block=False)
    large_motor_r.on_for_degrees(speed=velocidad, degrees=-grados_motor, brake=True, block=block)


def buscar_palos():
    angulo = 0
    palo1 = None
    palo2 = None

    distancia_prev = ultrasonic_sensor.distance_centimeters

    while angulo < 180:
        girar(2, velocidad=10, block=True)  
        sleep(0.05)
        angulo += 2

        distancia_actual = ultrasonic_sensor.distance_centimeters

        if distancia_actual < distancia_prev * 0.7:
            sound.beep()

            if palo1 is None:
                palo1 = angulo
            elif palo2 is None:
                palo2 = angulo
                break 

        distancia_prev = distancia_actual

    return palo1, palo2, angulo

os.system('setfont Lat15-TerminusBold14')

sound = Sound()
sound.beep()


blanco = 0
for i in range(10):
    blanco += color_sensor.reflected_light_intensity

blanco /= 10

# Etapa 1: Buscar línea
recto(2)
while color_sensor.reflected_light_intensity > (blanco * 0.7):
    continue
parar()
sound.beep()

# Etapa 2: Girar y medir

palo1, palo2, angulo_final = buscar_palos()


if palo1 is None or palo2 is None:
    print("No se detectaron dos palos.")
else:
    print("Palo 1:", palo1, "grados")
    print("Palo 2:", palo2, "grados")

    centro = (palo1 + palo2) / 2
    delta = centro - angulo_final
    girar(delta, velocidad=15, block=True)
    sound.beep()



sound.beep()

sound.beep()





