import math
from typing import Tuple
from config import FEMUR_LENGTH_MM, TIBIA_LENGTH_MM

# Assuming FEMUR_LENGTH_MM and TIBIA_LENGTH_MM are imported from config

class IK:
    @staticmethod
    def solve(x, y, z, right_handed=True) -> Tuple[float, float, float]:
        # 1. Coordinate System Adjustment
        if not right_handed:
            x, y = y, x  # Proper way to swap in Python

        # 2. Distance Calculations
        h = math.hypot(x, y)  # Distance on the XY plane
        l = math.hypot(h, z)  # Total distance from hip to foot

        # 3. Reachability Check (Prevent acos crashes)
        max_reach = FEMUR_LENGTH_MM + TIBIA_LENGTH_MM
        min_reach = abs(FEMUR_LENGTH_MM - TIBIA_LENGTH_MM)

        if l > max_reach or l < min_reach:
            # Handle out-of-bounds: clip to max reach or raise error
            l = max_reach if l > max_reach else min_reach

        # 4. Solve Hip Angle
        hip_angle_rad = math.atan2(x, y)

        # 5. Solve Ankle (Knee-to-Tibia) Angle
        # Using Law of Cosines: c^2 = a^2 + b^2 - 2ab*cos(C)
        cos_ankle = (FEMUR_LENGTH_MM ** 2 + TIBIA_LENGTH_MM ** 2 - l ** 2) / (2 * FEMUR_LENGTH_MM * TIBIA_LENGTH_MM)
        # Standardize range to avoid floating point errors slightly outside [-1, 1]
        ankle_angle_rad = math.acos(max(-1, min(1, cos_ankle)))

        # 6. Solve Knee (Hip-to-Femur) Angle
        # Angle between femur and the line 'l'
        knee_a = (l ** 2 + FEMUR_LENGTH_MM ** 2 - TIBIA_LENGTH_MM ** 2) / (2 * l * FEMUR_LENGTH_MM)
        knee_angle_part1 = math.acos(max(-1, min(1, knee_a)))

        # Angle of the leg elevation
        knee_angle_part2 = math.atan2(z, h)

        knee_angle_rad = knee_angle_part1 + knee_angle_part2

        return (
            math.degrees(hip_angle_rad),
            math.degrees(knee_angle_rad),
            math.degrees(ankle_angle_rad)
        )