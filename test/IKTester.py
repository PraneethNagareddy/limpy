from inverse_kinematics import IK
from adafruit_servokit import ServoKit

import time
import sys

angles = IK.solve(90,10,-40)
print(angles)

kit = ServoKit(channels = 16, address=0x40)

kit.servo[14].angle = angles[0]
time.sleep(0.5)
kit.servo[12].angle = angles[1]
time.sleep(0.5)
kit.servo[0].angle = angles[2]