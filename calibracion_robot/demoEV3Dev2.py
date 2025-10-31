#!/usr/bin/env python3
from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor
from ev3dev2.led import Leds
from time import sleep
from ev3dev2.motor import LargeMotor, OUTPUT_A
import os
from ev3dev2.sound import Sound

os.system('setfont Lat15-TerminusBold14')

sound = Sound()

sound.beep()
sound.speak( "Hi" )

leds = Leds()

print( 'Starting Leds' )
sound.beep()
sleep(1)

leds.set_color('LEFT',  'RED')
leds.set_color('RIGHT', 'RED')

sound.beep()
sleep(1)

leds.set_color('LEFT',  'GREEN')
leds.set_color('RIGHT', 'GREEN')

print( 'Starting Motor' )
sound.beep()
sleep(1)


lm = LargeMotor()
lm.on_for_degrees(speed=10, degrees=90, brake=True, block=True)
print('Actual angle for commanded 90 (before sleep1)= ' + str(lm.position) + ' deg')
sleep(1)
print('Actual angle for commanded 90 (after sleep1)= ' + str(lm.position) + ' deg')

print( 'Reading US' )
sound.beep()
sleep(1)

for  i in range(3):
    us = UltrasonicSensor()

    print(str(i) + ': ' + str(us.distance_centimeters) + ' cm')

    sound.beep()
    sleep(1)


f = open( 'test.txt', 'w' )
f.write( '1: ' + str(us.distance_centimeters) + ' cm\n' )
f.write( '2: ' + str(us.distance_centimeters) + ' cm\n' )
f.close(  )

