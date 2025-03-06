# Motion Controlled Gestural Mouse

## Overview
This project implements a gesture-based mouse control system using a Raspberry Pi 5 as the base. The system allows users to control a computer's mouse cursor and perform actions like clicking, scrolling, and picking up/dropping the mouse using hand gestures and touch sensors. The project uses MediaPipe for hand tracking, OpenCV for image processing, and GPIO for interfacing with sensors and LEDs.

---

## Features
1. **Hand Tracking**:
   - Tracks the user's hand using a camera and maps the hand's position to the mouse cursor on the screen.
   - Uses MediaPipe for hand landmark detection.

2. **Mouse Actions**:
   - **Left Click**: Triggered by touch sensor.
   - **Right Click**: Triggered by second touch sensor.
   - **Scroll**: Controlled by tilting the device or using an ultrasonic sensor as a speed gauge, triggered by a third touch sensor.
   - **Pick/Drop Mouse**: Toggles the mouse control on/off using a fourth touch sensor.

3. **Visual Feedback** - alerts for successful functionality:
   - **DIP Two-Color LED**: Indicates whether the mouse is picked up (green) or dropped (red).
   - **SMD RGB LED**: Lights up when the mouse is picked up and a left click is performed.

4. **Ultrasonic Sensor**:
   - Measures the distance of the speed gauge from the sensor to control the scroll speed.

5. **Accelerometer/Gyroscope**:
   - Detects hand tilt to control the scroll direction (up or down).

6. **Multi-Core Processing**:
   - The program uses threading and 2 CPUs to optimize performance by assigning the processor-heavy hand tracking program to a single core and all of the other threads to a second core..

---

## Hardware
- **Raspberry Pi 5** (with GPIO pins, 2 cores available)
- **Camera Module** (Raspberry Pi Camera Module V2)
   - CSI FPC Flexible Cable for Raspberry Pi 5,  22Pin to 15Pin
- **Ultrasonic Sensor** (HC-SR04)
- **Accelerometer/Gyroscope** (MPU6050)
- **Touch Sensors** (TTP223B Digital Capacitivev Touch Sensor Switch Module) x 4
- **LEDs**:
  - 2-Color DIP LED (KY-011)
  - 3-Color SMD RGB LED (KY-009)
- **Resistors** (for LEDs)
- **Jumper Wires** and **Breadboard**
- **Glove** (Palm and Fingers exposed (only fingertips on non-thumb fingers covered))

---

## Software Requirements
- **Python 3**
- **Libraries**:
  - `mediapipe` (for hand tracking)
  - `opencv-python` (for image processing)
  - `pyautogui` (for mouse control)
  - `gpiod` (for GPIO control)
  - `gpiozero` (for LED and ultrasonic sensor control)
  - `smbus2` (for I2C communication with MPU6050)
  - `pynput` (for mouse control)
  - `picamera2` (for camera interfacing)

---

## Setup Instructions

### 1. Install Dependencies
Install the required Python libraries:
```bash
pip install mediapipe opencv-python pyautogui gpiod gpiozero smbus2 pynput picamera2
```

### 2. Connect Hardware
- Connect the **camera module** to the Raspberry Pi using the CSI conversion cable.
- Connect the **ultrasonic sensor** to GPIO pins:
  - `TRIGGER` to BCM 6
  - `ECHO` to BCM 5
- Connect the **accelerometer/gyroscope** to the I2C pins (SDA and SCL).
  - Accelerometer: BCM 2
  - Gyroscope: BCM 3
- Connect the **touch sensors** to GPIO pins:
  - Left Click: BCM 17
  - Right Click: BCM 27
  - Scroll: BCM 22
  - Pick/Drop: BCM 23
- Connect the **LEDs** to GPIO pins:
  - DIP Red: BCM 20
  - DIP Green: BCM 21
  - SMD Red: BCM 26
  - SMD Green: BCM 19
  - SMD Blue: BCM 13
- Attach sensors to **glove**:
  - The left-click touch sensor is attached to the index finger of the glove
  - The right-click touch sensor is attached to the middle finger of the glove
  - The scroll touch sensor is attached to the ring finger of the glove
  - The pick/drop touch sensor is attached to the pinkie finger of the glove
  - The accellerometer/gyroscope is attached to the back of the glove

### 3. Run the Program
1. Clone the repository or download the code files (`cam2.py` and `project.py`).
2. Run the main program:
   ```bash
   python project.py
   ```

---

## Code Structure

### `cam2.py`
- Handles **hand tracking** using **MediaPipe** and **OpenCV**.
- Captures frames from the camera, processes them to detect hand landmarks, and maps the hand position to the mouse cursor by normalizing from camera view to screen size.

### `project.py`
- Main program that integrates all functionalities:
  - **GPIO Control**: Handles touch inputs and LED outputs.
  - **Mouse Actions**: Implements left click, right click, scroll, and pick/drop functionality.
  - **Ultrasonic Sensor**: Measures speed gauge to control scroll speed.
  - **Accelerometer/Gyroscope**: Detects hand tilt to control scroll direction.
  - **Threading**: Uses multi-threading to run tasks concurrently on different CPU cores.

---

## Usage
1. **Start the Program**:
   - Run `project.py` to start the gesture-based mouse control system.
2. **Hand Tracking**:
   - Move your hand in front of the camera to control the mouse cursor.
3. **Mouse Actions**:
   - **Left Click**: Press the index-finger touch sensor.
   - **Right Click**: Press the middle-finger touch sensor.
   - **Scroll**: Tilt the device or move the speed gauge closer/farther from the ultrasonic sensor to control it, press the ring-finger touch sensor to activate scroll.
   - **Pick/Drop Mouse**: Press the pinkie-finger touch sensor to toggle mouse control on/off.
4. **Visual Feedback**:
   - The **DIP LED** will turn green when the mouse is picked up and red when the mouse is dropped.
   - The **SMD RGB LED** will light up when the mouse is picked up and a left click is performed.

