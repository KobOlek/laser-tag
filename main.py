#!/usr/bin/env python3
# imports
import cv2, pyautogui, mouse, threading
import numpy as np
from picamera2 import Picamera2
from screeninfo import get_monitors
# Constants for screen size and camera configuration
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
CAMERA = Picamera2()
CONFIG = CAMERA.create_preview_configuration({'format': 'RGB888'})
CAMERA.configure(CONFIG)
CAMERA.start()

# Calibration helper function: Get color limits
def get_color_limits(color):
    """Returns the lower and upper bounds for a color in HSV space."""
    # Inverted RGB to HSV using OpenCV range adjustments
    return np.array([color[2], 50, 50]), np.array([color[0], 255, 255])

# Function to get the largest location of the given color in the frame
def get_color_location(frame, lower_color, upper_color):
    """Detects the largest area of a specified color and returns its coordinates."""
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_frame, lower_color, upper_color)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(mask)
    return max_loc

# Set color limits (in BGR format, reversed to RGB for correct conversion to HSV)
LOWER_LASER, UPPER_LASER = np.array([0, 0, 255]), np.array([255, 255, 255])
LOWER_RED, UPPER_RED = get_color_limits([255, 0, 0])
LOWER_BLUE, UPPER_BLUE = get_color_limits([0, 0, 255])
LOWER_GREEN, UPPER_GREEN = get_color_limits([0, 255, 0])

# Calibration variables
field_width, field_height = 0, 0  # Will be calculated dynamically during video capture

def calibrate_and_move_cursor(max_laser_loc, max_red_loc, max_blue_loc, max_green_loc):
    """Calibrate and move the cursor based on color locations."""
    global field_width, field_height
    
    # Calibration: calculate field dimensions
    field_width = max_green_loc[0] - max_blue_loc[0]
    field_height = max_blue_loc[1] - max_red_loc[1]

    # Only move cursor if field dimensions are valid (positive values)
    if field_width > 0 and field_height > 0:
        width_k = SCREEN_WIDTH / field_width
        height_k = SCREEN_HEIGHT / field_height

        # Calculate the relative position of the laser in the red region
        red_x = max_laser_loc[0] - max_red_loc[0]
        red_y = max_laser_loc[1] - max_red_loc[1]

        # If laser is within the bounds, calculate and move the cursor
        if red_x >= 0 and red_y >= 0:
            cursor_x = red_x * width_k
            cursor_y = red_y * height_k
            mouse.move(int(cursor_x), int(cursor_y))

# Main loop to capture and process video frames
def main():
    """Main function to capture frames and track laser pointer."""
    while True:
        # Capture frame from the camera
        frame = CAMERA.capture_array()
        if frame is None:
            print("Failed to capture frame, exiting...")
            break

        # Get the locations of different colors (laser, red, blue, green)
        max_laser_loc = get_color_location(frame, LOWER_LASER, UPPER_LASER)
        max_red_loc = get_color_location(frame, LOWER_RED, UPPER_RED)
        max_blue_loc = get_color_location(frame, LOWER_BLUE, UPPER_BLUE)
        max_green_loc = get_color_location(frame, LOWER_GREEN, UPPER_GREEN)

        # Visualize detected color points
        cv2.circle(frame, max_laser_loc, 20, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.circle(frame, max_red_loc, 20, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.circle(frame, max_blue_loc, 20, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.circle(frame, max_green_loc, 20, (0, 255, 0), 2, cv2.LINE_AA)

        # Calibrate and move the cursor
        calibrate_and_move_cursor(max_laser_loc, max_red_loc, max_blue_loc, max_green_loc)

        # Display the frame with annotations
        cv2.imshow('Laser Tracker', frame)

        # Exit condition: Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    CAMERA.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    t1 = threading.Thread(target=main)
    t1.start()
    t1.join()
 
