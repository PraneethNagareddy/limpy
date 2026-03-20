import time
import math
from terminaltables import AsciiTable  # Optional, for clean UI
from driver import *
from inverse_kinematics import *

# --- START CALIBRATION VALUES ---
FEMUR = 60.0  # Try 58.0 or 62.0 if arcing
TIBIA = 104.0  # Try 102.0 or 106.0 if arcing
COXA = 43.0
Z_OFFSET = 10.0  # Your 10mm vertical step


# --------------------------------

def calculate_test_ik(x, y, z, f_len, t_len):
    # Use the same logic we perfected
    h_total = math.hypot(x, y)
    l_reach = h_total - COXA
    adj_z = z - Z_OFFSET
    d = math.hypot(l_reach, adj_z)

    # Law of Cosines
    cos_t = (f_len ** 2 + t_len ** 2 - d ** 2) / (2 * f_len * t_len)
    t_int = math.degrees(math.acos(max(-1, min(1, cos_t))))

    cos_f = (f_len ** 2 + d ** 2 - t_len ** 2) / (2 * f_len * d)
    alpha = math.degrees(math.acos(max(-1, min(1, cos_f))))
    beta = math.degrees(math.atan2(adj_z, l_reach))

    return 90 - (alpha + beta), t_int


print(f"--- Calibration Mode: {front_right_leg.config.position.name} ---")
print("Goal: The foot should stay at X=103, Y=0 throughout the move.")

try:
    while True:
        # Step from -60 to -140 and back
        for z_target in list(range(-60, -141, -2)) + list(range(-140, -59, 2)):
            # 1. Use your REAL move_to_position logic
            # This tests your rotation, your Z-offset, and your lengths
            front_right_leg.move_to_position(103, 0, z_target, with_ease=False)

            # 2. Print status for monitoring
            print(f"Target Z: {z_target:4}mm | Check X alignment...", end='\r')

            # Small delay to let the MG995 servos reach the position
            time.sleep(0.05)

except KeyboardInterrupt:
    print("\nCalibration stopped. Returning to home.")
    leg.move_to_position(103, 0, -104)