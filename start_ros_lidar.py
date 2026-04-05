#!/usr/bin/env python3
from time import sleep
import subprocess
import sys

def startRosLidar():
    bashCommand = "ros2 launch krabi_bringup krabi_lidars_launch.py useLidarLoc:=False"
    subprocess.Popen(bashCommand.split(), stdout=sys.stdout, stderr=sys.stderr).communicate()


if __name__ == '__main__':
    program = startRosLidar()

