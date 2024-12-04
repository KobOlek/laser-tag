#!/home/alpha/Documents/laser-tag/.venv/bin/ python3
import cv2
import pyautogui
import mouse
import numpy as np
from picamera2 import Picamera2
from util import get_limits
import tkinter as tk
import threading
import queue

# Constants for screen size and camera configuration
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
CAMERA = Picamera2()
CONFIG = CAMERA.create_preview_configuration({'format': 'RGB888'})
CAMERA.configure(CONFIG)
CAMERA.start()

# Tkinter window setup
ROOT = tk.Tk()
ROOT.overrideredirect(True)
ROOT.geometry(f"500x300+{(SCREEN_WIDTH - 300) // 2}+{720}")
ROOT.configure(bg='#3a3a3a')
ROOT.attributes("-topmost", 1)

# Color range definitions
LOWER_LASER, UPPER_LASER = np.array([0, 0, 255]), np.array([255, 255, 255])
LOWER_RED, UPPER_RED = get_limits([255, 0, 0][::-1])
LOWER_BLUE, UPPER_BLUE = get_limits([0, 0, 255][::-1])
LOWER_GREEN, UPPER_GREEN = get_limits([0, 255, 0][::-1])

# Calibration variables
field_width, field_height = 0, 0  # Will be calculated dynamically during video capture

def get_color_location(frame, lower_color, upper_color):
    """Detects the largest area of a specified color and returns its coordinates."""
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Convert to HSV for better color tracking
    mask = cv2.inRange(hsv_frame, lower_color, upper_color)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(mask)  # Get the max location of the mask
    return max_loc

def calibrate_and_move_cursor(max_laser_loc, max_red_loc, max_blue_loc, max_green_loc):
    """Calibrate and move the cursor based on color locations."""
    global field_width, field_height
    
    # Calibration: calculate field dimensions
    field_width = max_green_loc[0] - max_blue_loc[0]
    field_height = max_blue_loc[1] - max_red_loc[1]

    if field_width <= 0 or field_height <= 0:
        return  # Invalid calibration, don't move the cursor

    # Scaling factors for mapping to screen resolution
    width_k = SCREEN_WIDTH / field_width
    height_k = SCREEN_HEIGHT / field_height

    # Calculate the relative position of the laser pointer within the red region
    red_x = max_laser_loc[0] - max_red_loc[0]
    red_y = max_laser_loc[1] - max_red_loc[1]

    if red_x >= 0 and red_y >= 0:  # Ensure laser is within bounds
        cursor_x = int(red_x * width_k)
        cursor_y = int(red_y * height_k)
        mouse.move(cursor_x, cursor_y)  # Move the mouse cursor to the calculated position

def main(queue):
    """Main loop to capture frames and track laser pointer."""
    # Set up OpenCV window but do not show it
    cv2.namedWindow('Laser Tracker', flags=cv2.WINDOW_GUI_NORMAL)
    cv2.setWindowProperty('Laser Tracker', cv2.WND_PROP_TOPMOST, 1)  # Keep the window on top

    while True:
        frame = CAMERA.capture_array()  # Capture frame from the camera
        if frame is None:
            print("Failed to capture frame, exiting...")
            break

        # Detect color locations (laser, red, blue, green)
        max_laser_loc = get_color_location(frame, LOWER_LASER, UPPER_LASER)
        max_red_loc = get_color_location(frame, LOWER_RED, UPPER_RED)
        max_blue_loc = get_color_location(frame, LOWER_BLUE, UPPER_BLUE)
        max_green_loc = get_color_location(frame, LOWER_GREEN, UPPER_GREEN)

        # Draw circles on detected points for visualization
        cv2.circle(frame, max_laser_loc, 20, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.circle(frame, max_red_loc, 20, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.circle(frame, max_blue_loc, 20, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.circle(frame, max_green_loc, 20, (0, 255, 0), 2, cv2.LINE_AA)

        # Calibrate the system and move the cursor accordingly
        calibrate_and_move_cursor(max_laser_loc, max_red_loc, max_blue_loc, max_green_loc)
        # Center the window on the screen (excluding the title bar height)
        window_title_bar_height = 750  # Approximate height of window title bar (adjust if needed)
        cv2.moveWindow('Laser Tracker', (SCREEN_WIDTH - 300) // 2, window_title_bar_height)
        # Send the frame for processing in Tkinter (avoid calling Tkinter from non-main thread)
        if not queue.full():
            queue.put(frame)

        # Exit condition: Press 'q' to quit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

def update_gui():
    """Update the Tkinter GUI with the latest frame."""
    if not frame_queue.empty():
        frame = frame_queue.get()
        # You can add any code here to display the frame in the Tkinter window
        # For example, convert OpenCV frame to Tkinter-compatible image format and display
        # This is just a placeholder to demonstrate how to update Tkinter safely.

    # Call this method again to continually update the GUI
    ROOT.after(10, update_gui)

def run_opencv(queue):
    """Run the OpenCV processing in a separate thread."""
    main(queue)

if __name__ == "__main__":
    # Create a queue to communicate between threads
    frame_queue = queue.Queue(maxsize=1)  # Queue with size 1 to limit memory usage

    # Run OpenCV in a separate thread
    opencv_thread = threading.Thread(target=run_opencv, args=(frame_queue,))
    opencv_thread.daemon = True  # Make the thread daemon so it exits when the program ends
    opencv_thread.start()

    # Start the Tkinter GUI in the main thread
    ROOT.after(10, update_gui)  # Schedule the GUI update function
    ROOT.mainloop()  # Start Tkinter event loop (main thread)
