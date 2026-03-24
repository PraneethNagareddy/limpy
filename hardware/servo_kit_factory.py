from adafruit_servokit import ServoKit

class ServoKitFactory(object):
    @staticmethod
    def get_servo_kit(i2c_address):
        servo_kits = {
            0x40: ServoKit(channels=16, address=0x40),
            0x41: ServoKit(channels=16, address=0x41)
        }
        return servo_kits.get(i2c_address)