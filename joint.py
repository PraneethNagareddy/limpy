import math

from servo_kit_factory import ServoKitFactory
from joint_config import JointConfig
from time import sleep
import logging

class Joint:
    def __init__(self, joint_config: JointConfig):
        if joint_config.channel == -1:
            raise Exception("Unable to instantiate joint: %s", joint_config.common_name)
        self.joint_config = joint_config
        self.KIT = ServoKitFactory.get_servo_kit(joint_config.i2c_address)
        self.KIT.servo[self.joint_config.channel].set_pulse_width_range(self.joint_config.pulse_width_min, self.joint_config.pulse_width_max)

    def turn(self, to_angle:float, await_completion=False, wait_time=None):
        logging.info("Turning joint: %s to %s", self.joint_config.common_name, to_angle)
        if (to_angle > self.joint_config.max_angle or
                to_angle < self.joint_config.min_angle):
            logging.error("Angle for joint: %s out of range", self.joint_config.common_name)
        self.KIT.servo[self.joint_config.channel].angle = to_angle
        if await_completion:
            if wait_time is None:
                angle_delta = abs(self.get_current_angle() - to_angle)
                sleep(self.__get_servo_sleep_time_seconds(angle_delta))
            else:
                sleep(wait_time)

    def turn_smooth(self, to_angle, time_interval=0.002):
        logging.debug("Turning joint: %s smoothly to: %s with time interval: %s", self.joint_config.common_name, to_angle, time_interval)
        if (to_angle > self.joint_config.max_angle or
                to_angle < self.joint_config.min_angle):
            logging.error("Angle for joint: %s out of range", self.joint_config.common_name)
        init_angle = self.KIT.servo[self.joint_config.channel].angle
        current_angle = init_angle
        while abs(current_angle - to_angle) > 1:
            if to_angle > init_angle:
                current_angle += 1
            else:
                current_angle -= 1
            self.KIT.servo[self.joint_config.channel].angle = current_angle
            sleep(time_interval)
        self.KIT.servo[self.joint_config.channel].angle = to_angle
        sleep(time_interval * 2)

    def reverse_turn(self, turned_angle, await_completion=False, wait_time=None):
        logging.debug("Reversing joint: %s", self.joint_config.common_name)
        to_angle = abs(self.get_current_angle() - turned_angle)
        if (to_angle > self.joint_config.max_angle or
                to_angle < self.joint_config.min_angle):
            logging.error("Angle for joint: %s out of range", self.joint_config.common_name)
        angle_delta = abs(self.get_current_angle() - to_angle)
        self.KIT.servo[self.joint_config.channel].angle = to_angle
        if await_completion:
            if wait_time is None:
                sleep(self.__get_servo_sleep_time_seconds(angle_delta))
            else:
                sleep(wait_time)

    def stop(self):
        logging.info("Stopping joint: %s", self.joint_config.common_name)

    def reset(self, await_completion=False, wait_time=None):
        logging.info("Resetting joint: %s", self.joint_config.common_name)
        current_angle = 180 if self.get_current_angle() is None else self.get_current_angle()
        angle_delta = abs(current_angle - self.joint_config.default_angle)
        self.KIT.servo[self.joint_config.channel].angle = self.joint_config.default_angle
        if await_completion:
            if wait_time is None:
                sleep(self.__get_servo_sleep_time_seconds(angle_delta))
            else:
                sleep(wait_time)

    def get_current_angle(self) -> float:
        #logging.info("Angle value of joint: %s is %f", self.joint_config.common_name, self.KIT.servo[self.joint_config.channel].angle)
        return self.KIT.servo[self.joint_config.channel].angle

    def validate_and_reset(self):
        current_angle = self.get_current_angle()
        if current_angle is None or math.isnan(current_angle):
            logging.info("Servo angle is NaN. Resetting the servo")
            self.reset()

    def __get_servo_sleep_time_seconds(joint, angle) -> float:
        return (joint.joint_config.turn_time_per_degree_millis * angle) / 1000