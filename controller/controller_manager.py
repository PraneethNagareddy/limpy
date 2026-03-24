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
        self.__init_keyboard_controller()

    @staticmethod
    def __init_keyboard_controller():
        logging.info("Initializing Keyboard Controller...")

        # Initialize the controller with our spider instance
        controller = KeyboardController()

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
            controller.start()
        except Exception as e:
            logging.error(f"Failed to start controller: {e}")
        finally:
            controller.stop()
            logging.info("Controller stopped.")
