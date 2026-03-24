import threading

from controller.keyboard_controller import KeyboardController
from controller.ps4_controller import PS4Controller
import logging


class ControllerManager:
    def __init__(self, spider):
        self.spider = spider
        self.keyboard = KeyboardController(spider)
        self.ps4 = PS4Controller(spider)
        self.running = False

    def start(self):
        self.running = True
        threading.Thread(target=self.__init_ps4_controller, daemon=True).start()
        self.__init_keyboard_controller()


    def __init_keyboard_controller(self):
        logging.info("Initializing Keyboard Controller...")
        print("\n" + "=" * 50)
        print("ROBOT KEYBOARD CONTROLLER")
        print("=" * 50)
        print("Controls:")
        print("  Up Arrow       : Walk Forward")
        print("  Down Arrow     : Walk Backward")
        print("  Left Arrow     : Walk Left")
        print("  Right Arrow    : Walk Right")
        print("  'A' Key        : Turn Left")
        print("  'D' Key        : Turn Right")
        print("  'Z' Key        : Step Left")
        print("  'C' Key        : Step Right")
        print("  Up + Left      : Walk Forward + Left (Omni)")
        print("  Q / ESC        : Stop & Exit")
        print("=" * 50 + "\n")

        try:
            # Start listening for key presses
            self.keyboard.start()
        except Exception as e:
            logging.error(f"Failed to start controller: {e}")
        finally:
            self.keyboard.stop()
            logging.info("Controller stopped.")

    def __init_ps4_controller(self):
        logging.info("Skipping ps4 Controller initialization...")
        pass