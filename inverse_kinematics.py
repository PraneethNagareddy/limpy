import logging
import math
from typing import Tuple
from config import FEMUR_LENGTH_MM, TIBIA_LENGTH_MM, COXA_LENGTH_MM, COXA_Z_OFFSET_MM, FEMUR_Z_OFFSET_MM


class IK:
    @staticmethod
    def solve(x, y, z) -> Tuple[float, float, float]:
        # 1. Hip Angle: Simple rotation around the vertical axis
        hip_angle_rad = math.atan2(y, x)
        hip_deg = math.degrees(hip_angle_rad)

        # 2. Horizontal Reach (L): Distance from Coxa pivot to foot,
        # MINUS the coxa's own length.
        # This leaves us with the reach the Femur and Tibia must cover.
        h_total = math.hypot(x, y)
        l_reach = h_total - COXA_LENGTH_MM

        # 3. THE CRITICAL FIX: Account for the 10mm vertical step
        # We subtract 10mm from Z because the Femur pivot is 10mm HIGHER
        # than the Hip pivot.
        total_z_offset = COXA_Z_OFFSET_MM + FEMUR_Z_OFFSET_MM
        adjusted_z = z - COXA_Z_OFFSET_MM

        # 3. 3D "Leg Plane" Distance (D):
        # The hypotenuse from the Femur-joint to the Foot.
        d = math.hypot(l_reach, adjusted_z)

        # Safety Check: Don't exceed physical limit
        max_reach = FEMUR_LENGTH_MM + TIBIA_LENGTH_MM
        d = min(d, max_reach)

        # 4. Law of Cosines for Tibia (Ankle)
        # Returns the internal angle between Femur and Tibia.
        # 180 = straight, 90 = L-shape.
        cos_tibia = (FEMUR_LENGTH_MM ** 2 + TIBIA_LENGTH_MM ** 2 - d ** 2) / (2 * FEMUR_LENGTH_MM * TIBIA_LENGTH_MM)
        tibia_internal_deg = math.degrees(math.acos(max(-1, min(1, cos_tibia))))

        # 5. Law of Cosines for Femur (Knee)
        # alpha: angle between Femur and the line 'd'
        cos_femur = (FEMUR_LENGTH_MM ** 2 + d ** 2 - TIBIA_LENGTH_MM ** 2) / (2 * FEMUR_LENGTH_MM * d)
        alpha = math.degrees(math.acos(max(-1, min(1, cos_femur))))

        # beta: angle of the line 'd' relative to the horizontal plane
        # If z is negative (foot below hip), beta will be negative.
        beta = math.degrees(math.atan2(adjusted_z, l_reach))

        # 6. Apply your physical offsets (90/90/90 = L-shape)
        # Knee: If alpha + beta = 0, femur is horizontal (90 deg servo)
        # We subtract the angle from 90 to tilt the femur down for negative Z.
        final_knee = 90 - (alpha + beta)

        # Ankle: The internal angle is 90 for L-shape, 180 for straight.
        # Your servo is 90 for L-shape, 180 for straight. Direct map!
        final_ankle = tibia_internal_deg

        return hip_deg, final_knee, final_ankle
