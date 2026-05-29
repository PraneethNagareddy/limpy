from core.spider import Spider
from core.leg import Leg
from core.config.leg_config import LegConfig
from hardware.joint import Joint
from hardware.config.joint_config import JointConfig
from hardware.obstacle_sensor import ObstacleSensor
from hardware.config.obstacle_sensor_config import ObstacleSensorConfig
from hardware.feedback_communicator import FeedbackCommunicator
from hardware.led_feedback_communicator import LEDFeedbackCommunicator
from type import Legs

class SpiderBuilder:
    def __init__(self):
        self.legs = {}
        self.sensors = {}
        self.feedback_communicator: FeedbackCommunicator = None
        # Centralizing addresses makes it easier to debug the PCA9685 boards
        self.LEFT_ADDR = 0x41
        self.RIGHT_ADDR = 0x40

    def build_legs(self):
        # Front Left Leg
        fl_hip_cfg = JointConfig("MG995/996R", "Positional", "Front Left Hip", channel=3, i2c_address=self.LEFT_ADDR)
        fl_knee_cfg = JointConfig("MG995/996R", "Positional", "Front Left Knee", channel=11, i2c_address=self.RIGHT_ADDR)
        fl_ankle_cfg = JointConfig("MG995/996R", "Positional", "Front Left Ankle", channel=15, i2c_address=self.RIGHT_ADDR)
        self.legs['FL'] = Leg(Joint(fl_hip_cfg), Joint(fl_knee_cfg), Joint(fl_ankle_cfg), 
                              LegConfig(mount_angle=45, position=Legs.FRONT_LEFT, inverse_hip=True, hip_trim_angle=-5))

        # Middle Left Leg
        ml_hip_cfg = JointConfig("MG995/996R", "Positional", "Middle Left Hip", channel=2, i2c_address=self.RIGHT_ADDR)
        ml_knee_cfg = JointConfig("MG995/996R", "Positional", "Middle Left Knee", channel=4, i2c_address=self.RIGHT_ADDR)
        ml_ankle_cfg = JointConfig("MG995/996R", "Positional", "Middle Left Ankle", channel=5, i2c_address=self.LEFT_ADDR)
        self.legs['ML'] = Leg(Joint(ml_hip_cfg), Joint(ml_knee_cfg), Joint(ml_ankle_cfg), 
                              LegConfig(mount_angle=45, position=Legs.MIDDLE_LEFT, inverse_hip=True, hip_trim_angle=7))

        # Rear Left Leg
        rl_hip_cfg = JointConfig("MG995/996R", "Positional", "Rear Left Hip", channel=8, i2c_address=self.LEFT_ADDR)
        rl_knee_cfg = JointConfig("MG995/996R", "Positional", "Rear Left Knee", channel=1, i2c_address=self.RIGHT_ADDR)
        rl_ankle_cfg = JointConfig("MG995/996R", "Positional", "Rear Left Ankle", channel=0, i2c_address=self.RIGHT_ADDR)
        self.legs['RL'] = Leg(Joint(rl_hip_cfg), Joint(rl_knee_cfg), Joint(rl_ankle_cfg), 
                              LegConfig(mount_angle=45, position=Legs.REAR_LEFT, inverse_hip=True, hip_trim_angle=9))

        # Front Right Leg
        fr_hip_cfg = JointConfig("MG995/996R", "Positional", "Front Right Hip", channel=3, i2c_address=self.RIGHT_ADDR)
        fr_knee_cfg = JointConfig("MG995/996R", "Positional", "Front Right Knee", channel=1, i2c_address=self.LEFT_ADDR)
        fr_ankle_cfg = JointConfig("MG995/996R", "Positional", "Front Right Ankle", channel=14, i2c_address=self.RIGHT_ADDR)
        self.legs['FR'] = Leg(Joint(fr_hip_cfg), Joint(fr_knee_cfg), Joint(fr_ankle_cfg), 
                              LegConfig(mount_angle=45, position=Legs.FRONT_RIGHT))

        # Middle Right Leg
        mr_hip_cfg = JointConfig("MG995/996R", "Positional", "Middle Right Hip", channel=15, i2c_address=self.LEFT_ADDR)
        mr_knee_cfg = JointConfig("MG995/996R", "Positional", "Middle Right Knee", channel=8, i2c_address=self.RIGHT_ADDR)
        mr_ankle_cfg = JointConfig("MG995/996R", "Positional", "Middle Right Ankle", channel=0, i2c_address=self.LEFT_ADDR)
        self.legs['MR'] = Leg(Joint(mr_hip_cfg), Joint(mr_knee_cfg), Joint(mr_ankle_cfg), 
                              LegConfig(mount_angle=45, position=Legs.MIDDLE_RIGHT, hip_trim_angle=-7))

        # Rear Right Leg
        rr_hip_cfg = JointConfig("MG995/996R", "Positional", "Rear Right Hip", channel=9, i2c_address=self.RIGHT_ADDR)
        rr_knee_cfg = JointConfig("MG995/996R", "Positional", "Rear Right Knee", channel=7, i2c_address=self.LEFT_ADDR)
        rr_ankle_cfg = JointConfig("MG995/996R", "Positional", "Rear Right Ankle", channel=5, i2c_address=self.RIGHT_ADDR)
        self.legs['RR'] = Leg(Joint(rr_hip_cfg), Joint(rr_knee_cfg), Joint(rr_ankle_cfg), 
                              LegConfig(mount_angle=45, position=Legs.REAR_RIGHT, hip_trim_angle=-15))
        
        return self

    def add_sensors(self, front_obstacle_callback):
        config = ObstacleSensorConfig("HC-SR04", "Front Obstacle Sensor", trig_gpio_pin=0, echo_gpio_pin=0)
        self.sensors['front'] = ObstacleSensor(config, front_obstacle_callback)
        return self

    def add_feedback_communicator(self):
        self.feedback_communicator = LEDFeedbackCommunicator(green_pin=11, white1_pin=22, white2_pin=18)
        return self

    def get_spider(self) -> Spider:
        """Finalizes and returns the Singleton Spider instance."""
        return Spider(
            front_right_leg=self.legs['FR'],
            front_left_leg=self.legs['FL'],
            rear_right_leg=self.legs['RR'],
            rear_left_leg=self.legs['RL'],
            middle_left_leg=self.legs['ML'],
            middle_right_leg=self.legs['MR'],
            feedback_communicator=self.feedback_communicator
        )

# --- Initialization ---
def on_obstacle_distance_measure_front(distance_in_cm: float):
    pass
