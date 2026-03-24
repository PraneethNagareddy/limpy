class JointConfig:
    def __init__(self,
                 servo_name,
                 servo_type,
                 common_name,
                 i2c_address,
                 min_angle=0,
                 max_angle=180,
                 default_angle=0,
                 turn_time_per_degree_millis=1.6,
                 channel=-1,
                 pulse_width_min = 450,
                 pulse_width_max = 2600):
        self.channel = channel
        self.servo_name = servo_name
        self.servo_type = servo_type
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.common_name = common_name
        self.default_angle = default_angle
        self.turn_time_per_degree_millis = turn_time_per_degree_millis
        self.pulse_width_min = pulse_width_min
        self.pulse_width_max = pulse_width_max
        self.i2c_address = i2c_address