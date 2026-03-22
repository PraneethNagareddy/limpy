import keyboard
from spider import Spider
from gait import TripodGait
import logging
import threading
import time

class KeyboardController:
    def __init__(self, spider: Spider):
        self.spider = spider
        self.gait = TripodGait(spider)
        self.running = False
        
    def start(self):
        self.running = True
        logging.info("Keyboard controller started. Use arrow keys to move. (Press 'esc' to stop)")
        
        while self.running:
            try:
                if keyboard.is_pressed('ctrl+left'):
                    self.gait.turn_left()
                    # Wait for key release
                    while keyboard.is_pressed('ctrl+left'):
                        time.sleep(0.01)
                elif keyboard.is_pressed('ctrl+right'):
                    self.gait.turn_right()
                    # Wait for key release
                    while keyboard.is_pressed('ctrl+right'):
                        time.sleep(0.01)
                elif keyboard.is_pressed('up'):
                    self.gait.walk_forward()
                elif keyboard.is_pressed('down'):
                    self.gait.walk_backward()
                elif keyboard.is_pressed('left'):
                    self.gait.step_left()
                elif keyboard.is_pressed('right'):
                    self.gait.step_right()
                elif keyboard.is_pressed('esc'):
                    self.stop()
                else:
                    time.sleep(0.01)
            except Exception as e:
                logging.error(f"Error in keyboard controller: {e}")
                self.running = False

    def stop(self):
        self.running = False


class PS4Controller:
    def __init__(self, spider: Spider):
        try:
            from pyPS4Controller.controller import Controller
        except ImportError:
            logging.error("pyPS4Controller is not installed. Run `pip install pyPS4Controller`")
            return

        self.spider = spider
        self.gait = TripodGait(spider)
        
        class MyController(Controller):
            def __init__(self, gait, **kwargs):
                Controller.__init__(self, **kwargs)
                self.gait = gait
                self.action = None
                self.running = True
                self.action_thread = threading.Thread(target=self.run_action)
                self.action_thread.start()

            def run_action(self):
                while self.running:
                    if self.action == 'forward':
                        self.gait.walk_forward()
                    elif self.action == 'backward':
                        self.gait.walk_backward()
                    elif self.action == 'step_left':
                        self.gait.step_left()
                    elif self.action == 'step_right':
                        self.gait.step_right()
                    else:
                        time.sleep(0.01)

            def on_L3_up(self, value):
                self.action = 'forward'
                
            def on_L3_down(self, value):
                self.action = 'backward'
                
            def on_L3_left(self, value):
                self.action = 'step_left'
                
            def on_L3_right(self, value):
                self.action = 'step_right'

            def on_L3_y_at_rest(self):
                if self.action in ['forward', 'backward']:
                    self.action = None

            def on_L3_x_at_rest(self):
                if self.action in ['step_left', 'step_right']:
                    self.action = None
                
            def on_R3_left(self, value):
                self.gait.turn_left()
                
            def on_R3_right(self, value):
                self.gait.turn_right()
                
            def on_disconnect(self):
                self.running = False
                
        self.controller = MyController(gait=self.gait, interface="/dev/input/js0", connecting_using_ds4drv=False)

    def start(self):
        if hasattr(self, 'controller'):
            logging.info("PS4 controller started.")
            self.controller.listen()
