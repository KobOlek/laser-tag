# imports
import cv2
import numpy as np
from util import get_limits
import mouse
from screeninfo import get_monitors
import time, pyautogui
from picamera2 import Picamera2

# Connecting to Pi's camera
camera = Picamera2()
config = camera.create_preview_configuration({'format': 'RGB888'})
camera.configure(config)
camera.start()

# Get colors
def get_color(lower_color: np.array, upper_color: np.array):
    mask = cv2.inRange(hsv, lower_color, upper_color)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(mask)
    return maxLoc


# Color limits used for detection
lower_laser = np.array([0, 0, 255])
upper_laser = np.array([255, 255, 255])

lower_red, upper_red = get_limits([200,0,0][::-1])

lower_blue, upper_blue = get_limits([0,0,255][::-1])

lower_green, upper_green = get_limits([0,255,0][::-1])


# Calibration: screen size
screen_width, screen_height = pyautogui.size()[0], pyautogui.size()[1]
# Video capturing
while True:
    frame = camera.capture_array()
    if frame is None:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Color locations, getting coordinates of the largest accumulation of color
    maxLaserLoc = get_color(lower_laser, upper_laser)
    cv2.circle(frame, maxLaserLoc, 20, (255, 255, 255), 2, cv2.LINE_AA)

    maxRedLoc = get_color(lower_red, upper_red)
    cv2.circle(frame, maxRedLoc, 20, (0, 0, 255), 2, cv2.LINE_AA)

    maxBlueLoc = get_color(lower_blue, upper_blue)
    cv2.circle(frame, maxBlueLoc, 20, (255, 0, 0), 2, cv2.LINE_AA)

    maxGreenLoc = get_color(lower_green, upper_green)
    cv2.circle(frame, maxGreenLoc, 20, (0, 255, 0), 2, cv2.LINE_AA)


    # Calibration: projecting image size
    field_width = maxGreenLoc[0] - maxBlueLoc[0]
    field_height = maxBlueLoc[1] - maxRedLoc[1]

    # Calibration: cursor positioning
    if field_width > 0 and field_height > 0:
        width_k = screen_width / field_width
        height_k = screen_height / field_height

        red_x = maxLaserLoc[0] - maxRedLoc[0]
        red_y = maxLaserLoc[1] - maxRedLoc[1]
        if red_x >= 0 and red_y >= 0:
            cursor_x = (red_x) * width_k
            cursor_y = (red_y) * height_k
            mouse.move(int(cursor_x), int(cursor_y))

    # Camera frame showing
    cv2.imshow('Track Laser', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.stop()
cv2.destroyAllWindows()
