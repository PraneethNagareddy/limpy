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

    def __init_walk_stance(self):
        for leg in self.spider.legs:
            leg.move_to_position(-15, 60, 130, with_ease=True)
            logging.info("Leg %f initiated.", leg.config.position.name)

    def walk_forward(self, stride_distance_cm=5):
        # Code to move three legs off ground at once
        logging.info("Walking forward")
        start_time = time.time()
        #self.__init_walk_stance()
        while True:
            current_loop_time = time.time()
            t = (current_loop_time - start_time) * GAIT_SPEED

            # Phase 0 to 1 represents one full step cycle
            phase = t % 1.0

            for leg in self.spider.legs:

                # Assign leg to Group A or B
                # (Using a simple 1-6 ID mapping for this example)
                leg_id = leg.config.position.value
                is_group_a = leg_id in TRIPOD_GATE_A_GROUP  # FR, BR, ML
                is_right_side_leg = leg_id in RIGHT_LEGS_GROUP
                is_rear_leg = leg_id in REAR_LEGS_GROUP

                current_step_length = STEP_LENGTH
                if is_right_side_leg:
                    current_step_length = STEP_LENGTH * DRIFT_COMPENSATION_FACTOR


                # Offset the timing of Group B by half a cycle
                leg_phase = phase if is_group_a else (phase + 0.5) % 1.0

                # 1. SWING PHASE (Leg is in the air moving forward)
                if leg_phase < 0.5:
                    # Map 0.0-0.5 to a 0.0-1.0 sub-phase
                    s_phase = leg_phase * 2

                    # SMOOTH X: Uses Cosine to accelerate/decelerate
                    # Moves from -half to +half length
                    target_x = NEUTRAL_X-(math.cos(s_phase * math.pi) * (current_step_length / 2))

                    if is_rear_leg:
                        target_x = NEUTRAL_X+(math.cos(s_phase * math.pi) * (current_step_length / 2))

                    # Z LIFT: Parabolic/Sinusoidal
                    target_z = NEUTRAL_Z + (math.sin(s_phase * math.pi) * current_step_length)

                # 2. STANCE PHASE (Leg is on ground pushing body)
                else:
                    # Map 0.5-1.0 to a 0.0-1.0 sub-phase
                    s_phase = (leg_phase - 0.5) * 2

                    # Linear movement for keeping the body moving at constant speed
                    target_x = NEUTRAL_X + (current_step_length / 2) - (s_phase * current_step_length)
                    if is_rear_leg:
                        target_x = NEUTRAL_X - (current_step_length / 2) + (s_phase * current_step_length)

                    target_z = NEUTRAL_Z

                # Move the leg
                leg.move_to_position(target_x , NEUTRAL_Y, target_z)
            time.sleep(0.02)  # 50Hz update rate