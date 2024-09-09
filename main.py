import cv2
import numpy as np
import pyautogui
import time

# Load the arrow image
arrow_image = cv2.imread('arrow.png')

# Function to save the screenshot to a file (for debugging)
def save_screenshot(image, filename):
    cv2.imwrite(filename, image)

# Function to take a screenshot and return it as an array
def take_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)  # Convert to BGR for OpenCV
    return screenshot

# Function to locate the arrow on the screen and click
def find_and_click_arrow():
    screenshot = take_screenshot()

    # Convert screenshot and arrow image to grayscale
    gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    gray_arrow = cv2.cvtColor(arrow_image, cv2.COLOR_BGR2GRAY)

    # Use OpenCV to find the arrow icon in the screenshot
    result = cv2.matchTemplate(gray_screenshot, gray_arrow, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= 0.85)  # Threshold for matching

    # If no arrow is found, return False to stop the loop
    if len(loc[0]) == 0:
        return False

    # Click all found arrow icons
    for pt in zip(*loc[::-1]):
        # Move mouse and click
        pyautogui.moveTo(pt[0] + gray_arrow.shape[1] // 2, pt[1] + gray_arrow.shape[0] // 2, duration=0.2)  # Faster
        pyautogui.click()
        time.sleep(1)  # Short delay after each click

    return True

# Function to scroll down
def scroll_down(amount=-1500):
    pyautogui.scroll(amount)  # Adjust the scroll amount
    time.sleep(1)  # Allow page to load after scrolling

# Function to scroll to the top of the page
def scroll_to_top():
    pyautogui.scroll(3000)  # Scroll up to the top of the page
    time.sleep(1)

# Function to check if we have reached the bottom of the page by comparing screenshots
def is_bottom_of_page(last_screenshot):
    current_screenshot = take_screenshot()
    difference = cv2.absdiff(last_screenshot, current_screenshot)
    result = np.any(difference)
    return not result  # If no difference, we are at the bottom

# Function to recheck the entire page for arrows
def recheck_entire_page():
    scroll_to_top()  # Start from the top
    while True:
        found_arrow = find_and_click_arrow()  # Check and click arrows
        if not found_arrow:
            break  # Exit loop if no more arrows are found
        scroll_down(-500)  # Slowly scroll down and check again

# Main loop
screenshot_counter = 1
last_screenshot = take_screenshot()  # Initial screenshot for bottom detection

while True:
    print("Searching for arrow...")

    # Check for arrows before scrolling and recheck the entire page if needed
    found_arrow = find_and_click_arrow()
    time.sleep(3)
    # If arrows were clicked, recheck the entire page
    if found_arrow:
        recheck_entire_page()

    # Check if we are at the bottom of the page by comparing screenshots
    if is_bottom_of_page(last_screenshot):
        print("Reached the bottom of the page. Stopping.")
        break

    # Scroll down to load more content
    last_screenshot = take_screenshot()  # Update last_screenshot after scrolling
    scroll_down()

print("Script finished.")
