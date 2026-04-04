import time

from core.leg import Leg
from constants import INIT_COORDINATES;
import logging

class Spider:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Spider, cls).__new__(cls)
            cls._instance._is_initialized = False
        return cls._instance

    def __init__(self, front_right_leg:Leg=None,
                 front_left_leg:Leg=None,
                 rear_right_leg:Leg=None,
                 rear_left_leg:Leg=None,
                 middle_left_leg:Leg=None,
                 middle_right_leg:Leg=None):
        self.controller_manager = None
        if getattr(self, '_is_initialized', False):
            return
            
        self.front_right_leg = front_right_leg
        self.front_left_leg = front_left_leg
        self.rear_right_leg = rear_right_leg
        self.rear_left_leg = rear_left_leg
        self.middle_left_leg = middle_left_leg
        self.middle_right_leg = middle_right_leg
        
        # Only populate legs if they were provided (to support get_instance without args)
        if all([front_right_leg, front_left_leg, rear_right_leg, rear_left_leg, middle_left_leg, middle_right_leg]):
            self.legs = (self.front_right_leg, self.middle_right_leg, self.rear_right_leg, self.rear_left_leg, self.middle_left_leg, self.front_left_leg)
            self.__right_legs = (self.front_right_leg, self.rear_right_leg)
            self.__left_legs = (self.front_left_leg, self.rear_left_leg)
            self._is_initialized = True

    @classmethod
    def get(cls):
        """Returns the singleton instance. Raises an error if not yet initialized with legs."""
        if cls._instance is None or not getattr(cls._instance, '_is_initialized', False):
            raise Exception("Spider singleton has not been initialized with legs yet!")
        return cls._instance

    def startup(self):
        logging.info("Starting up spider smoothly...")
        (target_x, target_y, target_z) = INIT_COORDINATES

        # We start from a safe retracted position and rise up to the standing height
        # Assuming current height is near 0 or -10
        start_z = -10
        steps = 30

        for i in range(steps + 1):
            current_z = start_z + (target_z - start_z) * (i / steps)
            for leg in self.legs:
                leg.move_to_position(target_x, target_y, current_z)
            time.sleep(0.01)

        time.sleep(0.5)
        logging.info("Spider started and standing!")
        logging.info("Starting controllers")
        from controller.controller_manager import ControllerManager
        self.controller_manager = ControllerManager(spider=self)
        self.controller_manager.start()


    def shutdown(self):
        #for __leg in self.__legs:
        #    __leg.terminate()
        logging.info("Spider shutdown!")

    def hibernate(self):

        logging.info("Spider in hibernate!")
