**Gesture Based Mouse**

# Gesture-Based Mouse Control Using Raspberry Pi

## Overview
This project implements a **gesture-based mouse control system** using a **Raspberry Pi**. The system allows users to control a computer's mouse cursor and perform actions like clicking, scrolling, and picking up/dropping the mouse using hand gestures and physical buttons. The project leverages **MediaPipe** for hand tracking, **OpenCV** for image processing, and **GPIO** for interfacing with physical buttons and LEDs.

---

## Features
1. **Hand Tracking**:
   - Tracks the user's hand using a camera and maps the hand's position to the mouse cursor on the screen.
   - Uses **MediaPipe** for hand landmark detection.

2. **Mouse Actions**:
   - **Left Click**: Triggered by a physical button.
   - **Right Click**: Triggered by another physical button.
   - **Scroll**: Controlled by tilting the device or using an ultrasonic sensor to detect hand distance.
   - **Pick/Drop Mouse**: Toggles the mouse control on/off using a physical button.

3. **Visual Feedback**:
   - **DIP Two-Color LED**: Indicates whether the mouse is active (green) or inactive (red).
   - **SMD RGB LED**: Lights up when the mouse is active and a left click is performed.

4. **Ultrasonic Sensor**:
   - Measures the distance of the hand from the sensor to control the scroll speed.

5. **Accelerometer/Gyroscope**:
   - Detects device tilt to control the scroll direction (up or down).

6. **Multi-Core Processing**:
   - The program uses **threading** and **CPU core affinity** to optimize performance by pinning specific tasks to different CPU cores.

---

## Hardware Requirements
- **Raspberry Pi** (with GPIO pins)
- **Camera Module** (e.g., PiCamera)
- **Ultrasonic Sensor** (HC-SR04)
- **Accelerometer/Gyroscope** (MPU6050)
- **Push Buttons** (for left click, right click, scroll, and pick/drop)
- **LEDs**:
  - DIP Two-Color LED (red and green)
  - SMD RGB LED (red, green, blue)
- **Resistors** (for LEDs)
- **Jumper Wires** and **Breadboard**

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

---

## Troubleshooting
1. **Camera Not Working**:
   - Ensure the camera module is properly connected and enabled in the Raspberry Pi settings.
   - Run `raspi-config` to enable the camera interface.
2. **GPIO Errors**:
   - Check the wiring of the buttons, LEDs, and sensors.
   - Ensure the correct GPIO pins are used in the code.
3. **Hand Tracking Issues**:
   - Ensure proper lighting and a clear view of the hand.
   - Adjust the `min_detection_confidence` and `min_tracking_confidence` parameters in `cam2.py` if needed.

---

## Future Improvements
1. **Gesture Recognition**:
   - Add support for more gestures (e.g., pinch to zoom, swipe).
2. **Wireless Control**:
   - Implement wireless communication (e.g., Bluetooth or Wi-Fi) to control the mouse remotely.
3. **Energy Efficiency**:
   - Optimize the code to reduce CPU usage and improve battery life (if using a portable setup).

---

## License
This project is open-source and available under the **MIT License**. Feel free to modify and distribute it as needed.

---

## Acknowledgments
- **MediaPipe**: For providing an excellent hand tracking solution.
- **Raspberry Pi Foundation**: For creating an accessible and powerful platform for DIY projects.
- **OpenCV**: For enabling real-time image processing.

---

## Contact
For questions or feedback, please contact:
- **Your Name**: [Your Email]
- **GitHub**: [Your GitHub Profile]

---

Enjoy building and using your gesture-based mouse control system! 🎉
