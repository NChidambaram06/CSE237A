import os
import gpiod
from gpiod.line import Direction, Value
from gpiozero import LED, DistanceSensor
import time
import threading
from pynput.mouse import Button, Controller
import smbus2
import math
from cam2 import *

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

# run body_functions every 0.01 seconds (10 milliseconds)
TIME_INTERVAL = 0.01

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
        self.held = 0
        self.rightLastClickTime = self.get_millis()
        self.leftLastClickTime = self.get_millis()
        self.scrollLastClick = self.get_millis()
        self.pickLastClick = self.get_millis()
        self.scroll_speed = 1
        self.scroll_dir = -1
        self.lastUltraTime = self.get_millis()
    
    def get_millis(self):
        return int(time.time() * 1000)


def read_gpio_value(line): # read gpio pin value
    with gpiod.request_lines(CHIP_NAME, consumer="sensor", config={line: gpiod.LineSettings(direction = Direction.INPUT)}) as request:
        return request.get_value(line)
        
def write_gpio_value(line, val): # write to gpio pin
    with gpiod.request_lines(CHIP_NAME, consumer="sensor", config={line: gpiod.LineSettings(direction = Direction.OUTPUT)}) as request:
        return request.set_value(line, val)

def body_right(sv):
    if sv.pick == 1: # if mouse picked up
        curr_time = sv.get_millis()
        if read_gpio_value(PIN_RIGHT) and (curr_time - sv.rightLastClickTime) > 400: # if touch sensor 2 touched and last click was more than 400 ms ago, perform right click
            print("right click")
            sv.right = 1
            mouse.click(Button.right, 1)
            sv.rightLastClickTime = sv.get_millis()
        elif (curr_time - sv.rightLastClickTime) > 400: # after 400 ms, set right click state to off
            sv.right = 0

def body_left(sv):
    if sv.pick == 1: # if mouse picked up
        curr_time = sv.get_millis()
        if read_gpio_value(PIN_LEFT) and (curr_time - sv.leftLastClickTime) > 400: # if touch sensor 1 touched and last click was more than 400 ms ago
            print("left click")
            if sv.left == 1: # if button is held, button press to allow for click and hold (drag functionality enabled)
                sv.held = 1
                mouse.press(Button.left)
            else: # if button is tapped, perform normal left click
                mouse.click(Button.left, 1)
            sv.left = 1
            sv.leftLastClickTime = sv.get_millis()
        elif (curr_time - sv.leftLastClickTime) > 400: # after 400 ms if touch sensor not touched turn off left click state
            sv.left = 0
            if sv.held == 1:
                mouse.release(Button.left)
            sv.held = 0

def body_scroll(sv):
    if sv.pick == 1: # if mouse picked up
        curr_time = sv.get_millis()
        if read_gpio_value(PIN_SCROLL) and (curr_time - sv.scrollLastClick) > 100: # if touch sensor 3 touched, with delay of 100 ms between checks, scroll in appropriate direction
            print("scroll click")
            sv.scroll = 1
            sv.scrollLastClick = sv.get_millis()
            mouse.scroll(0, sv.scroll_speed*sv.scroll_dir) # scroll in direction and speed based on actuators (ultrasonic sensor control speed & accelerometer/gyroscope controls direction)
        elif (curr_time - sv.scrollLastClick) > 400: # if not touched after 400 ms, turn off scroll state
            if sv.scroll == 1:
                print("stop scroll click")
            sv.scroll = 0

def body_pick(sv):
    curr_time = sv.get_millis()
    if read_gpio_value(PIN_PICK) and (curr_time - sv.pickLastClick) > 400: # if touch sensor 4 touched, check with delay of 400 ms, toggle mouse pick up/dropped
        if sv.pick == 0:
            print("pick up mouse")
            sv.pick = 1 # set mouse state to picked up
            sv.pickLastClick = sv.get_millis()
        else:
            print("drop mouse")
            sv.pick = 0 # set mouse state to dropped (turns off all mouse functionality)
            sv.pickLastClick = sv.get_millis()
            
def body_twocolor(sv):
    if (sv.pick == 1): # if mouse picked up, display green color
        PIN_DIP_RED.off()
        PIN_DIP_GRN.on()
    else : # if mouse dropped, display red color
        PIN_DIP_RED.on()
        PIN_DIP_GRN.off()

def body_rgbcolor(sv):
    if (sv.pick == 1) and (sv.left == 1): # if mouse picked up and left click performed, turn on SMD RGB and make it white 
        PIN_SMD_RED.on()
        PIN_SMD_GRN.on()
        PIN_SMD_BLU.on()
    else: # if left click not performed, turn off SMD RGB LED
        PIN_SMD_RED.off()
        PIN_SMD_GRN.off()
        PIN_SMD_BLU.off()

def body_ultra(sv):
    currTime = sv.get_millis()
    if (currTime - sv.lastUltraTime) > 400 and sv.scroll == 0 and sv.pick == 1: # if not currently scrolling and mouse picked up (check with delay of 400ms)
        distance = DistanceSensor(echo=PIN_ECHO, trigger=PIN_TRIGGER).distance * 100 # get distance and convert to cm
        if distance < 7 or distance > 17: # if not detected in a good distance, set scroll speed to default of 1 
            sv.scroll_speed = 1
        else: # if detected distance in range it reads well in, use it to adjust the scroll speed (closer is faster, farther is slower)
            print(f"The distance is: {distance:.2f} cm")
            dist_10 = distance - 7
            sv.scroll_speed = int(10/dist_10)
        sv.lastUltraTime = currTime
        

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
    if sv.pick == 1 and sv.scroll == 1: # if mouse picked up and currently scrolling, check tilt to control direction of scroll
        curr_time = sv.get_millis()
        if (curr_time - sv.scrollLastClick) > 400: # if scroll not clicked recently (last 400 ms), turn off scroll
            sv.scroll = 0
        else: # if scroll clicked recently (less than 400 ms), calculate tilt to control scroll direction
            AcX, AcY, AcZ = read_sensor_data()
            x, y, z = calculate_angles(AcX, AcY, AcZ)
            if z > 35 and z < 90:
                print(f"tilted down, z: {z}")
                sv.scroll_dir = -1
            elif z < 15 or z >= 90:
                print(f"tilted up, z: {z}")
                sv.scroll_dir = 1


def body_mouse(sv):
    if sv.pick == 1: # if mouse picked up, move mouse based on hand position
        xPixelLoc, yPixelLoc = getXY() # get hand position from camera
        if xPixelLoc != -1: # if hand position is detected, move mouse
            mouse.position = (xPixelLoc, yPixelLoc)

def sensor_thread(func, sv, core_id):
    # Runs the given function as a thread on the specified
    def target():
        os.sched_setaffinity(0, {core_id})  # Set thread to specified core_id
        while not sv.bProgramExit: # run threads in a loop with a delay of time interval
            func(sv)
            time.sleep(TIME_INTERVAL)
    
    # run the thread
    t = threading.Thread(target=target)
    t.start()
    return t

if __name__ == "__main__":
    sv = SharedVariable()

    # initialize threads to run on core 0
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

    body_mouse_thread = sensor_thread(body_mouse, sv, 1) # run mouse movement thread on core 1, it performs computer vision hand tracking

    # keep programming running till program exited
    try:
        while not sv.bProgramExit:
            time.sleep(1)
    except KeyboardInterrupt:
        sv.bProgramExit = 1
        
    # Join threads
    for t in core_0_threads + [body_mouse_thread]:
        t.join()
    
    # destory window created by camera and turn off camera
    cv2.destroyAllWindows()
    camera.stop()
    
    print("Program finished.")
