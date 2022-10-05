#!/bin/bash
cd /mnt/test/practice_ws ; catkin_make ; source devel/setup.bash ; roslaunch model_gazebo ar_sensor_world.launch paused:=true&
sleep 100 ;cd /mnt/test/practice_ws/src/model_gazebo/src ; python DB_shoot.py ; killall -9 gzclient ; killall -9 gzserver ; python Trim.py ;python Renzoku_miss.py &