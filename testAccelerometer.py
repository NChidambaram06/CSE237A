import smbus2
import time
import math
from collections import deque
# import matplotlib.pyplot as plt
import random  #

# MPU6050 default address
MPU6050_ADDR = 0x68

# MPU6050 registers
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

ACCEL_THRESHOLD = 0.06  # Tune this value based on your sensor noise
ACC_ERROR_X = 0.03#0.00328#-5.493426
ACC_ERROR_Y= -0.1#0.030048#-3.049761
GYRO_ERROR_X = -2.930811
GYRO_ERROR_Y = 1.308454
GYRO_ERROR_Z = 0.787824
# AccErrorX: 0.000728
# AccErrorY: 0.030048
# GyroErrorX: -2.930811
# GyroErrorY: 1.308454
# GyroErrorZ: 0.787824
# AccErrorX: -5.493426
# AccErrorY: -3.049761
# GyroErrorX: -3.008769
# GyroErrorY: 1.299714
# GyroErrorZ: 0.793473
# Initialize I2C bus
bus = smbus2.SMBus(1)  # Use SMBus(0) for older Raspberry Pi models

# Wake up the MPU6050 (it starts in sleep mode)
bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)

def getMillis():
    millis = int(time.time() * 1000)
    return millis
def read_word(adr):
    """Read two bytes from the sensor and combine them into a signed 16-bit value."""
    high = bus.read_byte_data(MPU6050_ADDR, adr)
    low = bus.read_byte_data(MPU6050_ADDR, adr + 1)
    val = (high << 8) + low
    return val - 65536 if val >= 0x8000 else val  # Convert to signed

def calc_magnitude(a_x, a_y, a_z):
    magnitude = math.sqrt(a_x**2 + a_y**2 + a_z**2)
    return magnitude


def apply_deadband(value, threshold=ACCEL_THRESHOLD):
    return value if abs(value) > threshold else 0

def get_accel_gyro():
    """Read and return accelerometer and gyroscope data."""
    a_x = read_word(ACCEL_XOUT_H)/16384.0
    a_y = read_word(ACCEL_XOUT_H + 2)/16384.0
    a_z = read_word(ACCEL_XOUT_H + 4)/16384.0
    
    prev_time = getMillis()
    g_x = read_word(GYRO_XOUT_H)/131.0
    g_y = read_word(GYRO_XOUT_H + 2)/131.0
    g_z = read_word(GYRO_XOUT_H + 4)/131.0  
    curr_time = getMillis()
    elapsed_time = (curr_time - prev_time) * 1000

    print(f"Before correction: accel: ({a_x}, {a_y}, {a_z}), gyro: ({g_x}, {g_y}, {g_z})")

    a_x, a_y, a_z = get_corrected_accel(a_x, a_y, a_z)
    g_x, g_y, g_z = correct_gyro(g_x, g_y, g_z)  

    magnitude = calc_magnitude(a_x, a_y, a_z)

    return a_x, a_y, a_z, g_x , g_y, g_z, elapsed_time
    # return {
    #     "accel": {"x": accel_x / 16384.0, "y": accel_y / 16384.0, "z": accel_z / 16384.0},
    #     "gyro": {"x": gyro_x / 131.0, "y": gyro_y / 131.0, "z": gyro_z / 131.0},
    # }
def calculate_roll_pitch_yaw(ax, ay, az, gx, gy, gz, elapsedTime):
    """Calculates roll and pitch angles in degrees."""
    # roll = math.atan2(ay, az) * (180 / math.pi)
    # pitch = math.atan2(-ax, math.sqrt(ay**2 + az**2)) * (180 / math.pi)
    roll = (math.atan(ax / math.sqrt(ax**2 + az**2)) * (180 / math.pi)) - ACC_ERROR_X
    pitch = (math.atan(-ax / math.sqrt(ay**2 + az**2)) * (180 / math.pi)) - ACC_ERROR_Y

    gyroAngleX = gx * elapsedTime # deg/s * s = deg
    gyroAngleY = gy * elapsedTime
    roll = 0.96 * gyroAngleX + 0.04 *roll
    pitch = 0.96 * gyroAngleY + 0.04 * pitch
    yaw = gz * elapsedTime
    return roll, pitch, yaw

def correct_gyro(gx, gy, gz):
    correct_gx = gx - GYRO_ERROR_X 
    correct_gy = gy - GYRO_ERROR_Y
    correct_gz = gz - GYRO_ERROR_Z
    return correct_gx, correct_gy, correct_gz

def get_corrected_accel(ax, ay, az):
    """Apply bias correction and convert acceleration to m/s²."""
    ax_corrected = ax - ACC_ERROR_X
    ay_corrected = ay - ACC_ERROR_Y
    az_corrected = az  # No bias correction applied to Z-axis

    # Convert to m/s² (1g = 9.81 m/s²)
    # ax_m_s2 = ax_corrected * 9.81
    # ay_m_s2 = ay_corrected * 9.81
    # az_m_s2 = az_corrected * 9.81  # Assuming no significant error in Z

    return ax_corrected, ay_corrected, az_corrected

