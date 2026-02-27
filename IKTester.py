from inverse_kinematics import IK
from adafruit_servokit import ServoKit

import time
import sys


if not len(sys.argv) != 3:
        print("invalid usage. Provide exactly three arguments, i.e X,Y,Z co-ordinates")

X = int(sys.argv[1])
Y = int(sys.argv[2])
Z = int(sys.argv[3])


angles = IK.solve(X,Y,Z)
print(angles)

kit = ServoKit(channels = 16, address=0x40)

kit.servo[14].angle = angles[0]
time.sleep(0.5)
kit.servo[12].angle = angles[1]
time.sleep(0.5)
kit.servo[0].angle = angles[2]