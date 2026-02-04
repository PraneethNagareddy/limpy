import time
import logging

from obstacle_sensor_config import ObstacleSensorConfig
from obstacle_sensor import ObstacleSensor
from spider import Spider
from joint_config import JointConfig
from joint import Joint
from leg import Leg
from enums import Legs


logging.basicConfig(
    level=logging.INFO,  # Set the minimum level to log (INFO, DEBUG, etc.)
    format='%(asctime)s - %(levelname)s - %(message)s',
)

front_left_hip_config = JointConfig("TowerPro MG90S", "Positional", "Front Left Hip", channel=2)
front_left_knee_config = JointConfig("TowerPro MG90S", "Positional", "Front Left knee", channel=1)
front_left_ankle_config = JointConfig("TowerPro MG90S", "Positional", "Front Left Ankle", channel=0)
front_left_knee_joint = Joint(front_left_knee_config)
front_left_ankle_joint = Joint(front_left_ankle_config)
front_left_hip_joint = Joint(front_left_hip_config)
front_left_leg = Leg(front_left_hip_joint, front_left_knee_joint, front_left_ankle_joint, Legs.FRONT_LEFT)

rear_left_hip_config = JointConfig("TowerPro MG90S", "Positional", "Rear Left Hip", channel=6)
rear_left_knee_config = JointConfig("TowerPro MG90S", "Positional", "Rear Left knee", channel=5)
rear_left_ankle_config = JointConfig("TowerPro MG90S", "Positional", "Rear Left Ankle", channel=4)
rear_left_knee_joint = Joint(rear_left_knee_config)
rear_left_ankle_joint = Joint(rear_left_ankle_config)
rear_left_hip_joint = Joint(rear_left_hip_config)
rear_left_leg = Leg(rear_left_hip_joint, rear_left_knee_joint, rear_left_ankle_joint, Legs.REAR_LEFT)

front_right_ankle_config = JointConfig("TowerPro MG90S", "Positional", "Front Right Ankle", channel=8)
front_right_knee_config = JointConfig("TowerPro MG90S", "Positional", "Front Right knee", channel=9)
front_right_hip_config = JointConfig("TowerPro MG90S", "Positional", "Front Right Hip", channel=10)
front_right_knee_joint = Joint(front_right_knee_config)
front_right_ankle_joint = Joint(front_right_ankle_config)
front_right_hip_joint = Joint(front_right_hip_config)
front_right_leg = Leg(front_right_hip_joint, front_right_knee_joint, front_right_ankle_joint, Legs.FRONT_RIGHT)

rear_right_hip_config = JointConfig("TowerPro MG90S", "Positional", "Rear Right Hip", channel=14)
rear_right_knee_config = JointConfig("TowerPro MG90S", "Positional", "Rear Right knee", channel=13)
rear_right_ankle_config = JointConfig("TowerPro MG90S", "Positional", "Rear Right Ankle", channel=12)
rear_right_knee_joint = Joint(rear_right_knee_config)
rear_right_ankle_joint = Joint(rear_right_ankle_config)
rear_right_hip_joint = Joint(rear_right_hip_config)
rear_right_leg = Leg(rear_right_hip_joint, rear_right_knee_joint, rear_right_ankle_joint, Legs.REAR_RIGHT)


def on_obstacle_distance_measure_front(distance_in_cm: float):
    pass

front_obstacle_sensor_config : ObstacleSensorConfig = ObstacleSensorConfig("Ultra Sonic HC-SR04", "Front Obstacle Sensor", trig_gpio_pin=0, echo_gpio_pin=0)
front_obstacle_sensor:ObstacleSensor = ObstacleSensor(front_obstacle_sensor_config, on_obstacle_distance_measure_front)


spider:Spider = Spider(front_right_leg=front_right_leg,
                 front_left_leg=front_left_leg,
                 rear_right_leg=rear_right_leg,
                 rear_left_leg=rear_left_leg)

spider.startup()
time.sleep(20)
spider.hibernate()