def calculate_IMU_error():
    """Calculate accelerometer and gyroscope bias by averaging 800 samples."""
    AccErrorX = 0
    AccErrorY = 0
    GyroErrorX = 0
    GyroErrorY = 0
    GyroErrorZ = 0

    # Read accelerometer values 800 times
    for _ in range(800):
        ax = read_word(ACCEL_XOUT_H) / 16384.0
        ay = read_word(ACCEL_XOUT_H + 2) / 16384.0
        az = read_word(ACCEL_XOUT_H + 4) / 16384.0

        # AccErrorX += math.atan(ay / math.sqrt(ax**2 + az**2)) * (180 / math.pi)
        # AccErrorY += math.atan(-ax / math.sqrt(ay**2 + az**2)) * (180 / math.pi)
        AccErrorX += ax
        AccErrorY += ay
        time.sleep(0.002)  # Small delay for stability

    AccErrorX /= 800
    AccErrorY /= 800

    # Read gyroscope values 800 times
    for _ in range(800):
        gx = read_word(GYRO_XOUT_H) / 131.0
        gy = read_word(GYRO_XOUT_H + 2) / 131.0
        gz = read_word(GYRO_XOUT_H + 4) / 131.0

        GyroErrorX += gx
        GyroErrorY += gy
        GyroErrorZ += gz
        time.sleep(0.002)  # Small delay for stability

    GyroErrorX /= 800
    GyroErrorY /= 800
    GyroErrorZ /= 800

    # Print the error values
    print(f"AccErrorX: {AccErrorX:.6f}")
    print(f"AccErrorY: {AccErrorY:.6f}")
    print(f"GyroErrorX: {GyroErrorX:.6f}")
    print(f"GyroErrorY: {GyroErrorY:.6f}")
    print(f"GyroErrorZ: {GyroErrorZ:.6f}")

    return AccErrorX, AccErrorY, GyroErrorX, GyroErrorY, GyroErrorZ

# Main loop
if __name__ == "__main__":
    last_ax = deque([])
    last_ay = deque([])
    last_az = deque([])
    vxs = []
    vys=[]
    vzs=[]
    v_x = 0
    v_y = 0
    v_z = 0
    time_interval = 0.01 # in seconds
    n =0

    # calculate_IMU_error()

    while n < 100:
        a_x, a_y, a_z, g_x, g_y, g_z, elapsed_time = get_accel_gyro()
        a_x = apply_deadband(a_x)
        a_y = apply_deadband(a_y)
        a_z = apply_deadband(a_z)

        # roll, pitch, yaw =calculate_roll_pitch_yaw(a_x, a_y, a_z, g_x, g_y, g_z, elapsed_time)
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

        if abs(a_x) < 0.02 and abs(a_y) < 0.02 and abs(a_z) < 0.02:
            v_x, v_y, v_z = 0, 0, 0
        
        # velocity in cm/s
        v_x += a_x * time_interval
        v_y += a_y * time_interval
        v_z += a_z * time_interval

        vxs.append(v_x)
        vys.append(v_y)
        vzs.append(v_z)


        speed = calc_magnitude(v_x, v_y, 0)
        speed_angle_xy = 0
        if v_x != 0:
            speed_angle_xy =(math.atan(v_y/ v_x) * (180 / math.pi))
        elif v_y > 0:
            speed_angle_xy = 90
        else:
            speed_angle_xy = 270
        # # Integrate acceleration to get velocity in each dimension
        # for a_x, a_y, a_z in zip(last_ax, last_ay, last_az):
        #     v_x += a_x * 0.01  # v_x(t) = v_x(t-1) + a_x * Δt
        #     v_y += a_y * 0.01  # v_y(t) = v_y(t-1) + a_y * Δt
        #     v_z += a_z * 0.01  # v_z(t) = v_z(t-1) + a_z * Δt
            
        #     # Calculate the speed (magnitude of velocity vector)
        #     speed = calc_magnitude(v_x, v_y, v_z)
        
        # v_roll, v_pitch = calculate_roll_pitch_yaw(v_x, v_y, v_z, 0, 0, 0, 0)

        # print(f" Accel: ({a_x}, {a_y}, {a_z})")
        # print(f"accel Magnitude: {magnitude}")
        # print(f"roll(x): {roll}(y), pitch:{pitch}")
        # print("-------------Speed-----------")
        # print(f"speed: ({v_x}, {v_y}, {v_z})")
        # print(f"speed xy magnitude: {speed}")
        # print(f"xy angle of speed: {speed_angle_xy}\n\n")
        # print(f"roll(x): {v_roll}(y), pitch:{v_pitch}\n\n")

        # print(f"roll(x): {roll}(y), pitch:{pitch}\n\n")

        time.sleep(time_interval) # 10 milliseconds
        n += 1
    print(vxs)
    print(vys)
    
    # # Simulate accelerometer data (replace with actual readings from your sensor)
    # time_data = []
    # for i in range(len(last_ax)):
    #     time_data.append(i)

    # # Plotting acceleration data
    # plt.figure(figsize=(10, 6))

    # # Plot Acceleration on X, Y, and Z axes
    # plt.plot(time_data, last_ax, label='Accel X', color='r')
    # plt.plot(time_data, last_ay, label='Accel Y', color='g')
    # plt.plot(time_data, last_az, label='Accel Z', color='b')

    # # Labels and title
    # plt.xlabel('Time (s)')
    # plt.ylabel('Acceleration (g)')
    # plt.title('Accelerometer Data: X, Y, Z')

    # # Show legend
    # plt.legend()

    # # Display the plot
    # plt.grid(True)
    # plt.show()

    # time_v = []
    # for i in range(len(vxs)):
    #     time_v.append(i)
    
    #  # Plotting acceleration data
    # plt.figure(figsize=(10, 6))

    # # Plot Acceleration on X, Y, and Z axes
    # plt.plot(time_v, vxs, label='Speed X', color='r')
    # plt.plot(time_v, vys, label='Speed Y', color='g')
    # plt.plot(time_v, vzs, label='Speed Z', color='b')

    # # Labels and title
    # plt.xlabel('Time (s)')
    # plt.ylabel('Speed (g)')
    # plt.title('Speed Data: X, Y, Z')

    # # Show legend
    # plt.legend()

    # # Display the plot
    # plt.grid(True)
    # plt.show()