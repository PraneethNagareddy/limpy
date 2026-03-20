from enums import Legs

class LegConfig:
    def __init__(self,
                 mount_angle,
                 position:Legs,
                 ankle_trim_angle:float=0.0,
                 knee_trim_angle:float=0.0,
                 hip_trim_angle:float=0.0,
                 inverse_hip=False):
        self.mount_angle = mount_angle
        self.position = position
        self.inverse_hip = inverse_hip
        self.ankle_trim_angle = ankle_trim_angle
        self.knee_trim_angle = knee_trim_angle
        self.hip_trim_angle = hip_trim_angle