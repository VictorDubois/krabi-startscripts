#!/bin/bash
source /opt/ros/jazzy/setup.bash
source /home/ubuntu/krabi_ws/install/setup.bash
source /home/ubuntu/startScripts/venvStartRos/bin/activate
export ROS_DOMAIN_ID=0

python3 /home/ubuntu/startScripts/start_ros_color.py
#/opt/ros/humble/bin/ros2 launch krabi_bringup krabi_launch.py isSimulation:=false isBlue:=$1 useLidarLoc:=false useTimInsteadOfNeato:=true


