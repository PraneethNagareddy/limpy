import logging
from driver import spider
from controller import KeyboardController
import sys
import atexit

# Configure logging to see what's happening
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s\n')

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
    print("  Left Arrow     : Walk Left")
    print("  Right Arrow    : Walk Right")
    print("  'A' Key        : Turn Left")
    print("  'D' Key        : Turn Right")
    print("  'Z' Key        : Step Left")
    print("  'C' Key        : Step Right")
    print("  Up + Left      : Walk Forward + Left (Omni)")
    print("  Q / ESC        : Stop & Exit")
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
