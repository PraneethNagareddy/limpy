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
        self.start_time = time.time()

    def walk_forward(self, stride_distance_cm=3):
        pass

    def walk_backward(self, stride_distance_cm=3):
        pass

    def turn_left(self):
        pass

    def turn_right(self):
        pass

    def step_left(self):
        pass

    def step_right(self):
        pass


class TripodGait(WalkingGait):
    def __init__(self, spider: Spider):
        super().__init__(spider)
        self.gait_start_time = None

    def _get_phase(self):
        if self.gait_start_time is None:
            self.gait_start_time = time.time()
        current_loop_time = time.time()
        t = (current_loop_time - self.gait_start_time) * GAIT_SPEED
        return t % 1.0

    def walk_forward(self, stride_distance_cm=5):
        # Code to move three legs off ground at once
        phase = self._get_phase()

        for leg in self.spider.legs:
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
                target_x = NEUTRAL_X - (math.cos(s_phase * math.pi) * (current_step_length / 2))

                if is_rear_leg:
                    target_x = NEUTRAL_X + (math.cos(s_phase * math.pi) * (current_step_length / 2))

                # Z LIFT: Parabolic/Sinusoidal
                target_z = NEUTRAL_Z + (math.sin(s_phase * math.pi) * STEP_HEIGHT)

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
            leg.move_to_position(target_x, NEUTRAL_Y, target_z)

    def walk_backward(self, stride_distance_cm=5):
        phase = self._get_phase()

        for leg in self.spider.legs:
            leg_id = leg.config.position.value
            is_group_a = leg_id in TRIPOD_GATE_A_GROUP  # FR, BR, ML
            is_right_side_leg = leg_id in RIGHT_LEGS_GROUP
            is_rear_leg = leg_id in REAR_LEGS_GROUP

            current_step_length = STEP_LENGTH
            if is_right_side_leg:
                current_step_length = STEP_LENGTH * DRIFT_COMPENSATION_FACTOR

            leg_phase = phase if is_group_a else (phase + 0.5) % 1.0

            # 1. SWING PHASE (Leg is in the air moving backward)
            if leg_phase < 0.5:
                s_phase = leg_phase * 2
                
                target_x = NEUTRAL_X + (math.cos(s_phase * math.pi) * (current_step_length / 2))

                if is_rear_leg:
                    target_x = NEUTRAL_X - (math.cos(s_phase * math.pi) * (current_step_length / 2))

                target_z = NEUTRAL_Z + (math.sin(s_phase * math.pi) * STEP_HEIGHT)

            # 2. STANCE PHASE (Leg is on ground pushing body forward)
            else:
                s_phase = (leg_phase - 0.5) * 2
                
                target_x = NEUTRAL_X - (current_step_length / 2) + (s_phase * current_step_length)
                if is_rear_leg:
                    target_x = NEUTRAL_X + (current_step_length / 2) - (s_phase * current_step_length)

                target_z = NEUTRAL_Z

            leg.move_to_position(target_x, NEUTRAL_Y, target_z)

    def turn_left(self):
        logging.info(f"Turning left")
        phase = self._get_phase()
        
        TURN_ANGLE = 90  # degrees
        TURN_RADIUS = 100 # approximate radius for legs in mm (10cm)
        TURN_LENGTH = TURN_RADIUS * math.radians(TURN_ANGLE)
        
        for leg in self.spider.legs:
            leg_id = leg.config.position.value
            is_group_a = leg_id in TRIPOD_GATE_A_GROUP
            is_right_side_leg = leg_id in RIGHT_LEGS_GROUP
            is_rear_leg = leg_id in REAR_LEGS_GROUP
            
            leg_phase = phase if is_group_a else (phase + 0.5) % 1.0
            
            # Left turn -> right side legs move forward, left side legs move backward
            move_forward = is_right_side_leg
            
            if leg_phase < 0.5:
                s_phase = leg_phase * 2
                
                if move_forward:
                    # Moving forward: X from -half to +half
                    target_x = NEUTRAL_X - (math.cos(s_phase * math.pi) * (TURN_LENGTH / 2))
                    if is_rear_leg: target_x = NEUTRAL_X + (math.cos(s_phase * math.pi) * (TURN_LENGTH / 2))
                else:
                    # Moving backward: X from +half to -half
                    target_x = NEUTRAL_X + (math.cos(s_phase * math.pi) * (TURN_LENGTH / 2))
                    if is_rear_leg: target_x = NEUTRAL_X - (math.cos(s_phase * math.pi) * (TURN_LENGTH / 2))
                    
                target_z = NEUTRAL_Z + (math.sin(s_phase * math.pi) * STEP_HEIGHT)
            else:
                s_phase = (leg_phase - 0.5) * 2
                
                if move_forward:
                    # Stance pushing body backward relative to leg (leg moves backward)
                    target_x = NEUTRAL_X + (TURN_LENGTH / 2) - (s_phase * TURN_LENGTH)
                    if is_rear_leg: target_x = NEUTRAL_X - (TURN_LENGTH / 2) + (s_phase * TURN_LENGTH)
                else:
                    target_x = NEUTRAL_X - (TURN_LENGTH / 2) + (s_phase * TURN_LENGTH)
                    if is_rear_leg: target_x = NEUTRAL_X + (TURN_LENGTH / 2) - (s_phase * TURN_LENGTH)
                    
                target_z = NEUTRAL_Z

            leg.move_to_position(target_x, NEUTRAL_Y, target_z)

    def turn_right(self):
        logging.info(f"Turning right")
        phase = self._get_phase()
        
        TURN_ANGLE = 90  # degrees
        TURN_RADIUS = 100 # approximate radius for legs in mm (10cm)
        TURN_LENGTH = TURN_RADIUS * math.radians(TURN_ANGLE)
        
        for leg in self.spider.legs:
            leg_id = leg.config.position.value
            is_group_a = leg_id in TRIPOD_GATE_A_GROUP
            is_right_side_leg = leg_id in RIGHT_LEGS_GROUP
            is_rear_leg = leg_id in REAR_LEGS_GROUP
            
            leg_phase = phase if is_group_a else (phase + 0.5) % 1.0
            
            # Right turn -> left side legs move forward, right side legs move backward
            move_forward = not is_right_side_leg
            
            if leg_phase < 0.5:
                s_phase = leg_phase * 2
                
                if move_forward:
                    target_x = NEUTRAL_X - (math.cos(s_phase * math.pi) * (TURN_LENGTH / 2))
                    if is_rear_leg: target_x = NEUTRAL_X + (math.cos(s_phase * math.pi) * (TURN_LENGTH / 2))
                else:
                    target_x = NEUTRAL_X + (math.cos(s_phase * math.pi) * (TURN_LENGTH / 2))
                    if is_rear_leg: target_x = NEUTRAL_X - (math.cos(s_phase * math.pi) * (TURN_LENGTH / 2))
                    
                target_z = NEUTRAL_Z + (math.sin(s_phase * math.pi) * STEP_HEIGHT)
            else:
                s_phase = (leg_phase - 0.5) * 2
                
                if move_forward:
                    target_x = NEUTRAL_X + (TURN_LENGTH / 2) - (s_phase * TURN_LENGTH)
                    if is_rear_leg: target_x = NEUTRAL_X - (TURN_LENGTH / 2) + (s_phase * TURN_LENGTH)
                else:
                    target_x = NEUTRAL_X - (TURN_LENGTH / 2) + (s_phase * TURN_LENGTH)
                    if is_rear_leg: target_x = NEUTRAL_X + (TURN_LENGTH / 2) - (s_phase * TURN_LENGTH)
                    
                target_z = NEUTRAL_Z

            leg.move_to_position(target_x, NEUTRAL_Y, target_z)


    def step_left(self):
        phase = self._get_phase()

        for leg in self.spider.legs:
            leg_id = leg.config.position.value
            is_group_a = leg_id in TRIPOD_GATE_A_GROUP

            leg_phase = phase if is_group_a else (phase + 0.5) % 1.0

            if leg_phase < 0.5:
                s_phase = leg_phase * 2
                
                # Moving left: Leg swings to the left (negative Y)
                target_y = NEUTRAL_Y + (math.cos(s_phase * math.pi) * (STEP_LENGTH / 2))
                target_z = NEUTRAL_Z + (math.sin(s_phase * math.pi) * STEP_HEIGHT)
            else:
                s_phase = (leg_phase - 0.5) * 2
                
                # Stance: Leg pushes body to the left (leg moves to the right relative to body, positive Y)
                target_y = NEUTRAL_Y - (STEP_LENGTH / 2) + (s_phase * STEP_LENGTH)
                target_z = NEUTRAL_Z

            leg.move_to_position(NEUTRAL_X, target_y, target_z)

    def step_right(self):
        phase = self._get_phase()

        for leg in self.spider.legs:
            leg_id = leg.config.position.value
            is_group_a = leg_id in TRIPOD_GATE_A_GROUP

            leg_phase = phase if is_group_a else (phase + 0.5) % 1.0

            if leg_phase < 0.5:
                s_phase = leg_phase * 2
                
                # Moving right: Leg swings to the right (positive Y)
                target_y = NEUTRAL_Y - (math.cos(s_phase * math.pi) * (STEP_LENGTH / 2))
                target_z = NEUTRAL_Z + (math.sin(s_phase * math.pi) * STEP_HEIGHT)
            else:
                s_phase = (leg_phase - 0.5) * 2
                
                # Stance: Leg pushes body to the right (leg moves left relative to body, negative Y)
                target_y = NEUTRAL_Y + (STEP_LENGTH / 2) - (s_phase * STEP_LENGTH)
                target_z = NEUTRAL_Z

            leg.move_to_position(NEUTRAL_X, target_y, target_z)
