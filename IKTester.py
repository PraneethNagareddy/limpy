from inverse_kinematics import IK
from adafruit_servokit import ServoKit
from driver import *

import time
import sys


if not len(sys.argv) != 3:
        print("invalid usage. Provide exactly three arguments, i.e X,Y,Z co-ordinates")

X = int(sys.argv[1])
Y = int(sys.argv[2])
Z = int(sys.argv[3])


angles = IK.solve(X,Y,Z)
print("Servo Angles:", angles)

i2c_address = 0x40
leg = middle_left_leg

hip_joint_channel = leg.hip_joint.joint_config.channel
knee_joint_channel = leg.knee_joint.joint_config.channel
ankle_joint_channel = leg.ankle_joint.joint_config.channel

kit = ServoKit(channels = 16, address=0x40)
kit.servo[hip_joint_channel].set_pulse_width_range(450, 2650)
kit.servo[knee_joint_channel].set_pulse_width_range(450, 2650)
kit.servo[ankle_joint_channel].set_pulse_width_range(450, 2650)

kit.servo[hip_joint_channel].angle = angles[0]
time.sleep(0.5)
kit.servo[knee_joint_channel].angle = angles[1]
time.sleep(0.5)
kit.servo[ankle_joint_channel].angle = angles[2]