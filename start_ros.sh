#!/bin/bash
source /opt/ros/jazzy/setup.bash
source /home/ubuntu/startScripts/venvStartRos/bin/activate
source /home/ubuntu/krabi_ws/install/setup.bash
export ROS_DOMAIN_ID=0

python3 /home/ubuntu/startScripts/start_ros.py
