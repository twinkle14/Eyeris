import RPi.GPIO as GPIO
import time
from subprocess import call#to call espeak function
import os

cmd_beg = "espeak "
#text ="This is a sample code to speal in Raspberry PI"
cmd_out=" -ven+m1 -s 150 -a 300"
GPIO.setwarnings(False)
Listen_mode=26
s=21
GPIO.setmode(GPIO.BCM)
GPIO.setup((Listen_mode,s), GPIO.OUT)
while True:
    print('running')
    '''GPIO.output(Listen_mode,1)
    time.sleep(0.5)
    GPIO.output(Listen_mode,0)
    time.sleep(0.5)'''
    result="Copy"
    call(cmd_beg+"\""+result+"\""+cmd_out,shell=True)