from core.spider import Spider
from constants import *
from kinematics.gait.gait import WalkingGait

import time
import math
import logging

class TripodGait(WalkingGait):
    def __init__(self, spider: Spider = None):
        super().__init__(spider)
        self.gait_start_time = None

    def _get_phase(self):
        if self.gait_start_time is None:
            self.gait_start_time = time.time()
        current_loop_time = time.time()
        t = (current_loop_time - self.gait_start_time) * GAIT_SPEED
        return t % 1.0

    def walk_omni(self, x: float, y: float, stride_factor: float = 1.0):
        # x and y should be normalized between -1.0 and 1.0
        # stride_factor scales the overall movement

        # If no movement is requested, smoothly return to neutral stance
        if abs(x) < 0.1 and abs(y) < 0.1:
            self.return_to_neutral_stance()
            self.gait_start_time = None
            return

        magnitude = math.sqrt(x ** 2 + y ** 2)
        if magnitude > 1.0:
            x /= magnitude
            y /= magnitude

        phase = self._get_phase()

        for leg in self.spider.legs:
            leg_id = leg.config.position.value
            is_group_a = leg_id in TRIPOD_GATE_A_GROUP
            is_right_side_leg = leg_id in RIGHT_LEGS_GROUP
            is_rear_leg = leg_id in REAR_LEGS_GROUP

            # Calculate actual stride based on joystick input and drift compensation
            # Note: based on IK, X is forward/backward and Y is left/right.
            current_step_x = STEP_LENGTH * x * stride_factor
            current_step_y = STEP_LENGTH * y * stride_factor

            if is_right_side_leg:
                current_step_x *= DRIFT_COMPENSATION_FACTOR
                current_step_y *= DRIFT_COMPENSATION_FACTOR

            leg_phase = phase if is_group_a else (phase + 0.5) % 1.0

            if leg_phase < 0.5:
                s_phase = leg_phase * 2

                # Swing Phase: move smoothly from negative offset to positive offset
                offset_x = -(math.cos(s_phase * math.pi) * (current_step_x / 2))
                offset_y = -(math.cos(s_phase * math.pi) * (current_step_y / 2))

                if is_rear_leg:
                    # Inverting logic for rear legs as per original logic
                    offset_x = (math.cos(s_phase * math.pi) * (current_step_x / 2))
                    offset_y = (math.cos(s_phase * math.pi) * (current_step_y / 2))

                target_x = NEUTRAL_X + offset_x
                target_y = NEUTRAL_Y + offset_y
                target_z = NEUTRAL_Z + (math.sin(s_phase * math.pi) * STEP_HEIGHT)
            else:
                s_phase = (leg_phase - 0.5) * 2

                # Stance Phase: linearly push the body
                # Moves linearly from positive offset back to negative offset relative to body
                offset_x = (current_step_x / 2) - (s_phase * current_step_x)
                offset_y = (current_step_y / 2) - (s_phase * current_step_y)

                if is_rear_leg:
                    offset_x = -(current_step_x / 2) + (s_phase * current_step_x)
                    offset_y = -(current_step_y / 2) + (s_phase * current_step_y)

                target_x = NEUTRAL_X + offset_x
                target_y = NEUTRAL_Y + offset_y
                target_z = NEUTRAL_Z

            leg.move_to_position(target_x, target_y, target_z)

    def return_to_neutral_stance(self):
        logging.info("Returning to neutral stance.")
        (target_x, target_y, target_z) = INIT_COORDINATES
        for leg in self.spider.legs:
            leg.move_to_position(target_x, target_y, target_z, with_ease=False) # Use with_ease for smooth transition

    def turn_omni(self, rx: float, ry: float, turn_factor: float = 1.0):
        # Only turn if joystick is actively being pressed beyond a deadzone
        magnitude = math.sqrt(rx ** 2 + ry ** 2)
        if magnitude < 0.1:
            return

        # Continuous rotation based strictly on the horizontal axis of the right joystick (rx)
        # Positive rx -> turn right, Negative rx -> turn left
        # ry is technically the target angle if we map it to heading, but for a simple walking hexapod
        # turning continuously until the joystick is released is the standard mapping.

        # We map rx directly to rotation strength
        rotation_strength = rx * turn_factor

        TURN_ANGLE = 30  # Max degrees per step
        TURN_RADIUS = 100  # approximate radius for legs in mm (10cm)
        TURN_LENGTH = TURN_RADIUS * math.radians(TURN_ANGLE) * abs(rotation_strength)

        phase = self._get_phase()

        for leg in self.spider.legs:
            leg_id = leg.config.position.value
            is_group_a = leg_id in TRIPOD_GATE_A_GROUP
            is_right_side_leg = leg_id in RIGHT_LEGS_GROUP
            is_rear_leg = leg_id in REAR_LEGS_GROUP

            leg_phase = phase if is_group_a else (phase + 0.5) % 1.0

            # Left turn -> right side legs move forward, left side legs move backward
            # Right turn -> left side legs move forward, right side legs move backward
            is_turning_right = rotation_strength > 0

            if is_turning_right:
                move_forward = not is_right_side_leg
            else:
                move_forward = is_right_side_leg

            if leg_phase < 0.5:
                s_phase = leg_phase * 2

                if move_forward:
                    target_x = NEUTRAL_X - (math.cos(s_phase * math.pi) * (TURN_LENGTH / 2))
                else:
                    target_x = NEUTRAL_X + (math.cos(s_phase * math.pi) * (TURN_LENGTH / 2))

                target_z = NEUTRAL_Z + (math.sin(s_phase * math.pi) * STEP_HEIGHT)
            else:
                s_phase = (leg_phase - 0.5) * 2

                if move_forward:
                    target_x = NEUTRAL_X + (TURN_LENGTH / 2) - (s_phase * TURN_LENGTH)
                else:
                    target_x = NEUTRAL_X - (TURN_LENGTH / 2) + (s_phase * TURN_LENGTH)

                target_z = NEUTRAL_Z

            leg.move_to_position(target_x, NEUTRAL_Y, target_z)

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

        TURN_ANGLE = 30  # degrees
        TURN_RADIUS = 100  # approximate radius for legs in mm (10cm)
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

        TURN_ANGLE = 30  # degrees
        TURN_RADIUS = 100  # approximate radius for legs in mm (10cm)
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
            is_rear_leg = leg_id in REAR_LEGS_GROUP

            leg_phase = phase if is_group_a else (phase + 0.5) % 1.0

            if leg_phase < 0.5:
                s_phase = leg_phase * 2

                # Moving left: Leg swings to the left (negative Y)
                target_y = NEUTRAL_Y + (math.cos(s_phase * math.pi) * (STEP_LENGTH / 2))

                if is_rear_leg:
                    target_y = NEUTRAL_Y - (math.cos(s_phase * math.pi) * (STEP_LENGTH / 2))

                target_z = NEUTRAL_Z + (math.sin(s_phase * math.pi) * STEP_HEIGHT)
            else:
                s_phase = (leg_phase - 0.5) * 2

                # Stance: Leg pushes body to the left (leg moves to the right relative to body, positive Y)
                target_y = NEUTRAL_Y - (STEP_LENGTH / 2) + (s_phase * STEP_LENGTH)

                if is_rear_leg:
                    target_y = NEUTRAL_Y + (STEP_LENGTH / 2) - (s_phase * STEP_LENGTH)

                target_z = NEUTRAL_Z

            leg.move_to_position(NEUTRAL_X, target_y, target_z)

    def step_right(self):
        phase = self._get_phase()

        for leg in self.spider.legs:
            leg_id = leg.config.position.value
            is_group_a = leg_id in TRIPOD_GATE_A_GROUP
            is_rear_leg = leg_id in REAR_LEGS_GROUP

            leg_phase = phase if is_group_a else (phase + 0.5) % 1.0

            if leg_phase < 0.5:
                s_phase = leg_phase * 2

                # Moving right: Leg swings to the right (positive Y)
                target_y = NEUTRAL_Y - (math.cos(s_phase * math.pi) * (STEP_LENGTH / 2))

                if is_rear_leg:
                    target_y = NEUTRAL_Y + (math.cos(s_phase * math.pi) * (STEP_LENGTH / 2))

                target_z = NEUTRAL_Z + (math.sin(s_phase * math.pi) * STEP_HEIGHT)
            else:
                s_phase = (leg_phase - 0.5) * 2

                # Stance: Leg pushes body to the right (leg moves left relative to body, negative Y)
                target_y = NEUTRAL_Y + (STEP_LENGTH / 2) - (s_phase * STEP_LENGTH)

                if is_rear_leg:
                    target_y = NEUTRAL_Y - (STEP_LENGTH / 2) + (s_phase * STEP_LENGTH)

                target_z = NEUTRAL_Z

            leg.move_to_position(NEUTRAL_X, target_y, target_z)