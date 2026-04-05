#!/usr/bin/env python3
# sudo apt-get install python3-gpiod
# pip install gpiod
import subprocess
import sys
import gpiod
from gpiod.line import Direction, Value, Bias

# BOARD 40 -> BCM 21  (color) — owned exclusively by this script
color_chan = 21
GPIO_CHIP = "/dev/gpiochip4"  # Pi 5: 40-pin header is on gpiochip4 (pinctrl-rp1)

chip = gpiod.Chip(GPIO_CHIP)
gpio_request = chip.request_lines(
    config={
        color_chan: gpiod.LineSettings(direction=Direction.INPUT, bias=Bias.PULL_UP),
    },
    consumer="start_ros_color"
)

def isBlue():
    blue = gpio_request.get_value(color_chan) == Value.ACTIVE
    print("Is blue: " + str(blue))
    return blue

def startRos():
    isBluestr = "True" if isBlue() else "False"

    xPos = "1.25"
    yPos = "-0.75"
    zRot = "1.570796327"

    if isBluestr == "True":
        xPos = "-1.25"
        yPos = "-0.75"
        zRot = "1.570796327"

    bashCommand = (
        "ros2 launch krabi_bringup krabi_launch.py"
        " isSimulation:=False"
        " isBlue:=" + isBluestr +
        " useLidarLoc:=False"
        " useTimInsteadOfNeato:=True"
        " xRobotPos:=" + xPos +
        " yRobotPos:=" + yPos +
        " zRobotOrientation:=" + zRot +
        " use_aruco:=True" + 
        " do_record:=True"
    )
    print(bashCommand)
    subprocess.Popen(bashCommand.split(), stdout=sys.stdout, stderr=sys.stderr).communicate()

if __name__ == '__main__':
    try:
        startRos()
    finally:
        gpio_request.release()
        chip.close()
