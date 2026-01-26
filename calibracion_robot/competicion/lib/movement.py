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

large_motor_l = LargeMotor(OUTPUT_B)
large_motor_r = LargeMotor(OUTPUT_A)
arm_motor = MediumMotor(OUTPUT_D)

ultrasonic_sensor = UltrasonicSensor(INPUT_2)
color_sensor = ColorSensor(INPUT_1)

DIAMETRO_RUEDA = 0.055
DISTANCIA_RUEDAS = 0.105
PERIMETRO_RUEDA = pi * DIAMETRO_RUEDA


def recto(distancia_m, velocidad=25, block=False):
    vueltas_rueda = distancia_m / PERIMETRO_RUEDA
    grados_motor = vueltas_rueda * 360

    large_motor_l.on_for_degrees(speed=velocidad, degrees=grados_motor, brake=True, block=False)
    large_motor_r.on_for_degrees(speed=velocidad, degrees=grados_motor, brake=True, block=block)

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

def girar_solo_izquierda(grados_robot, velocidad=25, block=True):
    # perímetro del círculo que trazan las ruedas al girar
    perimetro_giro_robot = pi * DISTANCIA_RUEDAS
    distancia_a_recorrer = (grados_robot / 360) * perimetro_giro_robot

    # distancia a grados del motor
    vueltas_rueda = distancia_a_recorrer / PERIMETRO_RUEDA
    grados_motor = vueltas_rueda * 360

    large_motor_l.on_for_degrees(speed=velocidad, degrees=grados_motor, brake=False, block=block)

def girar_solo_derecha(grados_robot, velocidad=25, block=True):
    # perímetro del círculo que trazan las ruedas al girar
    perimetro_giro_robot = pi * DISTANCIA_RUEDAS
    distancia_a_recorrer = (grados_robot / 360) * perimetro_giro_robot

    # distancia a grados del motor
    vueltas_rueda = distancia_a_recorrer / PERIMETRO_RUEDA
    grados_motor = vueltas_rueda * 360

    large_motor_r.on_for_degrees(speed=velocidad, degrees=grados_motor, brake=False, block=block)

def girar_con_accion(accion, tiempo_espera=0.005, grados_robot=360, velocidad=5):
    girar(grados_robot, velocidad, block=False)

    while large_motor_r.is_running or large_motor_l.is_running:
        accion()
        time.sleep(tiempo_espera)

def subir_brazo():
    arm_motor.on_for_degrees(speed=20, degrees=-40, brake=True, block=True)
    sleep(1)
    arm_motor.on_for_degrees(speed=20, degrees=40, brake=True, block=True)
