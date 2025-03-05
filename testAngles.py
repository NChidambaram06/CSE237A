import smbus
import math
import time

# MPU6050 I2C address
MPU_ADDR = 0x68

# Accelerometer and Gyroscope data variables
AcX = 0
AcY = 0
AcZ = 0

TILT_THRESHOLD = 30

minVal = 265
maxVal = 402

# Initialize the I2C bus
bus = smbus.SMBus(1)  # For Raspberry Pi (use 1 for newer models, 0 for older ones)

# Wake up the MPU6050
bus.write_byte_data(MPU_ADDR, 0x6B, 0)

def read_sensor_data():
    # Read accelerometer and gyroscope data (14 bytes starting from address 0x3B)
    data = bus.read_i2c_block_data(MPU_ADDR, 0x3B, 14)
    
    # Combine the high and low bytes for X, Y, Z accelerometer values
    AcX = (data[0] << 8) + data[1]
    AcY = (data[2] << 8) + data[3]
    AcZ = (data[4] << 8) + data[5]
    
    return AcX, AcY, AcZ

def calculate_angles(AcX, AcY, AcZ):
    # Map the accelerometer data to -90 to 90 degrees
    xAng = map_value(AcX, minVal, maxVal, -90, 90)
    yAng = map_value(AcY, minVal, maxVal, -90, 90)
    zAng = map_value(AcZ, minVal, maxVal, -90, 90)

    # Calculate angles using atan2 function
    x = math.degrees(math.atan2(-yAng, -zAng) + math.pi)
    y = math.degrees(math.atan2(-xAng, -zAng) + math.pi)
    z = math.degrees(math.atan2(-yAng, -xAng) + math.pi)
    
    return x, y, z

def map_value(value, in_min, in_max, out_min, out_max):
    # Map a value from one range to another
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def detect_tilt(AcZ):
    if AcZ > 35:
        return "Tilted Down"
    elif AcZ < 15:
        return "Tilted Up"
    else:
        return "Not Tilted"

def main():
    while True:
        AcX, AcY, AcZ = read_sensor_data()
        x, y, z = calculate_angles(AcX, AcY, AcZ)
        
        # Print the results
        print(f"AngleX= {x:.2f}")
        print(f"AngleY= {y:.2f}")
        print(f"AngleZ= {z:.2f}")

        # Detect tilt
        tilt_status = detect_tilt(z)
        print(f"Tilt Status: {tilt_status}")
        
        print("-----------------------------------------")
        
        # Delay between readings
        time.sleep(0.4)

if __name__ == "__main__":
    main()