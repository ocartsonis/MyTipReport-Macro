import pyscreeze
import cv2
import numpy as np
#MONKEYPATCH
_original_opencv = pyscreeze._locateAll_opencv

def _locateAll_opencv_with_confidence(needleImage, haystackImage, grayscale=None, limit=10000, region=None, step=1, confidence=0.999):
    # Load images into OpenCV format (same as original does)
    needle = pyscreeze._load_cv2(needleImage, grayscale)
    haystack = pyscreeze._load_cv2(haystackImage, grayscale)
    # Crop to region if requested
    if region:
        x, y, w, h = region
        haystack = haystack[y:y+h, x:x+w]
    # Perform the template match
    result = cv2.matchTemplate(haystack, needle, cv2.TM_CCOEFF_NORMED)  # cv2 matchTemplate :contentReference[oaicite:4]{index=4}
    # Extract the peak correlation (minVal, maxVal, minLoc, maxLoc)
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)  # cv2.minMaxLoc :contentReference[oaicite:5]{index=5}
    # Print or log the raw confidence
    print(f"[pyscreeze monkey-patch] peak confidence = {maxVal:.4f} (threshold = {confidence})")
    # Delegate to the original implementation to yield bounding boxes
    yield from _original_opencv(needleImage, haystackImage, grayscale=grayscale, limit=limit, region=region, step=step, confidence=confidence)

# Replace the internal function
pyscreeze._locateAll_opencv = _locateAll_opencv_with_confidence
pyscreeze.locateAll = _locateAll_opencv_with_confidence

import pyautogui
import keyboard
import time

is_true = True
button1_bool = True
button2_bool = True
start_time = time.time()

while is_true:
    current_time = time.time()
    if keyboard.is_pressed('q'):
        is_true = False
    
    if current_time-start_time >= 2 and button1_bool:
        button1_bool = False
        button2_bool = True
        try:
            button1_location = pyautogui.locateOnScreen('google docs.png', confidence= 0.8)
            button1_center = pyautogui.center(button1_location)
            pyautogui.click(button1_center)

        except pyautogui.ImageNotFoundException:
            print("Button 1 Not Found")

    if current_time-start_time >= 4 and button2_bool:
        button1_bool = True
        button2_bool = False
        start_time = time.time()
        try:
            button2_location = pyautogui.locateOnScreen('back arrow.png', confidence= 0.8)
            button2_center = pyautogui.center(button2_location)
            pyautogui.click(button2_center)

        except pyautogui.ImageNotFoundException:
            print("Button 2 Not Found")
