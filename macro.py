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
button3_bool = True

start_time = time.time()
button1_index = 0
min_distance = 10 #minimum pixel distance the buttons must have from each other in order to prevent duplication illusions

cycle_time = 3 #time it takes loop to run once in seconds

while is_true:
    current_time = time.time()
    if keyboard.is_pressed('q'):
        is_true = False
    
    if current_time-start_time >= (cycle_time/3) and button1_bool:
        button2_bool = True
        button1_bool = False
        try:
            button1_locations_expired = list(pyautogui.locateAllOnScreen('Expired Button.png', confidence= 0.85))
        except pyscreeze.ImageNotFoundException:
            button1_locations_expired = []
        try:
            button1_locations_active = list(pyautogui.locateAllOnScreen('Active Button.png', confidence= 0.85))
        except pyscreeze.ImageNotFoundException:
            button1_locations_active = []
        try:
            
            button1_locations_list = button1_locations_expired + button1_locations_active
            button1_locations_list.sort(key=lambda box: box.top)
            filtered_locations_list = []
            top_abs = 0
            for button1_location_list in button1_locations_list:
                if abs(button1_location_list[1]-top_abs) > min_distance:
                    top_abs = button1_location_list[1]
                    filtered_locations_list.append(button1_location_list)
            #print(pyautogui.center(button1_locations_list[0]), pyautogui.center(button1_locations_list[1]))
            print(filtered_locations_list)
            button1_location = filtered_locations_list[button1_index]
            button1_center = pyautogui.center(button1_location)
            pyautogui.moveTo(button1_center)
            pyautogui.click(button1_center)

        except (pyautogui.ImageNotFoundException, pyscreeze.ImageNotFoundException, IndexError) as e:
            print("Button 1 Not Found", e)
            button2_bool = False
            button1_bool = True

    if current_time-start_time >= (2*(cycle_time/3)) and button2_bool:
        button3_bool = True
        button2_bool = False
        try:
            button2_location = pyautogui.locateOnScreen('Submit Button.png', confidence= 0.85)
            button2_center = pyautogui.center(button2_location)
            pyautogui.click(button2_center)

        except pyautogui.ImageNotFoundException:
            button1_index += 1
            print("Button 2 Not Found")
    
    if current_time-start_time >= cycle_time and button3_bool:
        button1_bool = True
        button3_bool = False
        start_time = time.time()
        try:
            button3_location = pyautogui.locateOnScreen('OK Button.png', confidence= 0.85)
            button3_center = pyautogui.center(button3_location)
            pyautogui.click(button3_center)

        except pyautogui.ImageNotFoundException:
            print("Button 3 Not Found")
