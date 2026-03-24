from core.spider import Spider
from kinematics.gait.gait import WalkingGait
from kinematics.gait.tripod_gait import TripodGait
import logging
import threading
import time

class PS4Controller:
    def __init__(self, spider: Spider = None, gait: WalkingGait = None):
        try:
            from pyPS4Controller.controller import Controller
        except ImportError:
            logging.error("pyPS4Controller is not installed. Run `pip install pyPS4Controller`")
            return

        self.spider = spider
        self.gait = gait if gait is not None else TripodGait(spider)

        class MyController(Controller):
            def __init__(self, gait, **kwargs):
                Controller.__init__(self, **kwargs)
                self.gait = gait
                self.x = 0.0
                self.y = 0.0
                self.rx = 0.0
                self.ry = 0.0
                self.running = True
                self.action_thread = threading.Thread(target=self.run_action)
                self.action_thread.start()

            def run_action(self):
                while self.running:
                    if abs(self.rx) > 0.1 or abs(self.ry) > 0.1:
                        self.gait.turn_omni(self.rx, self.ry, turn_factor=1.0)
                    elif self.x != 0.0 or self.y != 0.0:
                        self.gait.walk_omni(self.x, self.y, stride_factor=1.0)
                    else:
                        time.sleep(0.01)

            def on_L3_up(self, value):
                self.x = abs(value) / 32767.0

            def on_L3_down(self, value):
                self.x = -(abs(value) / 32767.0)

            def on_L3_left(self, value):
                self.y = -(abs(value) / 32767.0)

            def on_L3_right(self, value):
                self.y = abs(value) / 32767.0

            def on_L3_y_at_rest(self):
                self.x = 0.0

            def on_L3_x_at_rest(self):
                self.y = 0.0

            def on_R3_left(self, value):
                self.ry = -(abs(value) / 32767.0)

            def on_R3_right(self, value):
                self.ry = abs(value) / 32767.0

            def on_R3_up(self, value):
                self.rx = abs(value) / 32767.0

            def on_R3_down(self, value):
                self.rx = -(abs(value) / 32767.0)

            def on_R3_x_at_rest(self):
                self.ry = 0.0

            def on_R3_y_at_rest(self):
                self.rx = 0.0

            def on_disconnect(self):
                self.running = False

        self.controller = MyController(gait=self.gait, interface="/dev/input/js0", connecting_using_ds4drv=False)

    def start(self):
        if hasattr(self, 'controller'):
            logging.info("PS4 controller started.")
            self.controller.listen()