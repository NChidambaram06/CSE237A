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
- Connect the **camera module** to the Raspberry Pi.
- Connect the **ultrasonic sensor** to GPIO pins:
  - `TRIG` to GPIO 6
  - `ECHO` to GPIO 5
- Connect the **MPU6050** (accelerometer/gyroscope) to the I2C pins (SDA and SCL).
- Connect the **buttons** to GPIO pins:
  - Left Click: GPIO 17
  - Right Click: GPIO 27
  - Scroll: GPIO 22
  - Pick/Drop: GPIO 23
- Connect the **LEDs** to GPIO pins:
  - DIP Red: GPIO 20
  - DIP Green: GPIO 21
  - SMD Red: GPIO 26
  - SMD Green: GPIO 19
  - SMD Blue: GPIO 13

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
- Captures frames from the camera, processes them to detect hand landmarks, and maps the hand position to the mouse cursor.

### `project.py`
- Main program that integrates all functionalities:
  - **GPIO Control**: Handles button inputs and LED outputs.
  - **Mouse Actions**: Implements left click, right click, scroll, and pick/drop functionality.
  - **Ultrasonic Sensor**: Measures hand distance to control scroll speed.
  - **Accelerometer/Gyroscope**: Detects device tilt to control scroll direction.
  - **Threading**: Uses multi-threading to run tasks concurrently on different CPU cores.

---

## Usage
1. **Start the Program**:
   - Run `project.py` to start the gesture-based mouse control system.
2. **Hand Tracking**:
   - Move your hand in front of the camera to control the mouse cursor.
3. **Mouse Actions**:
   - **Left Click**: Press the left-click button.
   - **Right Click**: Press the right-click button.
   - **Scroll**: Tilt the device or move your hand closer/farther from the ultrasonic sensor.
   - **Pick/Drop Mouse**: Press the pick/drop button to toggle mouse control on/off.
4. **Visual Feedback**:
   - The **DIP LED** will turn green when the mouse is active and red when inactive.
   - The **SMD RGB LED** will light up when the mouse is active and a left click is performed.

