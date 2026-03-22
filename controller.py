import sys
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
        
    def get_key(self):
        """Reads a single keypress or escape sequence from the terminal"""
        import termios
        import tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            # Check for escape sequence
            if ch == '\x1b':
                ch2 = sys.stdin.read(1)
                if ch2 == '[':
                    ch3 = sys.stdin.read(1)
                    if ch3 == '1': # Might be ctrl+arrow (e.g., \x1b[1;5C)
                        ch4 = sys.stdin.read(1)
                        if ch4 == ';':
                            ch5 = sys.stdin.read(1)
                            if ch5 == '5':
                                ch6 = sys.stdin.read(1)
                                return 'ctrl+' + ch6
                    return '\x1b[' + ch3
                return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def start(self):
        self.running = True
        logging.info("Keyboard controller started. Use arrow keys to move. (Press 'q' or 'esc' to stop)")
        
        while self.running:
            try:
                key = self.get_key()
                
                if key == '\x1b[A':  # Up Arrow
                    logging.info("Up Arrow Pressed")
                    self.gait.walk_forward()
                elif key == '\x1b[B':  # Down Arrow
                    logging.info("Down Arrow Pressed")
                    self.gait.walk_backward()
                elif key == '\x1b[D':  # Left Arrow
                    logging.info("Left Arrow Pressed")
                    self.gait.step_left()
                elif key == '\x1b[C':  # Right Arrow
                    logging.info("Right Arrow Pressed")
                    self.gait.step_right()
                elif key == 'ctrl+D':  # Ctrl + Left Arrow
                    logging.info("Ctrl+Left Pressed")
                    self.gait.turn_left()
                elif key == 'ctrl+C':  # Ctrl + Right Arrow
                    logging.info("Ctrl+Right Pressed")
                    self.gait.turn_right()
                elif key == '\x1b' or key.lower() == 'q' or key == '\x03':  # Esc, Q, or Ctrl+C
                    logging.info("Exit key pressed.")
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
