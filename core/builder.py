from core.spider import Spider
from core.leg import Leg
from core.config.leg_config import LegConfig
from hardware.joint import Joint
from hardware.config.joint_config import JointConfig
from hardware.obstacle_sensor import ObstacleSensor
from hardware.config.obstacle_sensor_config import ObstacleSensorConfig
from type import Legs

class SpiderBuilder:
    def __init__(self):
        self.legs = {}
        self.sensors = {}
        # Centralizing addresses makes it easier to debug the PCA9685 boards
        self.LEFT_ADDR = 0x41
        self.RIGHT_ADDR = 0x40

    def _create_leg(self, side_addr, position, channels, mount_angle=45, inverse_hip=False, hip_trim=0):
        """Helper to reduce repetitive Joint and Leg instantiation."""
        hip_cfg = JointConfig("MG995/996R", "Positional", f"{position.name} Hip", channel=channels[0], i2c_address=side_addr)
        knee_cfg = JointConfig("MG995/996R", "Positional", f"{position.name} Knee", channel=channels[1], i2c_address=side_addr)
        ankle_cfg = JointConfig("MG995/996R", "Positional", f"{position.name} Ankle", channel=channels[2], i2c_address=side_addr)

        leg_cfg = LegConfig(
            mount_angle=mount_angle, 
            position=position, 
            inverse_hip=inverse_hip, 
            hip_trim_angle=hip_trim
        )

        return Leg(Joint(hip_cfg), Joint(knee_cfg), Joint(ankle_cfg), leg_cfg)

    def build_legs(self):
        # Left Side (0x41) - Note the 'inverse_hip=True' for the whole side
        self.legs['FL'] = self._create_leg(self.LEFT_ADDR, Legs.FRONT_LEFT, [2, 7, 15], inverse_hip=True, hip_trim=-5)
        self.legs['ML'] = self._create_leg(self.LEFT_ADDR, Legs.MIDDLE_LEFT, [14, 8, 6], inverse_hip=True, hip_trim=7)
        self.legs['RL'] = self._create_leg(self.LEFT_ADDR, Legs.REAR_LEFT, [13, 5, 0], inverse_hip=True, hip_trim=9)

        # Right Side (0x40)
        self.legs['FR'] = self._create_leg(self.RIGHT_ADDR, Legs.FRONT_RIGHT, [14, 12, 0])
        self.legs['MR'] = self._create_leg(self.RIGHT_ADDR, Legs.MIDDLE_RIGHT, [5, 8, 4], hip_trim=-7)
        self.legs['RR'] = self._create_leg(self.RIGHT_ADDR, Legs.REAR_RIGHT, [3, 7, 15], hip_trim=-15)
        
        return self

    def add_sensors(self, front_obstacle_callback):
        config = ObstacleSensorConfig("HC-SR04", "Front Obstacle Sensor", trig_gpio_pin=0, echo_gpio_pin=0)
        self.sensors['front'] = ObstacleSensor(config, front_obstacle_callback)
        return self

    def get_spider(self) -> Spider:
        """Finalizes and returns the Singleton Spider instance."""
        return Spider(
            front_right_leg=self.legs['FR'],
            front_left_leg=self.legs['FL'],
            rear_right_leg=self.legs['RR'],
            rear_left_leg=self.legs['RL'],
            middle_left_leg=self.legs['ML'],
            middle_right_leg=self.legs['MR']
        )

# --- Initialization ---
def on_obstacle_distance_measure_front(distance_in_cm: float):
    pass
