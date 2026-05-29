from abc import ABC, abstractmethod
from core.feedback_enums import FeedbackStatus

class FeedbackCommunicator(ABC):
    @abstractmethod
    def communicate_startup(self, is_smooth: bool = True):
        """Communicates the robot's startup sequence."""
        pass

    @abstractmethod
    def communicate_movement(self, is_moving: bool):
        """Communicates whether the robot is currently moving or idle."""
        pass

    @abstractmethod
    def communicate_status(self, status: FeedbackStatus):
        """Communicates a specific feedback status using LED combinations."""
        pass

    @abstractmethod
    def shutdown(self):
        """Performs cleanup for the communicator."""
        pass
