import logging
from driver import spider
from controller import KeyboardController
import sys
import atexit

# Configure logging to see what's happening
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    logging.info("Initializing Keyboard Controller...")
    
    # Initialize the controller with our spider instance
    controller = KeyboardController(spider)
    
    print("\n" + "="*50)
    print("ROBOT KEYBOARD CONTROLLER")
    print("="*50)
    print("Controls:")
    print("  Up Arrow       : Walk Forward")
    print("  Down Arrow     : Walk Backward")
    print("  'A' Key        : Step Left")
    print("  'D' Key        : Step Right")
    print("  Left Arrow     : Turn Left")
    print("  Right Arrow    : Turn Right")
    print("  ESC / 'Q'      : Stop & Exit")
    print("="*50 + "\n")
    
    try:
        # Start listening for key presses
        controller.start()
    except Exception as e:
        logging.error(f"Failed to start controller: {e}")
    finally:
        controller.stop()
        logging.info("Controller stopped.")

if __name__ == "__main__":
    main()
