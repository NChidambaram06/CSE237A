import os
import gpiod
from gpiozero import LED, DistanceSensor
import time
import threading
from pynput.mouse import Button, Controller
import smbus2
import math
from collections import deque
# from testAccelerometer import * 
from camera_rasp_pi import *

# GPIO chip and lines
CHIP_NAME = "/dev/gpiochip0"
PIN_LEFT = 17
PIN_RIGHT = 27
PIN_SCROLL = 22
PIN_PICK = 23
#DIP two-color LED (Dual In-line Package)
PIN_DIP_RED = LED(20)
PIN_DIP_GRN = LED(21)
#SMD RGB LED (Surface Mount Device)
PIN_SMD_RED = LED(26)
PIN_SMD_GRN = LED(19)
PIN_SMD_BLU = LED(13)
#Ultrasonic
PIN_TRIGGER = 6
PIN_ECHO = 5
# Accelerometer/Gyroscope
MPU_ADDR = 0x68
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

ACCEL_THRESHOLD = 0.1  # Tune this value based on your sensor noise
ACC_ERROR_X = 0.03#0.00328#-5.493426
ACC_ERROR_Y= -0.03#0.030048#-3.049761
GYRO_ERROR_X = -2.930811
GYRO_ERROR_Y = 1.308454
GYRO_ERROR_Z = 0.787824
# AccErrorX: 0.000728
# run body_functions every 0.01 seconds (10 milliseconds)
TIME_INTERVAL = 0.01
PIXEL_MOUSE_MOVE = 300

mouse = Controller()
bus = smbus2.SMBus(1)
bus.write_byte_data(MPU_ADDR, PWR_MGMT_1, 0) # wake up the MPU6050

class SharedVariable:
    def __init__(self):
        self.bProgramExit = 0
        self.right = 0
        self.left = 0
        self.scroll = 0
        self.pick = 1
        self.rightLastClickTime = self.get_millis()
        self.leftLastClickTime = self.get_millis()
        self.scrollLastClick = self.get_millis()
        self.pickLastClick = self.get_millis()
        self.scroll_speed = 1
        self.scroll_dir = -1
        self.last_ax = deque([])
        self.last_ay = deque([])
        self.last_az = deque([])
        self.vx = 0
        self.vy = 0
        self.vz = 0
        self.n = 0
    
    def get_millis(self):
        return int(time.time() * 1000)


def read_gpio_value(line):
    with gpiod.Chip(CHIP_NAME) as chip:
        # gpio_line = chip.get_line(line)
        chip.request(consumer="sensor", type=gpiod.LINE_REQ_DIR_IN)
        return gpio_line.get_value()
        
def write_gpio_value(line, val):
    with gpiod.Chip(CHIP_NAME) as chip:
        gpio_line = chip.get_line(line)
        gpio_line.request(consumer="sensor", type=gpiod.LINE_REQ_DIR_OUT)
        gpio_line.set_value(val)

def body_right(sv):
    if sv.pick == 1:
        curr_time = sv.get_millis()
        if read_gpio_value(PIN_RIGHT) and (curr_time - sv.rightLastClickTime) > 400:
            print("right click")
            sv.right = 1
            mouse.click(Button.right, 1)
            sv.rightLastClickTime = sv.get_millis()
        elif (curr_time - sv.rightLastClickTime) > 400:
            sv.right = 0

def body_left(sv):
    if sv.pick == 1:
        curr_time = sv.get_millis()
        if read_gpio_value(PIN_LEFT) and (curr_time - sv.leftLastClickTime) > 400:
            print("left click")
            sv.left = 1
            mouse.click(Button.left, 1)
            sv.leftLastClickTime = sv.get_millis()
        elif (curr_time - sv.leftLastClickTime) > 400:
            sv.left = 0

def body_scroll(sv):
    if sv.pick == 1:
        curr_time = sv.get_millis()
        if read_gpio_value(PIN_SCROLL) and (curr_time - sv.scrollLastClick) > 0:
            print("scroll click")
            sv.scroll = 1
            sv.scrollLastClick = sv.get_millis()
            mouse.scroll(0, sv.scroll_speed*sv.scroll_dir)
        elif (curr_time - sv.scrollLastClick) > 0:
            if sv.scroll == 1:
                print("stop scroll click")
            sv.scroll = 0

def body_pick(sv):
    curr_time = sv.get_millis()
    if read_gpio_value(PIN_PICK) and (curr_time - sv.pickLastClick) > 400:
        if sv.pick == 0:
            print("pick up mouse")
            sv.pick = 1
            sv.pickLastClick = sv.get_millis()
        else:
            print("drop mouse")
            sv.pick = 0
            sv.pickLastClick = sv.get_millis()
            
def body_twocolor(sv):
    if (sv.pick == 1):
        PIN_DIP_RED.off()
        PIN_DIP_GRN.on()
    else :
        PIN_DIP_RED.on()
        PIN_DIP_GRN.off()

def body_rgbcolor(sv):
    if (sv.pick == 1) and (sv.left == 1):
        PIN_SMD_RED.on()
        PIN_SMD_GRN.on()
        PIN_SMD_BLU.on()
    else:
        PIN_SMD_RED.off()
        PIN_SMD_GRN.off()
        PIN_SMD_BLU.off()

