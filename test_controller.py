import logging
from driver import spider
from controller import KeyboardController
import sys
import termios
import tty
import atexit

# Configure logging to see what's happening
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def disable_echo(fd, old_settings):
    """Restores the terminal settings"""
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

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
    print("  Left Arrow     : Step Left")
    print("  Right Arrow    : Step Right")
    print("  Ctrl + Left    : Turn Left (Single Step)")
    print("  Ctrl + Right   : Turn Right (Single Step)")
    print("  ESC            : Stop & Exit")
    print("="*50 + "\n")
    
    # Save the current terminal settings so we can restore them later
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    
    # Ensure terminal settings are always restored when script exits
    atexit.register(disable_echo, fd, old_settings)
    
    try:
        # tty.setcbreak puts terminal in mode where it reads keys without echoing them to the screen
        tty.setcbreak(sys.stdin.fileno())
        # Start listening for key presses
        controller.start()
    except Exception as e:
        logging.error(f"Failed to start controller: {e}")
    finally:
        controller.stop()
        logging.info("Controller stopped.")

if __name__ == "__main__":
    main()
