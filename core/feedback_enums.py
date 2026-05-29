from enum import Enum

class FeedbackStatus(Enum):
    # General Robot States
    ROBOT_IDLE = "ROBOT_IDLE"
    ROBOT_MOVING = "ROBOT_MOVING"
    ROBOT_TURNING = "ROBOT_TURNING"
    ROBOT_STEPPING = "ROBOT_STEPPING"
    ROBOT_ERROR = "ROBOT_ERROR"
    ROBOT_SHUTDOWN = "ROBOT_SHUTDOWN"
    ROBOT_HIBERNATING = "ROBOT_HIBERNATING"
    # Add more specific statuses as needed for your 9 combinations
    CUSTOM_STATUS_1 = "CUSTOM_STATUS_1"
    CUSTOM_STATUS_2 = "CUSTOM_STATUS_2"
