import smbus2
import time
import math
from collections import deque

# MPU6050 default address
MPU6050_ADDR = 0x68

# MPU6050 registers
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

# Initialize I2C bus
bus = smbus2.SMBus(1)  # Use SMBus(0) for older Raspberry Pi models

# Wake up the MPU6050 (it starts in sleep mode)
bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)

def read_word(adr):
    """Read two bytes from the sensor and combine them into a signed 16-bit value."""
    high = bus.read_byte_data(MPU6050_ADDR, adr)
    low = bus.read_byte_data(MPU6050_ADDR, adr + 1)
    val = (high << 8) + low
    return val - 65536 if val >= 0x8000 else val  # Convert to signed

def calc_magnitude(a_x, a_y, a_z):
    magnitude = math.sqrt(a_x**2 + a_y**2 + a_z**2)
    return magnitude

def get_accel_gyro():
    """Read and return accelerometer and gyroscope data."""
    a_x = read_word(ACCEL_XOUT_H)/16384.0
    a_y = read_word(ACCEL_XOUT_H + 2)/16384.0
    a_z = read_word(ACCEL_XOUT_H + 4)/16384.0
    
    g_x = read_word(GYRO_XOUT_H)/131.0
    g_y = read_word(GYRO_XOUT_H + 2)/131.0
    g_z = read_word(GYRO_XOUT_H + 4)/131.0    

    magnitude = calc_magnitude(a_x, a_y, a_z)

    return a_x, a_y, a_z, g_x , g_y, g_z, magnitude
    # return {
    #     "accel": {"x": accel_x / 16384.0, "y": accel_y / 16384.0, "z": accel_z / 16384.0},
    #     "gyro": {"x": gyro_x / 131.0, "y": gyro_y / 131.0, "z": gyro_z / 131.0},
    # }
def calculate_roll_pitch(ax, ay, az):
    """Calculates roll and pitch angles in degrees."""
    roll = math.atan2(ay, az) * (180 / math.pi)
    pitch = math.atan2(-ax, math.sqrt(ay**2 + az**2)) * (180 / math.pi)
    return roll, pitch


# Main loop
if __name__ == "__main__":
    last_ax = deque([])
    last_ay = deque([])
    last_az = deque([])
    v_x = 0
    v_y = 0
    v_z = 0
    time_interval = 0.01 # in seconds

    while True:
        a_x, a_y, a_z, g_x, g_y, g_z, magnitude = get_accel_gyro()
        roll, pitch =calculate_roll_pitch(a_x, a_y, a_z)
        if len(last_ax) < 100:
            last_ax.append(a_x)
            last_ay.append(a_y)
            last_az.append(a_z)
        elif len(last_ax) == 100:
            old_x = last_ax.popleft()
            old_y = last_ay.popleft()
            old_z = last_az.popleft()
            v_x -= old_x * time_interval
            v_y -= old_y * time_interval
            v_z -= old_y * time_interval

            last_ax.append(a_x)
            last_ay.append(a_y)
            last_az.append(a_z)
        
        v_x += a_x * time_interval
        v_y += a_y * time_interval
        v_z += a_z * time_interval

        speed = calc_magnitude(v_x, v_y, v_z)
        
        # # Integrate acceleration to get velocity in each dimension
        # for a_x, a_y, a_z in zip(last_ax, last_ay, last_az):
        #     v_x += a_x * 0.01  # v_x(t) = v_x(t-1) + a_x * Δt
        #     v_y += a_y * 0.01  # v_y(t) = v_y(t-1) + a_y * Δt
        #     v_z += a_z * 0.01  # v_z(t) = v_z(t-1) + a_z * Δt
            
        #     # Calculate the speed (magnitude of velocity vector)
        #     speed = calc_magnitude(v_x, v_y, v_z)
        
        v_roll, v_pitch = calculate_roll_pitch(v_x, v_y, v_z)

        # print(f" Accel: ({a_x}, {a_y}, {a_z})")
        # print(f"accel Magnitude: {magnitude}")
        # print(f"roll(x): {roll}(y), pitch:{pitch}")
        # print("-------------Speed-----------")
        # print(f"speed: ({v_x}, {v_y}, {v_z})")
        print(f"speed magnitude: {speed}")
        print(f"roll(x): {v_roll}(y), pitch:{v_pitch}\n\n")

        # print(f"roll(x): {roll}(y), pitch:{pitch}\n\n")

        time.sleep(time_interval) # 10 milliseconds