'''
import cv2
import mediapipe
 
drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands
 
capture = cv2.VideoCapture(0)
 
with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2) as hands:
 
    while (True):
 
        ret, frame = capture.read()
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
 
        if results.multi_hand_landmarks != None:
            for handLandmarks in results.multi_hand_landmarks:
                drawingModule.draw_landmarks(frame, handLandmarks, handsModule.HAND_CONNECTIONS)
 
        cv2.imshow('Test hand', frame)
 
        if cv2.waitKey(1) == 27:
            break
 
cv2.destroyAllWindows()
capture.release()
'''

import cv2
import mediapipe
import pyautogui
from pynput.mouse import Button, Controller

width, height = pyautogui.size()
print(f"Screen width: {width} pixels")
print(f"Screen height: {height} pixels")
 
drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands
 
capture = cv2.VideoCapture(0)
 
frameWidth = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
frameHeight = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

mouse = Controller()

def stretch_range(x): # stretch range form approx 0.2 to 0.8 to 0 to 1 because struggles to detect hand near edge of camera
    x = (x - 0.1)/ (0.9-0.1) 
    return x
# while True:
#     getXY()
hands = None
try:
    hands = handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2)
except Exception as e:
    print(f"Failed to starts handsModule. Error: {e}")

def getXY():    
    ret, frame = capture.read()

    results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    if results.multi_hand_landmarks != None:
        for handLandmarks in results.multi_hand_landmarks:
            for point in handsModule.HandLandmark:
                if point==0:
                    wristLandmark = handLandmarks.landmark[handsModule.HandLandmark.WRIST]
                    print(f"Wrist (Landmark 0) - X: {wristLandmark.x}, Y: {wristLandmark.y}, Z: {wristLandmark.z}")
                    
                    xPixelLoc = min(stretch_range(width) * (1 - wristLandmark.x), width) # 1- wristLandmark.x to fix the mirroring
                    yPixelLoc = min(stretch_range(height) * wristLandmark.y, height)
                    print(f"Pixel Location: x: {xPixelLoc}, y: {yPixelLoc}")
                    mouse.position = (xPixelLoc, yPixelLoc)

                normalizedLandmark = handLandmarks.landmark[point]
                pixelCoordinatesLandmark = drawingModule._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, frameWidth, frameHeight)

                cv2.circle(frame, pixelCoordinatesLandmark, 5, (0, 255, 0), -1)


    cv2.imshow('Test hand', frame)

    if cv2.waitKey(1) == 27:
        return

while True:
    getXY()
 
cv2.destroyAllWindows()
capture.release()
