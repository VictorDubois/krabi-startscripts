#!/usr/bin/env python3
from time import sleep
import subprocess
import rclpy
import sys
from std_msgs.msg import Bool
from std_msgs.msg import String
import RPi.GPIO as GPIO # python3 -m pip install RPi.GPIO
#python3 -m pip install pyyaml
#sudo apt install rpi.gpio-common

poweroff_chan = 36
tirette_chan = 38
color_chan = 40
GPIO.setmode(GPIO.BOARD)

def init_pins():
    chan_list = [poweroff_chan, tirette_chan, color_chan]
    for channel in chan_list:
        print("init channel " + str(channel))
        GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def killRos():
    print("sudo systemctl stop krabi_color")
    bashCommand = "sudo systemctl stop krabi_color"
    subprocess.Popen(bashCommand.split())
    sleep(2)
    #subprocess.run(["killall", "ros2"])

def startRos():
    isBluestr = "False"
    if isBlue():
        isBluestr = "True"
    #bashCommand = "ros2 launch krabi_bringup krabi_launch.py isSimulation:=False isBlue:=" + isBluestr + " useLidarLoc:=False useTimInsteadOfNeato:=True" # Works, but killing does not :/
    #bashCommand = "sudo systemctl restart krabi_isBlue@" + isBluestr
    print("sudo systemctl restart krabi_color")
    bashCommand = "sudo systemctl restart krabi_color"
    #bashCommand = "ros2 launch krabi_bringup krabossColor.launch.py isSimulation:=False isBlue:=" + isBluestr + " useLidarLoc:=False useTimInsteadOfNeato:=True"
    #bashCommand = "/usr/bin/nice -n -20 ros2 launch krabi_bringup krabossColor.launch.py isSimulation:=False isBlue:=" + isBluestr + " useLidarLoc:=False useTimInsteadOfNeato:=True"
    subprocess.Popen(bashCommand.split())

def startLidarService():
    print("sudo systemctl restart krabi_lidar")
    bashCommand = "sudo systemctl restart krabi_lidar"
    subprocess.Popen(bashCommand.split())

def isBlue():
    blue = GPIO.input(color_chan)
    print("Is blue: " + str(blue))
    return blue

def turn_off_robot():
    print("Poweroff!!!")
    #bashCommand = "sudo poweroff"
    bashCommand = "sudo /usr/sbin/shutdown -h now"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

def checkPowerOff():
    if not GPIO.input(poweroff_chan):
        turn_off_robot()

if __name__ == '__main__':
    init_pins()
    program = None
    # Start lidars, as they are too slow to shutdown
    #bashCommand = "ros2 launch krabi_bringup krabi_lidars_launch.py useLidarLoc:=False useTimInsteadOfNeato:=True"
    #subprocess.Popen(bashCommand.split())
    #startLidarService()
    while True:
        while GPIO.input(tirette_chan):
            sleep(0.1)
            checkPowerOff()

        if program:
            program.terminate()
        killRos()
        checkPowerOff()
        program = startRos()
        sleep(1)  # debounce

        while not GPIO.input(tirette_chan):
            checkPowerOff()
            sleep(0.1)

        sleep(1)  # debounce

