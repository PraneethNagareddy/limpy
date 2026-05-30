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

def measure_distance():
    """Measures distance using the HC-SR04 sensor."""
    # Ensure trigger is low before pulsing
    GPIO.output(GPIO_TRIGGER, False)
    time.sleep(0.000002) # 2us delay

    # Send a 10us pulse to the trigger pin
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    pulse_start = time.time()
    pulse_end = time.time()

    # Wait for echo to go high
    timeout = time.time() + 0.02 # 20ms timeout for echo to start
    while GPIO.input(GPIO_ECHO) == 0:
        if time.time() > timeout:
            # print("Timeout: Echo never went HIGH") # Uncomment for debugging
            return -1
    pulse_start = time.time() # Capture time when it *first* goes high

    # Wait for echo to go low
    timeout = time.time() + 0.02 # 20ms timeout for echo to end
    while GPIO.input(GPIO_ECHO) == 1:
        if time.time() > timeout:
            # print("Timeout: Echo never went LOW") # Uncomment for debugging
            return -1
    pulse_end = time.time() # Capture time when it *first* goes low

    duration = pulse_end - pulse_start
    distance = (duration * 34300) / 2 # Speed of sound is 34300 cm/s
    return round(distance, 2)

def get_filtered_distance(samples=5):
    """Takes multiple samples and returns the median to filter out noise."""
    valid_readings = []
    for _ in range(samples):
        dist = measure_distance()
        # HC-SR04 range is ~2cm to 400cm. Ignore obvious garbage.
        if 2.0 <= dist <= 450.0: # Increased max range slightly for robustness
            valid_readings.append(dist)
        time.sleep(0.02) # Small gap between bursts

    if not valid_readings:
        return -1
    
    valid_readings.sort()
    return valid_readings[len(valid_readings) // 2]

def main():
    setup_gpio()

    print("\n--- HC-SR04 Distance Measurement Test ---")
    print(f"TRIG pin (BCM): {GPIO_TRIGGER}")
    print(f"ECHO pin (BCM): {GPIO_ECHO}")
    print("Starting continuous distance measurement (Ctrl+C to stop)...")

    try:
        while True:
            dist = get_filtered_distance()
            if dist != -1:
                print(f"Distance: {dist} cm")
            else:
                print("Measuring...") # Indicate that a measurement was attempted but failed
            time.sleep(0.5) # Measure twice per second
    except KeyboardInterrupt:
        print("\nMeasurement stopped by user.")
    finally:
        GPIO.cleanup()
        print("GPIO cleaned up.")

if __name__ == "__main__":
    main()