def body_ultra(sv):
    distance = sensor = DistanceSensor(echo=PIN_ECHO, trigger=PIN_TRIGGER).distance * 100
    if distance < 7 or distance > 17:
        sv.scroll_speed = 1
    else:
        print(f"The distance is: {distance:.2f} cm")
        dist_10 = distance - 7
        sv.scroll_speed = int(10/dist_10)
        
    
    # Pause between the individual measurements
    time.sleep(.25)

def read_sensor_data():
    # Read accelerometer and gyroscope data (14 bytes starting from address 0x3B)
    data = bus.read_i2c_block_data(MPU_ADDR, 0x3B, 14)
    
    # Combine the high and low bytes for X, Y, Z accelerometer values
    AcX = (data[0] << 8) + data[1]
    AcY = (data[2] << 8) + data[3]
    AcZ = (data[4] << 8) + data[5]
    
    return AcX, AcY, AcZ

def calculate_angles(AcX, AcY, AcZ):
    minVal = 265
    maxVal = 402
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

def body_tilt(sv):
    AcX, AcY, AcZ = read_sensor_data()
    x, y, z = calculate_angles(AcX, AcY, AcZ)
    if z > 35 and z < 90:
        print(f"tilted down, z: {z}")
        sv.scroll_dir = -1
    elif z < 15 or z >= 90:
        print(f"tilted up, z: {z}")
        sv.scroll_dir = 1

'''
def body_speed(sv):
    a_x, a_y, a_z, g_x, g_y, g_z, elapsed_time = get_accel_gyro()
    a_x = apply_deadband(a_x)
    a_y = apply_deadband(a_y)
    a_z = apply_deadband(a_z)

    max_time_counts = 50
    if len(sv.last_ax) < max_time_counts:
        sv.last_ax.append(a_x)
        sv.last_ay.append(a_y)
        sv.last_az.append(a_z)
    elif len(sv.last_ax) == max_time_counts:
        old_x = sv.last_ax.popleft()
        old_y = sv.last_ay.popleft()
        old_z = sv.last_az.popleft()
        sv.vx -= old_x * TIME_INTERVAL
        sv.vy -= old_y * TIME_INTERVAL
        sv.vz -= old_z * TIME_INTERVAL

        sv.last_ax.append(a_x)
        sv.last_ay.append(a_y)
        sv.last_az.append(a_z)

    if abs(a_x) < ACCEL_THRESHOLD and abs(a_y) < ACCEL_THRESHOLD:
        sv.v_x, sv.v_y, sv.v_z = 0, 0, 0
    

    # velocity in g/s
    sv.vx += a_x * TIME_INTERVAL
    sv.vy += a_y * TIME_INTERVAL
    sv.vz += a_z * TIME_INTERVAL
    if sv.n % 10 == 0:
        print(f"moving mouse:x{PIXEL_MOUSE_MOVE * sv.vx}, y {PIXEL_MOUSE_MOVE * (-1) * sv.vy}")
        mouse.move(PIXEL_MOUSE_MOVE * sv.vx, PIXEL_MOUSE_MOVE * sv.vy)
    sv.n += 1
'''
def body_mouse(sv):
    print("Move mouse (IS STUB RIGHT NOW)")
    xPixelLoc, yPixelLoc = getXY()
    mouse.position = (xPixelLoc, yPixelLoc)

# def sensor_thread(func, sv):
#     while not sv.bProgramExit:
#         func(sv)
#         time.sleep(TIME_INTERVAL)  # Small delay to reduce CPU usage

def sensor_thread(func, sv, core_id):
    """Runs the given function as a thread and pins it to a specific core."""
    def target():
        os.sched_setaffinity(0, {core_id})  # Set thread affinity to core_id
        while not sv.bProgramExit:
            func(sv)
            time.sleep(TIME_INTERVAL)

    t = threading.Thread(target=target)
    t.start()
    return t

if __name__ == "__main__":
    sv = SharedVariable()

    '''threads = [
        threading.Thread(target=sensor_thread, args=(body_right, sv)),
        threading.Thread(target=sensor_thread, args=(body_left, sv)),
        threading.Thread(target=sensor_thread, args=(body_scroll, sv)),
        threading.Thread(target=sensor_thread, args=(body_pick, sv)),
        threading.Thread(target=sensor_thread, args=(body_rgbcolor, sv)),
        threading.Thread(target=sensor_thread, args=(body_twocolor, sv)),
        threading.Thread(target=sensor_thread, args=(body_ultra, sv)),
        threading.Thread(target=sensor_thread, args=(body_tilt, sv)),
        #threading.Thread(target=sensor_thread, args=(body_speed, sv))
    ]'''
    core_0_threads = [
        sensor_thread(body_right, sv, 0),
        sensor_thread(body_left, sv, 0),
        sensor_thread(body_scroll, sv, 0),
        sensor_thread(body_pick, sv, 0),
        sensor_thread(body_rgbcolor, sv, 0),
        sensor_thread(body_twocolor, sv, 0),
        sensor_thread(body_ultra, sv, 0),
        sensor_thread(body_tilt, sv, 0),
    ]

    body_mouse_thread = sensor_thread(body_mouse, sv, 1)
    
    # for t in threads:
    #     t.start()
    
    try:
        while not sv.bProgramExit:
            time.sleep(1)
    except KeyboardInterrupt:
        sv.bProgramExit = 1
        
    # Join threads
    for t in core_0_threads + [body_mouse_thread]:
        t.join()
    
    cv2.destroyAllWindows()
    camera.stop()
    
    print("Program finished.")
