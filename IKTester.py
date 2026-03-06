from inverse_kinematics import IK
from adafruit_servokit import ServoKit
from driver import *
from config import *

import time
import sys


if not len(sys.argv) != 3:
        print("invalid usage. Provide exactly three arguments, i.e X,Y,Z co-ordinates")

#X = int(sys.argv[1])
#Y = int(sys.argv[2])
#Z = int(sys.argv[3])

(X,Y,Z) = INIT_COORDINATES
#angles = IK.solve(X,Y,Z)
leg = front_right_leg

leg.move_to_position(X, Y, Z)

#(hip_angle, knee_angle, ankle_angle) = leg.convert_IK_to_servo_angles(angles[0], angles[1], angles[2])

#print("Hip Angle:", hip_angle)
#print("Knee Angle:", knee_angle)
#print("Ankle Angle:", ankle_angle)

#hip_joint_channel = leg.hip_joint.joint_config.channel
#knee_joint_channel = leg.knee_joint.joint_config.channel
#ankle_joint_channel = leg.ankle_joint.joint_config.channel

#kit = ServoKit(channels = 16, address=0x40)
#kit.servo[hip_joint_channel].set_pulse_width_range(450, 2650)
#kit.servo[knee_joint_channel].set_pulse_width_range(450, 2650)
#kit.servo[ankle_joint_channel].set_pulse_width_range(450, 2650)

#kit.servo[hip_joint_channel].angle = hip_angle
#time.sleep(0.5)
#kit.servo[knee_joint_channel].angle = knee_angle
#time.sleep(0.5)
#kit.servo[ankle_joint_channel].angle = ankle_angle