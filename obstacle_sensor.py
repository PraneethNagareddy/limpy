from obstacle_sensor_config import ObstacleSensorConfig


class ObstacleSensor:
    def __init__(self, obstacle_sensor_config: ObstacleSensorConfig):
        if obstacle_sensor_config.trig_gpio_pin == -1 or obstacle_sensor_config.echo_gpio_pin == -1:
            raise Exception("Unable to instantiate obstacle sensor: %s", obstacle_sensor_config.common_name)
        self.obstacle_sensor_config = obstacle_sensor_config
