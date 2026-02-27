import math
from typing import Tuple
from config import *

class IK:

    @staticmethod
    def solve(x,y,z, right_handed_coordinate_system=True) -> Tuple[float, float, float]:
        #adjust axes for left-handed co-ordinate system
        if not right_handed_coordinate_system:
            IK.__swap(x, y)

        h = math.hypot(x, y)
        l = math.hypot(h,z)

        print("Value of H: {}", h)
        print("Value of L: {}", l)

        #Solve hip angle
        hip_angle_radians = math.atan2(x,y)

        #Solve ankle angle

        print( (FEMUR_LENGTH_MM**2 + TIBIA_LENGTH_MM**2 - (l**2)) / (2 * FEMUR_LENGTH_MM * TIBIA_LENGTH_MM))

        ankle_angle_radians = math.acos( ((FEMUR_LENGTH_MM**2 + TIBIA_LENGTH_MM**2 - (l**2)) / (2 * FEMUR_LENGTH_MM * TIBIA_LENGTH_MM)) )

        #Solve knee angle
        knee_angle_part1_radians = math.acos( (l**2 + FEMUR_LENGTH_MM**2 - TIBIA_LENGTH_MM**2) / (2 * l * FEMUR_LENGTH_MM) )
        knee_angle_part2_radians = math.atan2(z,h)

        knee_angle_radians = knee_angle_part1_radians + knee_angle_part2_radians

        #TO-DO
        #1. Adjust the hip angle relative to the attach angle 1.e 90
        #2. Calculations assume (0,0,0) is the hip joint point. Adjust the Z so that the foot touches the ground

        return math.degrees(hip_angle_radians),math.degrees(knee_angle_radians),math.degrees(ankle_angle_radians)

    @staticmethod
    def __swap(x, y):
        temp = x
        x = y
        y = temp