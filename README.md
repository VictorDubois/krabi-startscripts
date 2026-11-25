Configuration of the Raspberry Pi of the robot Krabi, which runs on [Ubuntu 24.04 server](https://releases.ubuntu.com/24.04.4/ubuntu-24.04.4-live-server-amd64.iso), and [ROS2 Jazzy](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html)

[installDep.sh](https://github.com/VictorDubois/krabi-startscripts/blob/main/installDep.sh) installs necessary dependencies, and [initVenv.sh](https://github.com/VictorDubois/krabi-startscripts/blob/main/initVenv.sh) initialize the necessary python venv

.services files are to be placed in /etc/systemd/system/

To autostart at boot, then run:
```
sudo systemctl enable krabi.service
sudo systemctl enable krabi_lidar.service
sudo systemctl enable krabi_gui.service
sudo systemctl enable krabi-can.service
```
Note : krabi_color.service is started by krabi.service, depending on the team color selected. It must not be enabled

krabi.service (start_ros.py) starts krabi_color.service once, at boot, with or without the tirette: inserting the tirette no longer restarts ROS. To restart ROS (between two matches, after changing the colour), use the RESTART COLOR button of the GUI. See [RECALAGE.md](https://github.com/VictorDubois/goal_strategy/blob/main/docs/RECALAGE.md) (in French).

boot_firmware_config.txt is a copy of /boot/firmware/config.txt

To rotate the logs, use `crontab -e`, based upon the example in [crontab_logrotate](https://github.com/VictorDubois/krabi-startscripts/blob/main/crontab_logrotate)
