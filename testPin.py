from __future__ import print_function
import RPi.GPIO as GPIO # python3 -m pip install RPi.GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

chan_list = [22, 24, 26, 32, 36, 38, 40]
for channel in chan_list:
    print("init channel " + str(channel))
    GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	
while True:
    for channel in chan_list:
        print(str(channel) + " = " + str(GPIO.input(channel)),end='  ')
	
    print()
    sleep(0.2)


