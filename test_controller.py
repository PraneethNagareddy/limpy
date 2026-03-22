import logging
from driver import spider
from controller import KeyboardController

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
    print("  Left Arrow     : Step Left")
    print("  Right Arrow    : Step Right")
    print("  Ctrl + Left    : Turn Left (Single Step)")
    print("  Ctrl + Right   : Turn Right (Single Step)")
    print("  ESC            : Stop & Exit")
    print("="*50 + "\n")
    
    try:
        # Start listening for key presses
        controller.start()
    except KeyboardInterrupt:
        logging.info("Interrupted by user. Exiting...")
    except Exception as e:
        logging.error(f"Failed to start controller: {e}")
        print("\nNote: On Linux/macOS, the 'keyboard' library usually requires sudo privileges.")
        print("Try running with: sudo python3 test_controller.py")
    finally:
        controller.stop()
        logging.info("Controller stopped.")

if __name__ == "__main__":
    main()
