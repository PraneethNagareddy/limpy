import logging
import math
from typing import Tuple
from config import FEMUR_LENGTH_MM, TIBIA_LENGTH_MM, COXA_LENGTH_MM, COXA_Z_OFFSET_MM


class IK:
    @staticmethod
    def solve(x, y, z, right_handed=True) -> Tuple[float, float, float]:
        if not right_handed:
            x, y = y, x

        # 1. Hip Angle
        hip_angle_rad = math.atan2(y, x)

        # 2. Geometry Correction for Scenario Z
        h_total = math.hypot(x, y)
        h_eff = h_total - COXA_LENGTH_MM
        z_eff = z - COXA_Z_OFFSET_MM  # This accounts for the 'step' in the coxa

        # 3. New 'L' based on corrected coordinates
        l = math.hypot(h_eff, z_eff)

        # Reachability Check
        max_reach = FEMUR_LENGTH_MM + TIBIA_LENGTH_MM
        l = min(l, max_reach)

        # 4. Law of Cosines (Ankle/Tibia)
        cos_ankle = (FEMUR_LENGTH_MM ** 2 + TIBIA_LENGTH_MM ** 2 - l ** 2) / (2 * FEMUR_LENGTH_MM * TIBIA_LENGTH_MM)
        ankle_angle_rad = math.acos(max(-1, min(1, cos_ankle)))

        # 5. Knee/Femur Angle
        knee_a = (l ** 2 + FEMUR_LENGTH_MM ** 2 - TIBIA_LENGTH_MM ** 2) / (2 * l * FEMUR_LENGTH_MM)
        knee_angle_part1 = math.acos(max(-1, min(1, knee_a)))

        # Use the corrected z_eff and h_eff here!
        knee_angle_part2 = math.atan2(z_eff, h_eff)

        knee_angle_rad = knee_angle_part1 + knee_angle_part2
        logging.info("IK Angles:", math.degrees(hip_angle_rad), math.degrees(knee_angle_rad), math.degrees(ankle_angle_rad))

        return get_servo_angles(
            math.degrees(hip_angle_rad),
            math.degrees(knee_angle_rad),
            math.degrees(ankle_angle_rad)
        )


def get_servo_angles(ik_hip, ik_knee, ik_ankle, mount_angle=45):
    # 1. Hip: Center is 90 at mount_angle
    # ik_hip increases -> servo moves further away from 0.
    s_hip = 90 + (ik_hip - mount_angle)

    # 2. Knee: Direct Mapping
    # 0 = Up, 90 = Horizontal, 180 = Down.
    # ik_knee follows this naturally.
    s_knee = 180 - ik_knee

    # 3. Ankle: Direct Mapping
    # 0 = Inward, 90 = Vertical, 180 = Outward.
    # When ik_ankle is 90 (right angle), the tibia is vertical.
    # When ik_ankle increases (leg straightens), servo moves toward 180.
    s_ankle = ik_ankle

    return s_hip, s_knee, s_ankle