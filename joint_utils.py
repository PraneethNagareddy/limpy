
def turn_and_await(joint, angle):
    pass

def turn(joint, angle):
    pass

def __get_servo_sleep_time_seconds(joint, angle) -> float:
    return (joint.joint_config.turn_time_per_degree_millis * angle) / 1000