from enums import DistanceUnit


class ObstacleSensorConfig:
    def __init__(self,
                 sensor_type,
                 common_name,
                 trig_gpio_pin=-1,
                 echo_gpio_pin=-1,
                 trigger_duration_sec=0.00001,
                 polling_interval_sec=1,
                 distance_unit: DistanceUnit = DistanceUnit.CENTI_METER):
        self.sensor_type = sensor_type
        self.common_name = common_name
        self.trig_gpio_pin = trig_gpio_pin
        self.echo_gpio_pin = echo_gpio_pin
        self.trigger_duration_sec = trigger_duration_sec
        self.polling_interval_sec = polling_interval_sec
        self.distance_unit = distance_unit