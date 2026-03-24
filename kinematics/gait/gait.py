import logging

from core.spider import Spider
import sys


class WalkingGait:
    def __init__(self, spider: Spider = None):
        if spider is None:
            logging.error("Cant initialize gait with null spider")
            sys.exit(0)
        self.spider = spider

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

    def walk_omni(self, x: float, y: float, stride_factor: float = 1.0):
        pass

    def turn_omni(self, rx: float, ry: float, turn_factor: float = 1.0):
        pass