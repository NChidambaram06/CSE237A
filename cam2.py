import cv2
import mediapipe
import numpy as np
import pyautogui
from picamera2 import Picamera2

# Get screen size
width, height = pyautogui.size()
print(f"Screen width: {width} pixels")
print(f"Screen height: {height} pixels")

# Initialize PiCamera2
camera = Picamera2()
camera.configure(camera.create_still_configuration())
camera.start()

# Initialize MediaPipe Hand Tracking
drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands

hands = handsModule.Hands(static_image_mode=False, 
                        min_detection_confidence=0.7, 
                        min_tracking_confidence=0.7, 
                        max_num_hands=2)
def norm(y): # normalize the y values to between 0 and 1
    return (y - 0.2)/(0.8-0.2)
def normX(x): # normalize the x values to between 0 and 1
    return (x-0.4)/(0.6-0.4)
def getXY():
    # Capture frame from PiCamera2
    frame = camera.capture_array()  # Capture image as NumPy array
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convert to BGR for OpenCV

    # Get frame dimensions
    frameHeight, frameWidth, _ = frame.shape
    xPixelLoc = -1
    yPixelLoc = -1

    # Process frame with MediaPipe
    results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    if results.multi_hand_landmarks:
        for handLandmarks in results.multi_hand_landmarks:
            for point in handsModule.HandLandmark:
                if point == 0:  # Wrist
                    wrist = handLandmarks.landmark[handsModule.HandLandmark.WRIST]
                    print(f"Wrist (Landmark 0) - X: {wrist.x}, Y: {wrist.y}, Z: {wrist.z}")

                    # Convert to pixel coordinates
                    xPixelLoc = min(width * normX(1 - wrist.x), width)  # 1 0 wrist.x to fix the mirroring
                    yPixelLoc = min(height * norm(wrist.y), height)
                    print(f"Pixel Location: x: {xPixelLoc}, y: {yPixelLoc}")

                # Draw landmarks on frame
                normalizedLandmark = handLandmarks.landmark[point]
                pixelCoordinatesLandmark = drawingModule._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, frameWidth, frameHeight)

                cv2.circle(frame, pixelCoordinatesLandmark, 5, (0, 255, 0), -1)
    else:
        print('hidden hand')
    # Display the frame
    cv2.imshow('Hand Tracking', frame)

    # Exit on 'ESC' key
    if cv2.waitKey(1) == 27:
        return
    return xPixelLoc, yPixelLoc

