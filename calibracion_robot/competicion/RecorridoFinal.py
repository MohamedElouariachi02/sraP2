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

from lib.movement import girar, girar_con_accion, girar_solo_derecha, girar_solo_izquierda, recto, parar, subir_brazo
from lib.measurements import analizar_valles, ancho_angular_porteria, calibrar_sensor_color_en_movimiento, seguir_linea

VELOCIDAD_GIROS_GRANDES = 20

large_motor_l = LargeMotor(OUTPUT_B)
large_motor_r = LargeMotor(OUTPUT_A)
arm_motor = MediumMotor(OUTPUT_D)

ultrasonic_sensor = UltrasonicSensor(INPUT_2)
color_sensor = ColorSensor(INPUT_1)
leds = Leds()


def avanzar_hasta_linea(media_ref, umbral_ref, velocidad=20, max_distancia_m=2):
    recto(max_distancia_m, velocidad, block=False)
    delta = abs(media_ref - umbral_ref)
    limite_inferior = media_ref - delta
    limite_superior = media_ref + delta

    while large_motor_l.is_running or large_motor_r.is_running:
        lectura = color_sensor.reflected_light_intensity
        if lectura < limite_inferior or lectura > limite_superior:
            parar()
            break
        time.sleep(0.005)


os.system('setfont Lat15-TerminusBold14')

sound = Sound()
sound.beep()
leds.all_off()
leds.set_color("LEFT", "AMBER")
leds.set_color("RIGHT", "AMBER")

media, umbral = calibrar_sensor_color_en_movimiento(color_sensor, distancia_m=.1, n_muestras=10, desviaciones_sigma=3)

avanzar_hasta_linea(media, umbral, velocidad=20, max_distancia_m=2)

points = []
girar_con_accion(
    lambda: points.append((time.time(), ultrasonic_sensor.distance_centimeters)),
    tiempo_espera=0.5/360,
    grados_robot=360,
    velocidad=20
)
print("Puntos obtenidos: ", len(points))

valles = analizar_valles(points, umbral_distancia=200, max_salto=30, grados_totales=360)

min_ancho, max_ancho = ancho_angular_porteria()
min_ancho = 1

mejor_valle = min(
    filter(
        lambda valle: valle[2] > min_ancho and valle[2] < max_ancho,
        valles
    ),
    key=lambda item: item[1]
)
if mejor_valle is None:
    print("No se encontraron valles con ancho angular dentro de los limites")
    exit()

# 6 seg -> 0.20 m
seguir_linea(
    media,
    umbral,
    direccion_derecha=mejor_valle[0] < 180,
    distancia_m=max(mejor_valle[1] - 40, 0.0) / 100.0,
    seg_p_m=25
)

print("dir mejor valle ", mejor_valle[0] < 180)
print("distancia ", max(mejor_valle[1] - 30, 0.0) / 100.0)

# hacer segundo barrido
sleep(0.01)
girar(-90, 40, True)
sleep(0.5)
points = []
girar_con_accion(
    lambda: points.append((time.time(), ultrasonic_sensor.distance_centimeters)),
    tiempo_espera=1/360,
    grados_robot=180,
    velocidad=5
)
valles = analizar_valles(points, umbral_distancia=60, max_salto=20, grados_totales=180)
palos = sorted(valles, key=lambda valle: valle[1])[:2]
print("Puntos obtenidos cerca de la porteria: ", len(points))
print("angs: ", [palo[0] for palo in palos])

distancia_porteria = 0
if len(palos) == 1:
    angulo_a_girar = palos[0][0] #- 180
    distancia_porteria = palos[0][1]
    print("ang_valle: ", round(palos[0][0], 1), ", ang_a_girar: ", round(angulo_a_girar, 1))
    girar(angulo_a_girar, 30, True)
elif len(palos) == 2:
    angulo_medio = (palos[0][0] + palos[1][0]) / 2.0
    angulo_a_girar = angulo_medio #- 180
    distancia_porteria = (palos[0][1] + palos[1][1]) / 2.0
    print("ang_valle: ", round(angulo_medio, 1), ", ang_a_girar: ", round(angulo_a_girar, 1))
    girar(angulo_a_girar, 30, True)
else:
    time.sleep(1)
    sound = Sound()
    sound.beep()
    sound.beep()
    sound.beep()
    sleep(20)
    exit()

# tirar a porteria
sound.beep()
leds.all_off()
leds.set_color("LEFT", "RED")
leds.set_color("RIGHT", "RED")
sleep(0.1)
subir_brazo()
sleep(0.5)

# celebrar?
girar(180, 50, True)
seguir_linea(
    media,
    umbral,
    direccion_derecha=mejor_valle[0] < 180,
    distancia_m=max((distancia_porteria-5)/100.0, 0),
    seg_p_m=25
)
sound.beep()
leds.all_off()
leds.set_color("LEFT", "GREEN")
leds.set_color("RIGHT", "GREEN")
sleep(20)
exit()
