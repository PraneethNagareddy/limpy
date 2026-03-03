from enum import Enum, auto

class Legs(Enum):
    FRONT_RIGHT = 1
    MIDDLE_RIGHT = 2
    REAR_RIGHT = 3
    REAR_LEFT = 4
    MIDDLE_LEFT = 5
    FRONT_LEFT = 6

class DistanceUnit(Enum):
    METER = 1
    CENTI_METER = 2
    MILLI_METER = 3