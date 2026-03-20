import logging
import math
from typing import Tuple
from config import FEMUR_LENGTH_MM, TIBIA_LENGTH_MM, COXA_LENGTH_MM, COXA_Z_OFFSET_MM, FEMUR_Z_OFFSET_MM


class IK:
    @staticmethod
    def solve(x, y, z) -> Tuple[float, float, float]:
        # --- YOUR SPECIFIC CONFIGS ---
        COXA_LEN = 40.0
        FEMUR_H = 55.3  # Horizontal span of the femur bracket
        TIBIA_L = 100.0
        COXA_Z_OFFSET = 15.0  # 15mm rise from Hip to Knee
        FEMUR_Z_OFFSET = -23.0  # 23mm drop from Knee to Ankle

        # 1. THE GEOMETRIC FIX: True Femur Diagonal
        # The 'bone' is the hypotenuse of the 55.3mm span and 23mm drop
        true_femur_len = math.hypot(FEMUR_LENGTH_MM, abs(FEMUR_Z_OFFSET_MM))  # ~59.9mm

        # The 'Mount Angle' (gamma) of the femur bracket
        # This is the angle between horizontal and the true pivot-to-pivot line
        femur_mount_angle = math.degrees(math.atan2(abs(FEMUR_Z_OFFSET_MM), FEMUR_LENGTH_MM))  # ~22.6°

        # 2. Hip Angle (Swing)
        hip_deg = math.degrees(math.atan2(y, x))

        # 3. Reach Calculation
        h_total = math.hypot(x, y)
        l_reach = h_total - COXA_LENGTH_MM

        # Target Z relative to the Knee pivot (Knee is at Z=+15)
        z_rel_to_knee = z - COXA_Z_OFFSET_MM

        # 4. 3D Distance 'd' (Knee pivot to Foot tip)
        d = math.hypot(l_reach, z_rel_to_knee)
        d = min(d, true_femur_len + TIBIA_LENGTH_MM)  # Safety clamp

        # 5. Law of Cosines (Using the TRUE diagonal femur length)
        # Angle at Ankle (Internal Triangle Angle)
        cos_tibia = (true_femur_len ** 2 + TIBIA_LENGTH_MM ** 2 - d ** 2) / (2 * true_femur_len * TIBIA_LENGTH_MM)
        tibia_internal_deg = math.degrees(math.acos(max(-1, min(1, cos_tibia))))

        # Angle at Knee (alpha - internal triangle angle)
        cos_femur = (true_femur_len ** 2 + d ** 2 - TIBIA_LENGTH_MM ** 2) / (2 * true_femur_len * d)
        alpha = math.degrees(math.acos(max(-1, min(1, cos_femur))))

        # 6. Beta (Slope of the reach line 'd' from the Knee pivot)
        beta = math.degrees(math.atan2(z_rel_to_knee, l_reach))

        # 7. Final Servo Mappings
        # Knee: We subtract alpha and beta from 90, then ADD the mount angle.
        # This accounts for the fact that at '90' the bone is already tilted down.
        final_knee = 90 - (alpha + beta - femur_mount_angle)

        # Ankle: The triangle internal angle.
        final_ankle = tibia_internal_deg

        return hip_deg, final_knee, final_ankle