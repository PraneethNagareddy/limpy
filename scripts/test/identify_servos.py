import time
import logging
import sys

try:
    from adafruit_servokit import ServoKit
except ImportError:
    logging.error("Adafruit_ServoKit not found. Please install with: pip3 install adafruit-circuitpython-servokit")
    sys.exit(1)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the I2C addresses for your servo controllers
# Based on your driver.py, you have two boards: 0x40 (RIGHT_ADDR) and 0x41 (LEFT_ADDR)
SERVO_CONTROLLERS = {
    0x40: "Right Side Board",
    0x41: "Left Side Board"
}

# Initialize ServoKit instances
kits = {}
for addr, name in SERVO_CONTROLLERS.items():
    try:
        kits[addr] = ServoKit(channels=16, address=addr)
        logging.info(f"Initialized {name} at I2C address 0x{addr:x}")
    except OSError:
        logging.error(f"Could not find servo controller at I2C address 0x{addr:x}. Check wiring and I2C bus.")
        sys.exit(1)

def perform_movement(kit, channel):
    """Performs the distinct movement sequence for a servo."""
    kit.servo[channel].angle = 120
    time.sleep(0.5)
    kit.servo[channel].angle = 60
    time.sleep(0.5)
    kit.servo[channel].angle = 90
    time.sleep(0.5)

def move_servo_and_identify(kit, channel, board_name):
    """Moves a servo on a specific channel and prompts user for identification, with repeat option."""
    print(f"\n--- Testing {board_name}, Channel {channel} ---")
    
    perform_movement(kit, channel) # Initial movement
    
    while True:
        choice = input(f"Which servo moved on {board_name}, Channel {channel}? (Type name, 'r' to repeat, or 'skip'): ").strip().lower()
        
        if choice == 'r':
            print("Repeating movement...")
            perform_movement(kit, channel)
        elif choice == 'skip':
            return 'skip'
        elif choice: # User entered a name
            return choice
        else:
            print("Invalid input. Please type a name, 'r' to repeat, or 'skip'.")

def main():
    print("\n--- Servo Identification Script ---")
    print("This script will cycle through each channel on your servo controllers.")
    print("Observe which servo moves and enter its name.")
    print("Press Ctrl+C to exit at any time.\n")

    identified_servos = {}

    try:
        for addr, kit in kits.items():
            board_name = SERVO_CONTROLLERS[addr]
            print(f"\nStarting identification for {board_name} (0x{addr:x})...")
            for channel in range(16): # Channels 0-15
                servo_name = move_servo_and_identify(kit, channel, board_name)
                if servo_name == 'skip':
                    print(f"Skipping {board_name}, Channel {channel}.")
                elif servo_name:
                    identified_servos[f"Board 0x{addr:x}, Channel {channel}"] = servo_name
                    print(f"Mapped: {servo_name} -> Board 0x{addr:x}, Channel {channel}")
                else:
                    print(f"No name entered for Board 0x{addr:x}, Channel {channel}. Skipping.")
                
                # Ensure servo is at neutral after identification
                kit.servo[channel].angle = 90
                time.sleep(0.2)

    except KeyboardInterrupt:
        print("\nIdentification interrupted by user.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    finally:
        print("\n--- Identification Complete ---")
        if identified_servos:
            print("Identified Servo Mappings:")
            for mapping, name in identified_servos.items():
                print(f"  {name}: {mapping}")
            print("\nConsider updating your 'joint_config.py' with these mappings.")
        else:
            print("No servos were identified.")
        
        # Reset all servos to 90 degrees on all boards
        print("Resetting all identified servos to 90 degrees...")
        for addr, kit in kits.items():
            for channel in range(16):
                try:
                    kit.servo[channel].angle = 90
                except Exception as e:
                    logging.debug(f"Could not reset servo on board 0x{addr:x}, channel {channel}: {e}")
        time.sleep(1)
        logging.info("All servos reset.")

if __name__ == "__main__":
    main()
