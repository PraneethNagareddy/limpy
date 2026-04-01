import RPi.GPIO as GPIO
import time
import sys

# Standard Broadcom (BCM) pin numbers used on Raspberry Pi
# We will scan all common GPIO pins
GPIO_PINS = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19, 26, 14, 15, 18, 23, 24, 25, 8, 7, 12, 16, 20, 21]

def setup():
    GPIO.setmode(GPIO.BCM)
    for pin in GPIO_PINS:
        try:
            # Setting up with PULL_UP assumes the switch connects the pin to Ground when pressed
            # If your switches connect to 3.3V, you would use PULL_DOWN
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        except Exception as e:
            print(f"Skipping pin {pin}: {e}")

def main():
    print("--- Leg Sensor Identification Script ---")
    print("Press a switch on any leg to identify its GPIO pin.")
    print("Press Ctrl+C to exit.\n")
    
    setup()
    
    # Store initial states
    last_states = {pin: GPIO.input(pin) for pin in GPIO_PINS}
    
    try:
        while True:
            for pin in GPIO_PINS:
                try:
                    current_state = GPIO.input(pin)
                    # If state changed from HIGH (1) to LOW (0), it was pressed (due to PULL_UP)
                    if current_state == GPIO.LOW and last_states[pin] == GPIO.HIGH:
                        print(f"DETECTED: Pin {pin} was PRESSED!")
                    elif current_state == GPIO.HIGH and last_states[pin] == GPIO.LOW:
                        print(f"RELEASED: Pin {pin} was released.")
                    
                    last_states[pin] = current_state
                except:
                    continue
            time.sleep(0.05) # 20Hz scan rate
    except KeyboardInterrupt:
        print("\nExiting and cleaning up GPIO...")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
