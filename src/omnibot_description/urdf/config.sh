#!/bin/bash

  mv base_visual.stl base.stl && mv base.stl ../meshes/
  mv motor_2_visual.stl motor.stl && mv motor.stl ../meshes/
  mv roller_2_visual.stl roller.stl && mv roller.stl ../meshes/
  mv spacer.stl ../meshes/
  mv wheel_2_visual.stl wheel.stl && mv wheel.stl ../meshes/
  rm *.stl && rm *.part
  sed -i 's#omnibot_description/urdf#omnibot_description/meshes#g' robot.urdf
  sed -i 's#/base_[^\"]*#/base.stl#g' robot.urdf
  sed -i 's#meshes/motor[^\"]*#meshes/motor.stl#g' robot.urdf
  sed -i 's#meshes/roller[^\"]*#meshes/roller.stl#g' robot.urdf
  sed -i 's#meshes/wheel[^\"]*#meshes/wheel.stl#g' robot.urdf

  sed -i '1s|^|<?xml version="1.0"?>\n|' robot.urdf
#  sed -i "3i\<xacro:include filename=\"\$(find omnibot_description)/urdf/omnibot_gazebo.xacro\"/>" robot.urdf
#  sed -i "4i\<xacro:include filename=\"\$(find omnibot_description)/urdf/omnibot_ros2_control.xacro\"/>" robot.urdf

  sed -i 's#<robot name="omnibot">#<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="omnibot">#g' robot.urdf
  sed -i 's/revolute/continuous/g' robot.urdf
  sed -i 's/base_link/base_footprint/g' robot.urdf

  mv robot.urdf omnibot.urdf.xacro
