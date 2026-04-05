#!/usr/bin/env python3
# sudo apt-get install python3-gpiod
# pip install gpiod
from time import sleep
import subprocess
import gpiod
from gpiod.line import Direction, Value, Bias

# --- BCM GPIO numbers (Pi 5: 40-pin header on gpiochip4) ---
# BOARD 36 -> BCM 16  (poweroff) — owned exclusively by this script
# BOARD 38 -> BCM 20  (tirette)  — shared with gpio.py, polled with try/except
poweroff_chan = 16
tirette_chan  = 20

GPIO_CHIP = "/dev/gpiochip4"  # Pi 5: 40-pin header is on gpiochip4 (pinctrl-rp1)

chip = gpiod.Chip(GPIO_CHIP)

def read_poweroff():
    with chip.request_lines(
        config={poweroff_chan: gpiod.LineSettings(direction=Direction.INPUT, bias=Bias.PULL_UP)},
        consumer="start_ros_poweroff"
    ) as req:
        return req.get_value(poweroff_chan) == Value.ACTIVE

def read_tirette():
    """Returns True (high/not inserted) or False (low/inserted), or None if pin is busy."""
    try:
        with chip.request_lines(
            config={tirette_chan: gpiod.LineSettings(direction=Direction.INPUT, bias=Bias.PULL_UP)},
            consumer="start_ros_tirette"
        ) as req:
            return req.get_value(tirette_chan) == Value.ACTIVE
    except OSError:
        return None  # gpio.py is holding the pin, skip this poll

def killRos():
    print("sudo systemctl stop krabi_color")
    subprocess.Popen("sudo systemctl stop krabi_color".split())
    sleep(2)

def startRos():
    print("sudo systemctl restart krabi_color")
    subprocess.Popen("sudo systemctl restart krabi_color".split())

def startLidarService():
    print("sudo systemctl restart krabi_lidar")
    subprocess.Popen("sudo systemctl restart krabi_lidar".split())

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
        tirette_state = None

        # Wait for first successful tirette read
        while tirette_state is None:
            tirette_state = read_tirette()
            sleep(0.1)

        while True:
            # Wait for tirette insertion (goes low = False)
            while tirette_state is not False:
                sleep(0.1)
                checkPowerOff()
                val = read_tirette()
                if val is not None:
                    tirette_state = val

            killRos()
            checkPowerOff()
            startRos()
            sleep(1)  # debounce

            # Wait for tirette removal (goes high = True)
            while tirette_state is not True:
                sleep(0.1)
                checkPowerOff()
                val = read_tirette()
                if val is not None:
                    tirette_state = val

            sleep(1)  # debounce

    finally:
        chip.close()
