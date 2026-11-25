#!/usr/bin/env python3
# sudo apt-get install python3-gpiod
# pip install gpiod
from time import sleep
import subprocess
import gpiod
from gpiod.line import Direction, Value, Bias

# Starts the ROS stack (krabi_color.service) ONCE, at boot, with or without the tirette, then
# only watches the poweroff button. Inserting the tirette no longer restarts ROS: to restart it
# (between two matches, after changing the colour), use RESTART COLOR on the GUI.
#
# --- BCM GPIO numbers (Pi 5: 40-pin header on gpiochip4) ---
# BOARD 36 -> BCM 16  (poweroff) — owned exclusively by this script
# The tirette (BOARD 38 -> BCM 20) is read by gpio.py only.
poweroff_chan = 16

GPIO_CHIP = "/dev/gpiochip4"  # Pi 5: 40-pin header is on gpiochip4 (pinctrl-rp1)

chip = gpiod.Chip(GPIO_CHIP)

def read_poweroff():
    with chip.request_lines(
        config={poweroff_chan: gpiod.LineSettings(direction=Direction.INPUT, bias=Bias.PULL_UP)},
        consumer="start_ros_poweroff"
    ) as req:
        return req.get_value(poweroff_chan) == Value.ACTIVE

def start_FoxGloveBridge():
    print("ros2 launch foxglove_bridge foxglove_bridge_launch.xml port:=8765")
    subprocess.Popen("ros2 launch foxglove_bridge foxglove_bridge_launch.xml port:=8765".split())
    sleep(2)

def startRos():
    # "start", not "restart": does nothing if ROS already runs. krabi.service restarts this
    # script if it crashes; that must never restart ROS during a match.
    print("sudo systemctl start krabi_color")
    subprocess.Popen("sudo systemctl start krabi_color".split())

def turn_off_robot():
    print("Poweroff!!!")
    subprocess.Popen(
        "sudo /usr/sbin/shutdown -h now".split(), stdout=subprocess.PIPE
    ).communicate()

def checkPowerOff():
    try:
        if not read_poweroff():
            turn_off_robot()
    except OSError:
        pass  # retry next cycle

if __name__ == '__main__':
    try:
        #start_FoxGloveBridge()
        startRos()
        while True:
            sleep(0.1)
            checkPowerOff()

    finally:
        chip.close()
