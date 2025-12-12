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


large_motor_l = LargeMotor(OUTPUT_B)
large_motor_r = LargeMotor(OUTPUT_A)

ultrasonic_sensor = UltrasonicSensor(INPUT_2)
color_sensor = ColorSensor(INPUT_1)

DIAMETRO_RUEDA = 0.055
DISTANCIA_RUEDAS = 0.1147
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

with open(nombre_archivo, 'a') as archivo:
    archivo.write("grados,distancia_ultrasonido,intensidad_luz\n")
    
    for grado_actual in range(360):
        distancia = ultrasonic_sensor.distance_centimeters
        luz = color_sensor.reflected_light_intensity
        print("G:{} | D:{:.1f}cm | L:{}%".format(grado_actual, distancia, luz))
        archivo.write("{},{},{}\n".format(grado_actual, distancia, luz))

        girar(1)

sound.beep()
print("Guardado en {}".format(nombre_archivo))

sound.beep()
sleep(1)
