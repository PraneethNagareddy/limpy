import RPi.GPIO as GPIO
import time
import sys

# Pin Definitions (using BCM numbering as requested)
# BOARD 13 -> BCM 27 (TRIG)
# BOARD 16 -> BCM 23 (ECHO)
GPIO_TRIGGER = 27  # BCM pin for TRIG
GPIO_ECHO = 23     # BCM pin for ECHO

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    GPIO.output(GPIO_TRIGGER, False) # Ensure trigger is low
    print("GPIO setup complete (BCM mode).")

def pulse_trigger():
    """Sends a 10us pulse to the trigger pin."""
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001) # 10 microsecond pulse
    GPIO.output(GPIO_TRIGGER, False)

def measure_distance():
    """Measures distance using the HC-SR04 sensor."""
    pulse_trigger()

    pulse_start = 0
    pulse_end = 0

    # Wait for echo to go high
    timeout_start = time.time()
    while GPIO.input(GPIO_ECHO) == 0:
        pulse_start = time.time()
        if time.time() - timeout_start > 0.02: # 20ms timeout (max range is ~400cm)
            # print("Echo pulse start timeout!")
            return -1

    # Wait for echo to go low
    timeout_start = time.time()
    while GPIO.input(GPIO_ECHO) == 1:
        pulse_end = time.time()
        if time.time() - timeout_start > 0.1: # Timeout after 100ms
            print("Echo pulse end timeout!")
            return -1

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150 # Speed of sound in cm/s divided by 2 (to and fro)
    return round(distance, 2)

def get_filtered_distance(samples=5):
    """Takes multiple samples and returns the median to filter out noise."""
    valid_readings = []
    for _ in range(samples):
        dist = measure_distance()
        # HC-SR04 range is ~2cm to 400cm. Ignore obvious garbage.
        if 2.0 <= dist <= 450.0:
            valid_readings.append(dist)
        time.sleep(0.02) # Small gap between bursts

    if not valid_readings:
        return -1
    
    valid_readings.sort()
    return valid_readings[len(valid_readings) // 2]

def main():
    setup_gpio()

    print("\n--- HC-SR04 Test Script ---")
    print("Phase 1: Voltage Verification")
    print("-----------------------------")
    print(f"TRIG pin (BCM): {GPIO_TRIGGER}")
    print(f"ECHO pin (BCM): {GPIO_ECHO}")
    print("\nACTION: Please prepare to measure the voltage on your ECHO pin (after the voltage divider).")
    input("Press Enter to send a single TRIG pulse and then measure the ECHO voltage...")

    pulse_trigger()
    print("TRIG pulse sent. Measure the voltage on the ECHO pin now.")
    print("Expected voltage for a HIGH signal should be around 3.3V (after divider).")
    input("Press Enter when you have measured the voltage and are ready to proceed...")

    print("\nPhase 2: Distance Measurement")
    print("-----------------------------")
    print("ACTION: If you haven't already, connect the ECHO pin (BCM 23) to your Raspberry Pi.")
    input("Press Enter to start continuous distance measurement (Ctrl+C to stop)...")

    try:
        while True:
            dist = get_filtered_distance()
            if dist != -1:
                print(f"Distance: {dist} cm")
            time.sleep(1) # Measure every second
    except KeyboardInterrupt:
        print("\nMeasurement stopped by user.")
    finally:
        GPIO.cleanup()
        print("GPIO cleaned up.")

if __name__ == "__main__":
    main()
