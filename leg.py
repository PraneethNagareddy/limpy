from config import *
from joint_utils import move_joint_with_sine_easing as turn_joints_ease
from enums import Legs
from joint import Joint
from inverse_kinematics import IK
import logging

class Leg:
    def __init__(self, hip_joint: Joint, knee_joint:Joint, ankle_joint:Joint, position:Legs):
        self.hip_joint = hip_joint
        self.knee_joint = knee_joint
        self.ankle_joint = ankle_joint
        self.position = position


    def terminate(self):
        self.ankle_joint.turn_smooth(90)
        self.knee_joint.turn_smooth(180)
        self.hip_joint.turn_smooth(180)


    def rest(self):
        #TODO
        pass

    def move_to_position(self, x_target, y_target, z_target):
        (hip_angle, knee_angle, ankle_angle) = IK.solve(x_target, y_target, z_target)
        self.hip_joint.validate_and_reset()
        self.knee_joint.validate_and_reset()
        self.ankle_joint.validate_and_reset()
        turn_joints_ease([(self.hip_joint, self.hip_joint.get_current_angle(), hip_angle), (self.hip_joint, self.hip_joint.get_current_angle(), hip_angle), (self.hip_joint, self.hip_joint.get_current_angle(), hip_angle)], duration_sec=0.5)

    def move_to_stable_position(self):
        self.hip_joint.turn(to_angle=HIP_JOINT_STEP_ANGLE_FRONT, await_completion=False)

    def move_one_step_front(self):
        self.knee_joint.turn(to_angle=KNEE_JOINT_STEP_ANGLE_FRONT, await_completion=True)
        self.hip_joint.turn(to_angle=HIP_JOINT_STEP_ANGLE_FRONT, await_completion=True)
        self.knee_joint.reverse_turn(turned_angle=KNEE_JOINT_STEP_ANGLE_FRONT, await_completion=True)

    def move_one_step_back(self):
        self.knee_joint.turn(KNEE_JOINT_STEP_ANGLE_BACK, await_completion=True)
        self.hip_joint.turn(HIP_JOINT_STEP_ANGLE_BACK, await_completion=True)
        self.knee_joint.turn(KNEE_JOINT_STEP_ANGLE_FRONT, await_completion=True)

    def move_one_step_outward(self):
        self.knee_joint.turn(KNEE_JOINT_STEP_ANGLE_OUTWARD, await_completion=True)
        self.ankle_joint.turn(ANKLE_JOINT_STEP_ANGLE_OUTWARD, await_completion=True)
        self.knee_joint.turn(KNEE_JOINT_STEP_ANGLE_OUTWARD, await_completion=True)

    def move_one_step_inward(self):
        self.knee_joint.turn(KNEE_JOINT_STEP_ANGLE_INWARD, await_completion=True)
        self.ankle_joint.turn(ANKLE_JOINT_STEP_ANGLE_INWARD, await_completion=True)
        self.knee_joint.turn(KNEE_JOINT_STEP_ANGLE_INWARD, await_completion=True)

    def lean_down(self, lean_factor):
        #TODO
        pass

    def lean_up(self, lean_factor):
        #TODO
        pass

    def startup(self):
        match self.position:
            case Legs.FRONT_LEFT:
                self.ankle_joint.turn_smooth(0)
                self.knee_joint.turn_smooth(90)
                self.hip_joint.turn_smooth(50)
                self.ankle_joint.turn_smooth(135)
                self.knee_joint.turn_smooth(120)
                logging.info("Front left leg initiated")
            case Legs.FRONT_RIGHT:
                self.ankle_joint.turn_smooth(0)
                self.knee_joint.turn_smooth(90)
                self.hip_joint.turn_smooth(100)
                self.ankle_joint.turn_smooth(0)
                self.knee_joint.turn_smooth(120)
                logging.info("Front right leg initiated")
            case Legs.REAR_LEFT:
                self.ankle_joint.turn_smooth(0)
                self.knee_joint.turn_smooth(90)
                self.hip_joint.turn_smooth(150)
                self.ankle_joint.turn_smooth(75)
                self.knee_joint.turn_smooth(150)
                logging.info("Rear left leg initiated")
            case Legs.REAR_RIGHT:
                self.ankle_joint.turn_smooth(0)
                self.knee_joint.turn_smooth(90)
                self.hip_joint.turn_smooth(90)
                self.ankle_joint.turn_smooth(135)
                self.knee_joint.turn_smooth(120)
                logging.info("Rear right leg initiated")


    def init_ankle(self):
        target_angle = 0
        match self.position:
            case Legs.FRONT_LEFT:
                target_angle = 0
            case Legs.FRONT_RIGHT:
                target_angle = 0
            case Legs.REAR_LEFT:
                target_angle = 0
            case Legs.REAR_RIGHT:
                target_angle = 0
        logging.debug("Turning ankle to: %s", target_angle)
        self.ankle_joint.turn(target_angle)

    def init_knee(self):
        target_angle = 90
        match self.position:
            case Legs.FRONT_LEFT:
                target_angle = 90
            case Legs.FRONT_RIGHT:
                target_angle = 90
            case Legs.REAR_LEFT:
                target_angle = 90
            case Legs.REAR_RIGHT:
                target_angle = 90
        logging.debug("Turning knee to: %s", target_angle)
        self.knee_joint.turn(target_angle)

    def init_hip(self):
        target_angle = 90
        match self.position:
            case Legs.FRONT_LEFT:
                target_angle = 50
            case Legs.FRONT_RIGHT:
                target_angle = 100
            case Legs.REAR_LEFT:
                target_angle = 150
            case Legs.REAR_RIGHT:
                target_angle = 90
        logging.debug("Turning hip to: %s", target_angle)
        self.hip_joint.turn(target_angle)

    def init_support_weight(self):
        target_ankle_angle = 0
        target_knee_angle = 0
        match self.position:
            case Legs.FRONT_LEFT:
                target_ankle_angle = 135
                target_knee_angle = 120
            case Legs.FRONT_RIGHT:
                target_ankle_angle = 0
                target_knee_angle = 120
            case Legs.REAR_LEFT:
                target_ankle_angle = 75
                target_knee_angle = 120
            case Legs.REAR_RIGHT:
                target_ankle_angle = 135
                target_knee_angle = 120
        logging.debug("Turning ankle to: %s", target_ankle_angle)
        self.ankle_joint.turn(target_ankle_angle)
        logging.debug("Turning knee to: %s", target_knee_angle)
        self.knee_joint.turn(target_knee_angle)