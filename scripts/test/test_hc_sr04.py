import RPi.GPIO as GPIO
import time
import sys

# Pin Definitions (using BCM numbering as requested)
# BOARD 13 -> BCM 27 (TRIG)
# BOARD 16 -> BCM 23 (ECHO)
GPIO_TRIGGER = 27  # BCM pin for TRIG
GPIO_ECHO = 23     # BCM pin for ECHO

# Set to True to enable detailed debugging prints for measure_distance failures
DEBUG_MEASURE_DISTANCE = True 

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    GPIO.output(GPIO_TRIGGER, False) # Ensure trigger is low
    print("GPIO setup complete (BCM mode).")

def measure_distance():
    """Measures distance using the HC-SR04 sensor with GPIO.wait_for_edge."""
    # Ensure trigger is low for a moment to ensure a clean pulse
    GPIO.output(GPIO_TRIGGER, False)
    time.sleep(0.000002) # Small delay to ensure clean state

    # Send a 10us pulse to the trigger pin
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001) # 10 microsecond pulse
    GPIO.output(GPIO_TRIGGER, False)

    # --- Crucial change: Wait for Echo to go LOW before waiting for RISING edge ---
    # This ensures the pin is in a known idle state (LOW) before we expect the echo.
    # Add a timeout to prevent infinite loop if Echo is truly stuck HIGH.
    start_time = time.time()
    while GPIO.input(GPIO_ECHO) == 1: # Wait for the pin to go LOW
        if time.time() - start_time > 0.01: # 10ms timeout for Echo to go LOW
            if DEBUG_MEASURE_DISTANCE:
                print("DEBUG: Echo pin stuck HIGH before RISING edge wait.")
            return -1
    
    # Wait for the echo pin to go HIGH (rising edge)
    # Timeout is in milliseconds. 50ms is enough for max range ~400cm (23.32ms round trip)
    pulse_start_time = GPIO.wait_for_edge(GPIO_ECHO, GPIO.RISING, timeout=50) # Timeout in ms
    if pulse_start_time is None: # Timeout occurred, no rising edge detected
        if DEBUG_MEASURE_DISTANCE:
            print("DEBUG: Timeout - Echo never went HIGH after trigger.")
        return -1

    # Wait for the echo pin to go LOW (falling edge)
    pulse_end_time = GPIO.wait_for_edge(GPIO_ECHO, GPIO.FALLING, timeout=50) # Timeout in ms
    if pulse_end_time is None: # Timeout occurred, no falling edge detected
        if DEBUG_MEASURE_DISTANCE:
            print("DEBUG: Timeout - Echo never went LOW after rising edge.")
        return -1

    # GPIO.wait_for_edge returns the time in seconds since epoch when the edge was detected.
    duration = pulse_end_time - pulse_start_time
    
    # Filter out obviously bad durations (e.g., negative or excessively long/short)
    # Min duration for 2cm round trip is (2*2)/34300 = 0.0001166s = 116.6us
    # Max duration for 400cm round trip is (400*2)/34300 = 0.02332s = 23.32ms
    if duration < 0.0001 or duration > 0.025: # Roughly 100us to 25ms
        if DEBUG_MEASURE_DISTANCE:
            print(f"DEBUG: Filtered out bad duration: {duration*1000000:.2f} us")
        return -1

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
        time.sleep(0.03) # Slightly increased gap between bursts to 30ms

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
    if DEBUG_MEASURE_DISTANCE:
        print("DEBUG_MEASURE_DISTANCE is ENABLED. You will see debug messages for failed measurements.")

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
