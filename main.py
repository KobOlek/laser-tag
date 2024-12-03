import cv2
import pyautogui, mouse
import numpy as np
from picamera2 import Picamera2
from util import get_limits
import os
import subprocess

# Constants for screen size and camera configuration
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
CAMERA = Picamera2()
CONFIG = CAMERA.create_preview_configuration({'format': 'RGB888'})
CAMERA.configure(CONFIG)
CAMERA.start()

# Function to get the largest location of the given color in the frame
def get_color_location(frame, lower_color, upper_color):
    """Detects the largest area of a specified color and returns its coordinates."""
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_frame, lower_color, upper_color)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(mask)
    return max_loc

# Set color limits (in BGR format, reversed to RGB for correct conversion to HSV)
LOWER_LASER, UPPER_LASER = np.array([0, 0, 255]), np.array([255, 255, 255])
LOWER_RED, UPPER_RED = get_limits([255, 0, 0][::-1])
LOWER_BLUE, UPPER_BLUE = get_limits([0, 0, 255][::-1])
LOWER_GREEN, UPPER_GREEN = get_limits([0, 255, 0][::-1])

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
    # Create the window first before doing anything
    cv2.namedWindow('Laser Tracker', flags=cv2.WINDOW_GUI_NORMAL)
    # Try to make the window borderless or without a title bar (platform dependent)
    # cv2.setWindowProperty('Laser Tracker', cv2.WND_PROP_FULLSCREEN, 1)  # Try fullscreen
    cv2.setWindowProperty('Laser Tracker', cv2.WND_PROP_TOPMOST, 1)  # Ensure always on top

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
        
        # Move the window to the center of the screen on the X-axis
        window_title_bar_height = 750  # approximate height of the window's title bar
        cv2.moveWindow('Laser Tracker', (SCREEN_WIDTH - 300) // 2, window_title_bar_height)  # Center on X-axis

        # Exit condition: Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
