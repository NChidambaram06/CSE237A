import cv2
import mediapipe
import numpy as np
import pyautogui
from picamzero import PiCamera

# Initialize screen size
width, height = pyautogui.size()
print(f"Screen width: {width} pixels")
print(f"Screen height: {height} pixels")

# Initialize PiCamera
camera = PiCamera()
camera.resolution = (640, 480)
camera.start()

# Initialize MediaPipe Hand Tracking
# mp_drawing = mp.solutions.drawing_utils
# mp_hands = mp.solutions.hands
drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands

hands = handsModule.Hands(static_image_mode=False, 
                        min_detection_confidence=0.7, 
                        min_tracking_confidence=0.7, 
                        max_num_hands=2)

def getXY():
    # Capture frame from PiCamera
    frame = camera.array  # Get the image as a NumPy array
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convert to BGR for OpenCV

    # Get frame dimensions
    frameHeight, frameWidth, _ = frame.shape
    xPixelLoc = 0
    yPixelLoc = 0

    # Process frame with MediaPipe
    results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    if results.multi_hand_landmarks:
        for handLandmarks in results.multi_hand_landmarks:
            for point in handsModule.HandLandmark:
                if point == 0:  # Wrist
                    wrist = handLandmarks.landmark[handsModule.HandLandmark.WRIST]
                    print(f"Wrist (Landmark 0) - X: {wrist.x}, Y: {wrist.y}, Z: {wrist.z}")

                    # Convert to pixel coordinates
                    xPixelLoc = min(width * (1 - wrist.x), width)  # Fix mirroring
                    yPixelLoc = min(height * wrist.y, height)
                    print(f"Pixel Location: x: {xPixelLoc}, y: {yPixelLoc}")

                # Draw landmarks on frame
                # drawingModule.draw_landmarks(frame, hand_landmarks, handsModule.HAND_CONNECTIONS)
                normalizedLandmark = handLandmarks.landmark[point]
                pixelCoordinatesLandmark = drawingModule._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, frameWidth, frameHeight)

                cv2.circle(frame, pixelCoordinatesLandmark, 5, (0, 255, 0), -1)


    # Display the frame
    cv2.imshow('Hand Tracking', frame)

    # Exit on 'ESC' key
    if cv2.waitKey(1) == 27:
        return
    return xPixelLoc, yPixelLoc

# Run hand tracking loop
while True:
    getXY()

# Cleanup
cv2.destroyAllWindows()
camera.stop()