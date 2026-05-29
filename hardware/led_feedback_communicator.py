import RPi.GPIO as GPIO
import time
import threading
import logging
import math
from hardware.feedback_communicator import FeedbackCommunicator
from core.feedback_enums import FeedbackStatus

class LEDFeedbackCommunicator(FeedbackCommunicator):
    def __init__(self, green_pin: int, white1_pin: int, white2_pin: int):
        self.green_pin = green_pin
        self.white1_pin = white1_pin
        self.white2_pin = white2_pin
        self.pins = {
            "GREEN": green_pin,
            "WHITE1": white1_pin,
            "WHITE2": white2_pin
        }

        self.led_states = {pin: "OFF" for pin in self.pins.values()}
        self.pwm_objects = {}
        self.pwm_frequency = 100 # Hz

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False) # Suppress warnings

        for pin in self.pins.values():
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW) # Start with all LEDs off
            self.pwm_objects[pin] = GPIO.PWM(pin, self.pwm_frequency)
            self.pwm_objects[pin].start(0) # Start PWM with 0% duty cycle (off)

        self.running = True
        self.feedback_thread = threading.Thread(target=self._update_leds, daemon=True)
        self.feedback_thread.start()
        logging.info("LEDFeedbackCommunicator initialized with Green:%d, White1:%d, White2:%d", green_pin, white1_pin, white2_pin)

    def _set_led_state(self, pin: int, state: str):
        if pin not in self.pins.values():
            logging.warning("Pin %d not configured for LEDFeedbackCommunicator.", pin)
            return
        self.led_states[pin] = state.upper()

    def _update_leds(self):
        while self.running:
            for pin, state in self.led_states.items():
                if state == "ON":
                    self.pwm_objects[pin].ChangeDutyCycle(100)
                elif state == "OFF":
                    self.pwm_objects[pin].ChangeDutyCycle(0)
                elif state == "PULSATING":
                    duty_cycle = (math.sin(time.time() * 5) + 1) / 2 * 100 # Sine wave pulsation
                    self.pwm_objects[pin].ChangeDutyCycle(duty_cycle)
            time.sleep(0.02) # Update rate for pulsation

    def communicate_startup(self, is_smooth: bool = True):
        logging.info(f"Communicating startup (smooth={is_smooth})")
        self._set_led_state(self.pins["GREEN"], "ON")
        self._set_led_state(self.pins["WHITE1"], "OFF")
        self._set_led_state(self.pins["WHITE2"], "OFF")
        # You might add a sequence here, e.g., flash white LEDs once

    def communicate_movement(self, is_moving: bool):
        if is_moving:
            logging.info("Communicating movement: PULSATING Green")
            self._set_led_state(self.pins["GREEN"], "PULSATING")
        else:
            logging.info("Communicating movement: Solid Green (Idle)")
            self._set_led_state(self.pins["GREEN"], "ON")
        self._set_led_state(self.pins["WHITE1"], "OFF")
        self._set_led_state(self.pins["WHITE2"], "OFF")

    def communicate_status(self, status: FeedbackStatus):
        logging.info(f"Communicating status: {status.name}")
        # This is where you'd map your 9 combinations.
        # For now, let's implement a few examples.
        self._set_led_state(self.pins["GREEN"], "OFF") # Reset green for status codes

        if status == FeedbackStatus.ROBOT_IDLE:
            self._set_led_state(self.pins["GREEN"], "ON")
            self._set_led_state(self.pins["WHITE1"], "OFF")
            self._set_led_state(self.pins["WHITE2"], "OFF")
        elif status == FeedbackStatus.ROBOT_MOVING:
            self._set_led_state(self.pins["GREEN"], "PULSATING")
            self._set_led_state(self.pins["WHITE1"], "OFF")
            self._set_led_state(self.pins["WHITE2"], "OFF")
        elif status == FeedbackStatus.ROBOT_ERROR:
            self._set_led_state(self.pins["GREEN"], "OFF")
            self._set_led_state(self.pins["WHITE1"], "PULSATING")
            self._set_led_state(self.pins["WHITE2"], "ON")
        elif status == FeedbackStatus.ROBOT_SHUTDOWN:
            self._set_led_state(self.pins["GREEN"], "OFF")
            self._set_led_state(self.pins["WHITE1"], "OFF")
            self._set_led_state(self.pins["WHITE2"], "OFF")
        elif status == FeedbackStatus.ROBOT_HIBERNATING:
            self._set_led_state(self.pins["GREEN"], "OFF")
            self._set_led_state(self.pins["WHITE1"], "ON")
            self._set_led_state(self.pins["WHITE2"], "OFF")
        # Add more elif blocks for CUSTOM_STATUS_1, CUSTOM_STATUS_2, etc.

    def shutdown(self):
        logging.info("LEDFeedbackCommunicator shutting down.")
        self.running = False
        self.feedback_thread.join(timeout=1)
        for pin in self.pins.values():
            self.pwm_objects[pin].stop()
        GPIO.cleanup()
        logging.info("LEDFeedbackCommunicator shutdown complete.")
