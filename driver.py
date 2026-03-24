import time
import logging

from leg_config import LegConfig
from obstacle_sensor_config import ObstacleSensorConfig
from obstacle_sensor import ObstacleSensor
from spider import Spider
from joint_config import JointConfig
from joint import Joint
from leg import Leg
from enums import Legs


logging.basicConfig(
    level=logging.INFO,  # Set the minimum level to log (INFO, DEBUG, etc.)
    format='\r%(asctime)s - %(levelname)s - %(message)s\r\n',
)

front_left_hip_config = JointConfig("TowerPro MG90S", "Positional", "Front Left Hip", channel=2, i2c_address=0x41)
front_left_knee_config = JointConfig("TowerPro MG90S", "Positional", "Front Left knee", channel=7, i2c_address=0x41)
front_left_ankle_config = JointConfig("TowerPro MG90S", "Positional", "Front Left Ankle", channel=15, i2c_address=0x41)
front_left_knee_joint = Joint(front_left_knee_config)
front_left_ankle_joint = Joint(front_left_ankle_config)
front_left_hip_joint = Joint(front_left_hip_config)
front_left_leg = Leg(front_left_hip_joint, front_left_knee_joint, front_left_ankle_joint, LegConfig(mount_angle=45, position=Legs.FRONT_LEFT, inverse_hip=True, hip_trim_angle=-5))

rear_left_hip_config = JointConfig("TowerPro MG90S", "Positional", "Rear Left Hip", channel=13, i2c_address=0x41)
rear_left_knee_config = JointConfig("TowerPro MG90S", "Positional", "Rear Left knee", channel=5, i2c_address=0x41)
rear_left_ankle_config = JointConfig("TowerPro MG90S", "Positional", "Rear Left Ankle", channel=0, i2c_address=0x41)
rear_left_knee_joint = Joint(rear_left_knee_config)
rear_left_ankle_joint = Joint(rear_left_ankle_config)
rear_left_hip_joint = Joint(rear_left_hip_config)
rear_left_leg = Leg(rear_left_hip_joint, rear_left_knee_joint, rear_left_ankle_joint, LegConfig(mount_angle=45, position=Legs.REAR_LEFT, inverse_hip=True, hip_trim_angle=9))

front_right_ankle_config = JointConfig("TowerPro MG90S", "Positional", "Front Right Ankle", channel=0, i2c_address=0x40)
front_right_knee_config = JointConfig("TowerPro MG90S", "Positional", "Front Right knee", channel=12, i2c_address=0x40)
front_right_hip_config = JointConfig("TowerPro MG90S", "Positional", "Front Right Hip", channel=14, i2c_address=0x40)
front_right_knee_joint = Joint(front_right_knee_config)
front_right_ankle_joint = Joint(front_right_ankle_config)
front_right_hip_joint = Joint(front_right_hip_config)
front_right_leg = Leg(front_right_hip_joint, front_right_knee_joint, front_right_ankle_joint, LegConfig(mount_angle=45, position=Legs.FRONT_RIGHT))

rear_right_hip_config = JointConfig("TowerPro MG90S", "Positional", "Rear Right Hip", channel=3, i2c_address=0x40)
rear_right_knee_config = JointConfig("TowerPro MG90S", "Positional", "Rear Right knee", channel=7, i2c_address=0x40)
rear_right_ankle_config = JointConfig("TowerPro MG90S", "Positional", "Rear Right Ankle", channel=15, i2c_address=0x40)
rear_right_knee_joint = Joint(rear_right_knee_config)
rear_right_ankle_joint = Joint(rear_right_ankle_config)
rear_right_hip_joint = Joint(rear_right_hip_config)
rear_right_leg = Leg(rear_right_hip_joint, rear_right_knee_joint, rear_right_ankle_joint, LegConfig(mount_angle=45, position=Legs.REAR_RIGHT, hip_trim_angle=-15))


middle_right_ankle_config = JointConfig("TowerPro MG90S", "Positional", "Middle Right Ankle", channel=4, i2c_address=0x40)
middle_right_knee_config = JointConfig("TowerPro MG90S", "Positional", "Middle Right knee", channel=8, i2c_address=0x40)
middle_right_hip_config = JointConfig("TowerPro MG90S", "Positional", "Middle Right Hip", channel=5, i2c_address=0x40)
middle_right_knee_joint = Joint(middle_right_knee_config)
middle_right_ankle_joint = Joint(middle_right_ankle_config)
middle_right_hip_joint = Joint(middle_right_hip_config)
middle_right_leg = Leg(middle_right_hip_joint, middle_right_knee_joint, middle_right_ankle_joint, LegConfig(mount_angle=45, position=Legs.MIDDLE_RIGHT, hip_trim_angle=-7))


middle_left_ankle_config = JointConfig("TowerPro MG90S", "Positional", "Middle Left Ankle", channel=6, i2c_address=0x41)
middle_left_knee_config = JointConfig("TowerPro MG90S", "Positional", "Middle left knee", channel=8, i2c_address=0x41)
middle_left_hip_config = JointConfig("TowerPro MG90S", "Positional", "Middle Left Hip", channel=14, i2c_address=0x41)
middle_left_knee_joint = Joint(middle_left_knee_config)
middle_left_ankle_joint = Joint(middle_left_ankle_config)
middle_left_hip_joint = Joint(middle_left_hip_config)
middle_left_leg = Leg(middle_left_hip_joint, middle_left_knee_joint, middle_left_ankle_joint, LegConfig(mount_angle=45, position=Legs.MIDDLE_LEFT, inverse_hip=True, hip_trim_angle=7))

def on_obstacle_distance_measure_front(distance_in_cm: float):
    pass

front_obstacle_sensor_config : ObstacleSensorConfig = ObstacleSensorConfig("Ultra Sonic HC-SR04", "Front Obstacle Sensor", trig_gpio_pin=0, echo_gpio_pin=0)
front_obstacle_sensor:ObstacleSensor = ObstacleSensor(front_obstacle_sensor_config, on_obstacle_distance_measure_front)


spider:Spider = Spider(front_right_leg=front_right_leg,
                 front_left_leg=front_left_leg,
                 rear_right_leg=rear_right_leg,
                 rear_left_leg=rear_left_leg,
                 middle_left_leg=middle_left_leg,
                 middle_right_leg=middle_right_leg)

#spider.startup()
#time.sleep(20)
#spider.shutdown()