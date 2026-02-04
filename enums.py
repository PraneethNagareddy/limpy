from enum import Enum, auto

class Legs(Enum):
    FRONT_LEFT = 1
    FRONT_RIGHT = 2
    REAR_LEFT = 3
    REAR_RIGHT = 4

class DistanceUnit(Enum):
    METER = 1
    CENTI_METER = 2
    MILLI_METER = 3