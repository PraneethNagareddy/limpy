from enums import DistanceUnit


class ObstacleSensorConfig:
    def __init__(self,
                 sensor_type,
                 common_name,
                 trig_gpio_pin=-1,
                 echo_gpio_pin=-1,
                 trig_duration=0,
                 distance_unit: DistanceUnit = DistanceUnit.CENTI_METER):
        self.sensor_type = sensor_type
        self.common_name = common_name
        self.trig_gpio_pin = trig_gpio_pin
        self.echo_gpio_pin = echo_gpio_pin
        self.trig_duration = trig_duration
        self.distance_unit = distance_unit