#!/usr/bin/env python3
from time import sleep
import subprocess
import rclpy
from std_msgs.msg import Bool
from std_msgs.msg import String
import RPi.GPIO as GPIO
import sys

poweroff_chan = 36
tirette_chan = 38
color_chan = 40
GPIO.setmode(GPIO.BOARD)

def init_pins():
    chan_list = [poweroff_chan, tirette_chan, color_chan]
    for channel in chan_list:
        print("init channel " + str(channel))
        GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def startRos():
    isBluestr = "False"
    xPos = "0.275"
    yPos = "0.775"
    zRot = "-1.570796327"

    if isBlue():
        isBluestr = "True"
        xPos = "-0.275"
        yPos = "0.775"
        zRot = "-1.570796327"
    bashCommand = "ros2 launch krabi_bringup krabi_launch.py isSimulation:=False isBlue:=" + isBluestr + " useLidarLoc:=False useTimInsteadOfNeato:=True xRobotPos:=" + xPos + " yRobotPos:=" + yPos + " zRobotOrientation:=" + zRot # Works, but killing does not :/
    #bashCommand = "ros2 launch krabi_bringup krabossColor.launch.py isSimulation:=False isBlue:=" + isBluestr + " useLidarLoc:=False useTimInsteadOfNeato:=True"
    #bashCommand = "/usr/bin/nice -n -20 ros2 launch krabi_bringup krabossColor.launch.py isSimulation:=False isBlue:=" + isBluestr + " useLidarLoc:=False useTimInsteadOfNeato:=True"
    #subprocess.Popen(bashCommand.split())
    #subprocess.run(bashCommand.split(), capture_output=True)
    subprocess.Popen(bashCommand.split(), stdout=sys.stdout, stderr=sys.stderr).communicate()

def isBlue():
    blue = GPIO.input(color_chan)
    print("Is blue: " + str(blue))
    return blue

if __name__ == '__main__':
    init_pins()
    program = None
    program = startRos()

