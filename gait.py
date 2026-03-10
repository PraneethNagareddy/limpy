from spider import Spider
from config import *
from inverse_kinematics import IK
from enums import Legs

import time
import math
import logging

class WalkingGait:
    def __init__(self, spider: Spider):
        self.spider = spider

    def walk_forward(self, stride_distance_cm=3):
        pass

    def walk_backward(self, stride_distance_cm=3):
        pass

    def turn_left(self):
        pass

    def turn_right(self):
        pass


class TripodGait(WalkingGait):
    def __init__(self, spider: Spider):
        super().__init__(spider)

    def walk_forward(self, stride_distance_cm=5):
        # Code to move three legs off ground at once
        logging.info("Walking forward")
        tripod_a = [1, 3, 4]
        start_time = time.time()

        while True:
            t = (time.time() - start_time) * GAIT_SPEED

            # Phase 0 to 1 represents one full step cycle
            phase = t % 1.0

            for leg in self.spider.legs:

                # Assign leg to Group A or B
                # (Using a simple 0-5 ID mapping for this example)
                leg_id = leg.config.position.value
                is_group_a = leg_id in TRIPOD_GATE_A_GROUP  # FR, BR, ML

                if not is_group_a:
                    continue

                # Offset the timing of Group B by half a cycle
                leg_phase = phase if is_group_a else (phase + 0.5) % 1.0

                # 1. SWING PHASE (Leg is in the air moving forward)
                if leg_phase < 0.5:
                    # Map 0.0-0.5 to a 0.0-1.0 sub-phase
                    s_phase = leg_phase * 2

                    # Move X from -STEP_LENGTH/2 to +STEP_LENGTH/2
                    target_x = (s_phase - 0.5) * STEP_LENGTH
                    # Parabolic lift: Z peaks in the middle of the swing
                    target_z = NEUTRAL_Z - (math.sin(s_phase * math.pi) * STEP_HEIGHT)

                # 2. STANCE PHASE (Leg is on ground pushing body)
                else:
                    # Map 0.5-1.0 to a 0.0-1.0 sub-phase
                    s_phase = (leg_phase - 0.5) * 2

                    # Move X from +STEP_LENGTH/2 back to -STEP_LENGTH/2 (Pushing Body)
                    target_x = (0.5 - s_phase) * STEP_LENGTH
                    target_z = NEUTRAL_Z  # Stay flat on the floor

                leg.move_to_position(target_x, NEUTRAL_Y, target_z)
            time.sleep(0.002)  # 50Hz update rate