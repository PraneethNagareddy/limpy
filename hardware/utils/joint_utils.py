import math

from time import sleep

def turn_and_await(joint, angle):
    pass

def turn(joint, angle):
    pass

def __get_servo_sleep_time_seconds(joint, angle) -> float:
    return (joint.joint_config.turn_time_per_degree_millis * angle) / 1000


def move_joint_with_sine_easing(targets, duration_sec, refresh_rate=0.02):
    """
    targets: List of (joint, start_angle, end_angle)
    duration: Total time for the move in seconds
    refresh_rate: Delay between updates (0.02 = 50Hz)
    """
    steps = int(duration_sec / refresh_rate)

    for i in range(steps + 1):
        # Calculate progress from 0.0 to 1.0
        progress = i / steps

        # Apply Sine Easing: slow start, fast middle, slow end
        # Formula: (1 - cos(progress * pi)) / 2
        easing_factor = (1 - math.cos(progress * math.pi)) / 2

        for joint, start, end in targets:
            # Calculate the eased angle
            current_angle = start + (end - start) * easing_factor
            joint.turn(current_angle)
            #kit.servo[channel].angle = current_angle

        sleep(refresh_rate)