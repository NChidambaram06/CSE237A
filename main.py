import gpiod
from gpiozero import LED, DistanceSensor
import time
import threading
from pynput.mouse import Button, Controller

mouse = Controller()

# GPIO chip and lines
CHIP_NAME = "/dev/gpiochip0"
PIN_LEFT = 17
PIN_RIGHT = 27
PIN_SCROLL = 22
PIN_PICK = 23
#DIP two-color LED (Dual In-line Package)
PIN_DIP_RED = LED(2)
PIN_DIP_GRN = LED(3)
#SMD RGB LED (Surface Mount Device)
PIN_SMD_RED = LED(26)
PIN_SMD_GRN = LED(19)
PIN_SMD_BLU = LED(13)
#Ultrasonic
PIN_TRIGGER = 6
PIN_ECHO = 5

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
    
    def get_millis(self):
        return int(time.time() * 1000)


def read_gpio_value(line):
    with gpiod.Chip(CHIP_NAME) as chip:
        gpio_line = chip.get_line(line)
        gpio_line.request(consumer="sensor", type=gpiod.LINE_REQ_DIR_IN)
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
            rate = int(1/sv.scroll_speed)
            if rate == 0:
                rate = 1
            mouse.scroll(0, rate)
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
        sv.scroll_speed = dist_10
        
    
    # Pause between the individual measurements
    time.sleep(.25)


def sensor_thread(func, sv):
    while not sv.bProgramExit:
        func(sv)
        time.sleep(0.01)  # Small delay to reduce CPU usage

if __name__ == "__main__":
    sv = SharedVariable()
    
    threads = [
        threading.Thread(target=sensor_thread, args=(body_right, sv)),
        threading.Thread(target=sensor_thread, args=(body_left, sv)),
        threading.Thread(target=sensor_thread, args=(body_scroll, sv)),
        threading.Thread(target=sensor_thread, args=(body_pick, sv)),
        threading.Thread(target=sensor_thread, args=(body_rgbcolor, sv)),
        threading.Thread(target=sensor_thread, args=(body_twocolor, sv)),
        threading.Thread(target=sensor_thread, args=(body_ultra, sv))
    ]
    
    for t in threads:
        t.start()
    
    try:
        while not sv.bProgramExit:
            time.sleep(1)
    except KeyboardInterrupt:
        sv.bProgramExit = 1
        
    for t in threads:
        t.join()
    
    print("Program finished.")
