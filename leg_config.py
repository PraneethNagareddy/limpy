from enums import Legs

class LegConfig:
    def __init__(self,
                 mount_angle,
                 position:Legs,
                 inverse_hip=False):
        self.mount_angle = mount_angle
        self.position = position
        self.inverse_hip = inverse_hip