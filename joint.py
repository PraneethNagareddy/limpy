from config import KIT
from joint_config import JointConfig
from time import sleep
import logging

class Joint:
    def __init__(self, joint_config: JointConfig):
        if joint_config.channel == -1:
            raise Exception("Unable to instantiate joint: %s", joint_config.common_name)
        self.joint_config = joint_config

    def turn(self, to_angle:float, await_completion=False):
        logging.info("Turning joint: %s to %s", self.joint_config.common_name, to_angle)
        if (to_angle > self.joint_config.max_angle or
                to_angle < self.joint_config.min_angle):
            logging.error("Angle for joint: %s out of range", self.joint_config.common_name)
        angle_delta = abs(self.get_current_angle() - to_angle)
        KIT.servo[self.joint_config.channel].angle = to_angle
        if await_completion:
            sleep(self.__get_servo_sleep_time_seconds(angle_delta))

    def turn_smooth(self, to_angle, time_interval=0.002):
        logging.debug("Turning joint: %s smoothly to: %s with time interval: %s", self.joint_config.common_name, to_angle, time_interval)
        if (to_angle > self.joint_config.max_angle or
                to_angle < self.joint_config.min_angle):
            logging.error("Angle for joint: %s out of range", self.joint_config.common_name)
        init_angle = KIT.servo[self.joint_config.channel].angle
        current_angle = init_angle
        while abs(current_angle - to_angle) > 1:
            if to_angle > init_angle:
                current_angle += 1
            else:
                current_angle -= 1
            KIT.servo[self.joint_config.channel].angle = current_angle
            sleep(time_interval)
        KIT.servo[self.joint_config.channel].angle = to_angle
        sleep(time_interval * 2)

    def reverse_turn(self, turned_angle, await_completion=False):
        logging.debug("Reversing joint: %s", self.joint_config.common_name)
        to_angle = abs(self.get_current_angle() - turned_angle)
        if (to_angle > self.joint_config.max_angle or
                to_angle < self.joint_config.min_angle):
            logging.error("Angle for joint: %s out of range", self.joint_config.common_name)
        angle_delta = abs(self.get_current_angle() - to_angle)
        KIT.servo[self.joint_config.channel].angle = to_angle
        if await_completion:
            sleep(self.__get_servo_sleep_time_seconds(angle_delta))

    def stop(self, await_completion=False):
        logging.info("Stopping joint: %s", self.joint_config.common_name)

    def reset(self, await_completion=False):
        logging.info("Resetting joint: %s", self.joint_config.common_name)
        angle_delta = abs(self.get_current_angle() - self.joint_config.default_angle)
        KIT.servo[self.joint_config.channel].angle = self.joint_config.default_angle
        if await_completion:
            sleep(self.__get_servo_sleep_time_seconds(angle_delta))

    def get_current_angle(self) -> float:
        logging.info("Angle value of joint: %s is %f", self.joint_config.common_name, KIT.servo[self.joint_config.channel].angle)
        print("channel %s", self.joint_config.channel)
        print("current angle: %s", KIT.servo[self.joint_config.channel].angle)
        return KIT.servo[self.joint_config.channel].angle

    def __get_servo_sleep_time_seconds(joint, angle) -> float:
        return (joint.joint_config.turn_time_per_degree_millis * angle) / 1000