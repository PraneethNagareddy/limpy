import time

from leg import Leg
import logging
import threading

class Spider:
    def __init__(self, front_right_leg:Leg,
                 front_left_leg:Leg,
                 rear_right_leg:Leg,
                 rear_left_leg:Leg):
        self.front_right_leg = front_right_leg
        self.front_left_leg = front_left_leg
        self.rear_right_leg = rear_right_leg
        self.rear_left_leg = rear_left_leg
        self.__legs = (self.front_right_leg, self.rear_right_leg, self.rear_left_leg, self.front_left_leg)
        self.__right_legs = (self.front_right_leg, self.rear_right_leg)
        self.__left_legs = (self.front_left_leg, self.rear_left_leg)

    def startup(self):
        front_left_thread = threading.Thread(target=self.front_left_leg.startup())
        front_right_thread = threading.Thread(target=self.front_right_leg.startup())
        rear_left_thread = threading.Thread(target=self.rear_left_leg.startup())
        rear_right_thread = threading.Thread(target=self.rear_right_leg.startup())

        front_left_thread.start()
        front_right_thread.start()
        rear_left_thread.start()
        rear_right_thread.start()

        front_left_thread.join()
        front_right_thread.join()
        rear_left_thread.join()
        rear_right_thread.join()
        logging.info("Spider initiated!")

    def startup_old(self):
        #init ankles
        for __leg in self.__legs:
            __leg.init_ankle()
        time.sleep(1)
        logging.info("ankles up!")

        # init knee
        for __leg in self.__legs:
            __leg.init_knee()
        time.sleep(1)
        logging.info("Knees on ground level!")

        for __leg in self.__legs:
            __leg.init_hip()
        time.sleep(1)
        logging.info("Hips to position!")

        for __leg in self.__legs:
            __leg.init_support_weight()
        time.sleep(1)
        logging.info("Legs supporting weight!")
        logging.info("Spider initiated!")

    def shutdown(self):
        for __leg in self.__legs:
            __leg.terminate()
        logging.info("Spider shutdown!")

    def hibernate(self):
        for __leg in self.__legs:
            __leg.rest()
        logging.info("Spider in hibernate!")

    def walk_forward(self, steps):
        steps_expected = steps
        while steps > 0:
            for __leg in self.__legs:
                __leg.move_one_step_front()

            for __leg in self.__legs:
                __leg.move_to_stable_position()

            steps -= 1
        logging.debug("Moved %d steps forward", (steps_expected-steps))


    def walk_backwards(self, steps):
        steps_expected = steps
        while steps > 0:
            for __leg in self.__legs:
                __leg.move_one_step_back()
            steps -= 1
        logging.debug("Moved %d steps backward", (steps_expected - steps))

    def turn_left(self, steps):
        steps_expected = steps
        while steps > 0:
            for __left_leg in self.__left_legs:
                __left_leg.move_one_step_back()
            for __right_leg in self.__right_legs:
                __right_leg.move_one_step_front()
            steps -= 1
        logging.debug("Moved %d steps left", (steps_expected - steps))

    def turn_right(self, steps):
        steps_expected = steps
        while steps > 0:
            for __right_leg in self.__right_legs:
                __right_leg.move_one_step_back()
            for __left_leg in self.__left_legs:
                __left_leg.move_one_step_front()
            steps -= 1
        logging.debug("Moved %d steps right", (steps_expected - steps))

    def slide_left(self, steps):
        steps_expected = steps
        while steps > 0:
            for __left_leg in self.__left_legs:
                __left_leg.move_one_step_outward()
            for __right_leg in self.__right_legs:
                __right_leg.move_one_step_front()
            steps -= 1
        logging.debug("Moved %d steps left", (steps_expected - steps))

    def slide_right(self, steps):
        #TODO
        pass

    def lean_forward(self, lean_angle):
        #TODO
        pass

    def lean_backwards(self, lean_angle):
        #TODO
        pass

    def lean_right(self, lean_angle):
        #TODO
        pass

    def lean_left(self, lean_angle):
        #TODO
        pass
