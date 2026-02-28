import math
from typing import Tuple
from config import FEMUR_LENGTH_MM, TIBIA_LENGTH_MM, COXA_LENGTH_MM

class IK:
    @staticmethod
    def solve(x, y, z, right_handed=True) -> Tuple[float, float, float]:
        if not right_handed:
            x, y = y, x

        # 1. Hip Angle (remains the same)
        hip_angle_rad = math.atan2(y, x)

        # 2. Total distance from the hip axis to the foot on the XY plane
        h_total = math.hypot(x, y)

        # 3. Effective horizontal reach for the Femur/Tibia triangle
        # We subtract the Coxa because it's a fixed horizontal distance
        h_eff = h_total - COXA_LENGTH_MM

        # 4. Actual reach length for the triangle (from femur start to foot)
        l = math.hypot(h_eff, z)

        # Reachability Check
        max_reach = FEMUR_LENGTH_MM + TIBIA_LENGTH_MM
        if l > max_reach:
            l = max_reach

        # 5. Solve Ankle (Law of Cosines)
        cos_ankle = (FEMUR_LENGTH_MM ** 2 + TIBIA_LENGTH_MM ** 2 - l ** 2) / (2 * FEMUR_LENGTH_MM * TIBIA_LENGTH_MM)
        ankle_angle_rad = math.acos(max(-1, min(1, cos_ankle)))

        # 6. Solve Knee
        # Part 1: Internal angle of the femur/tibia triangle
        knee_a = (l ** 2 + FEMUR_LENGTH_MM ** 2 - TIBIA_LENGTH_MM ** 2) / (2 * l * FEMUR_LENGTH_MM)
        knee_angle_part1 = math.acos(max(-1, min(1, knee_a)))

        # Part 2: Angle of the leg elevation relative to the floor
        knee_angle_part2 = math.atan2(z, h_eff)

        knee_angle_rad = knee_angle_part1 + knee_angle_part2

        return (
            math.degrees(hip_angle_rad),
            math.degrees(knee_angle_rad),
            math.degrees(ankle_angle_rad)
        )