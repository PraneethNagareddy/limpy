import logging
import threading

from hardware.config.obstacle_sensor_config import ObstacleSensorConfig
import RPi.GPIO as GPIO         #imports modules required in program
import time                     #time module is used to add delays


class ObstacleSensor:

    def __init__(self, obstacle_sensor_config: ObstacleSensorConfig, callback):
        if obstacle_sensor_config.trig_gpio_pin == -1 or obstacle_sensor_config.echo_gpio_pin == -1:
            raise Exception("Unable to instantiate obstacle sensor: %s", obstacle_sensor_config.common_name)
        self.obstacle_sensor_config = obstacle_sensor_config
        self.callback = callback
        self._on_loop = False

    def initialize(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.obstacle_sensor_config.trig_gpio_pin, GPIO.OUT)  # trig pin is output
        GPIO.setup(self.obstacle_sensor_config.echo_gpio_pin, GPIO.IN)  # echo pin is input
        GPIO.OUTPUT(self.obstacle_sensor_config.trig_gpio_pin, GPIO.LOW)  # drives trig pin to 0V
        time.sleep(2)
        logging.info("Obstacle sensor initialized")

    def listen(self, run_on_loop: bool):
        if not run_on_loop:
            threading.Thread(target=self._measure_distance_once, daemon=False).start()
        else:
            threading.Thread(target=self._measure_distance_continuously, daemon=True).start()

    def _measure_distance_continuously(self):
        logging.debug("Initializing Obstacle Sensor Continuously")
        while self._on_loop:
            self._measure_distance_once()
            time.sleep(self.obstacle_sensor_config.polling_interval_sec)


    def _measure_distance_once(self):
        pulse_received = time.time()
        pulse_send = time.time()
        GPIO.output(self.obstacle_sensor_config.trig_gpio_pin, GPIO.HIGH)  # set trig pin high
        time.sleep(0.00001)  # keeps trig pin high for 10 microseconds. This is used to trigger/start the ultrasonic module. Sends 8 ultrasonic bursts at 40KHz.
        GPIO.output(self.obstacle_sensor_config.trig_gpio_pin, GPIO.LOW)  # Set trig pin low

        while GPIO.input(self.obstacle_sensor_config.echo_gpio_pin) == 0:  # check when the echo pin goes low and
            pulse_send = time.time()  # note down this time stamp in pulse_send

        while GPIO.input(self.obstacle_sensor_config.echo_gpio_pin) == 1:  # check when the echo pin goes high and
            pulse_received = time.time()  # note down this time stamp

        pulse_duration = pulse_received - pulse_send
        pulse_duration = round(pulse_duration / 2, 2)

        # The round function rounds off the value upto 2 decimal places.

        distance = 34000 * pulse_duration
        logging.debug("Distance measured: %s", distance)
        self.callback(distance)