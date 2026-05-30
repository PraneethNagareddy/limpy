import smbus
import time

# MPU6050 Register Addresses
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47

# MPU6050 I2C address (can be 0x68 or 0x69 depending on AD0 pin)
# Assuming 0x68 as a common default. If it doesn't work, try 0x69.
MPU6050_ADDR = 0x68

# Initialize I2C bus (0 for older Pis, 1 for newer ones like Pi 2, 3, 4)
# You might need to change this depending on your Raspberry Pi model
bus = smbus.SMBus(1) 

def MPU6050_init():
    """Initializes the MPU6050 sensor."""
    # Wake up MPU6050 (set PWR_MGMT_1 register to 0)
    bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)
    print("MPU6050 initialized.")

def read_word_2c(addr, reg):
    """Reads a 16-bit signed value from two 8-bit registers."""
    high = bus.read_byte_data(addr, reg)
    low = bus.read_byte_data(addr, reg + 1)
    value = (high << 8) + low
    if value >= 0x8000:
        return -((65535 - value) + 1)
    else:
        return value

def get_accel_data():
    """Reads and returns accelerometer data (X, Y, Z)."""
    accel_x = read_word_2c(MPU6050_ADDR, ACCEL_XOUT_H)
    accel_y = read_word_2c(MPU6050_ADDR, ACCEL_YOUT_H)
    accel_z = read_word_2c(MPU6050_ADDR, ACCEL_ZOUT_H)
    
    # Accelerometer sensitivity (for +/- 2g range, default)
    # 16384 LSB/g for +/- 2g range
    # To get values in g's, divide by this sensitivity scale factor.
    # You can configure sensitivity via ACCEL_CONFIG register (0x1C)
    accel_x_g = accel_x / 16384.0
    accel_y_g = accel_y / 16384.0
    accel_z_g = accel_z / 16384.0
    
    return accel_x_g, accel_y_g, accel_z_g

def get_gyro_data():
    """Reads and returns gyroscope data (X, Y, Z)."""
    gyro_x = read_word_2c(MPU6050_ADDR, GYRO_XOUT_H)
    gyro_y = read_word_2c(MPU6050_ADDR, GYRO_YOUT_H)
    gyro_z = read_word_2c(MPU6050_ADDR, GYRO_ZOUT_H)
    
    # Gyroscope sensitivity (for +/- 250 deg/s range, default)
    # 131 LSB/(deg/s) for +/- 250 deg/s range
    # To get values in deg/s, divide by this sensitivity scale factor.
    # You can configure sensitivity via GYRO_CONFIG register (0x1B)
    gyro_x_deg_s = gyro_x / 131.0
    gyro_y_deg_s = gyro_y / 131.0
    gyro_z_deg_s = gyro_z / 131.0
    
    return gyro_x_deg_s, gyro_y_deg_s, gyro_z_deg_s

def main():
    try:
        MPU6050_init()
        print("\n--- MPU6050 Gyro and Accelerometer Test ---")
        print(f"MPU6050 I2C Address: 0x{MPU6050_ADDR:X}")
        print("Reading sensor data (Ctrl+C to stop)...")

        while True:
            accel_x, accel_y, accel_z = get_accel_data()
            gyro_x, gyro_y, gyro_z = get_gyro_data()

            print(f"Accel (g): X={accel_x:.2f}, Y={accel_y:.2f}, Z={accel_z:.2f} | "
                  f"Gyro (deg/s): X={gyro_x:.2f}, Y={gyro_y:.2f}, Z={gyro_z:.2f}")
            
            time.sleep(0.1) # Read every 100ms

    except FileNotFoundError:
        print("Error: SMBus not found. Make sure 'python3-smbus' is installed and I2C is enabled.")
        print("You can install it with: sudo apt-get install python3-smbus")
        print("Enable I2C via 'sudo raspi-config' -> Interface Options -> I2C.")
    except OSError as e:
        if "121" in str(e): # Remote I/O error, often means device not found at address
            print(f"Error: MPU6050 not found at I2C address 0x{MPU6050_ADDR:X}.")
            print("Please check wiring and ensure the correct address (0x68 or 0x69) is used.")
            print("You can scan for I2C devices using 'i2cdetect -y 1'.")
        else:
            print(f"An I2C communication error occurred: {e}")
    except KeyboardInterrupt:
        print("\nMeasurement stopped by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
