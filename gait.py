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
                leg_id = leg.config.position.value
                is_group_a = leg_id in TRIPOD_GATE_A_GROUP

                # Offset the timing of Group B by half a cycle
                leg_phase = phase if is_group_a else (phase + 0.5) % 1.0

                if leg_id is not Legs.FRONT_RIGHT:
                    continue

                # 1. SWING PHASE (Leg in air moving forward)
                if leg_phase < 0.5:
                    s_phase = leg_phase * 2  # 0.0 to 1.0

                    # SMOOTH X: Uses Cosine to accelerate/decelerate
                    # Moves from -half to +half length
                    target_x = -math.cos(s_phase * math.pi) * (STEP_LENGTH / 2)

                    # Z LIFT: Parabolic/Sinusoidal
                    target_z = NEUTRAL_Z - (math.sin(s_phase * math.pi) * STEP_HEIGHT)

                # 2. STANCE PHASE (Leg on ground pushing body)
                else:
                    s_phase = (leg_phase - 0.5) * 2  # 0.0 to 1.0

                    # SMOOTH X: Reverse Cosine to push the body forward
                    target_x = math.cos(s_phase * math.pi) * (STEP_LENGTH / 2)

                    target_z = NEUTRAL_Z

                # Move the leg
                leg.move_to_position(target_x, NEUTRAL_Y, target_z)


            time.sleep(0.02)  # 50Hz update rate