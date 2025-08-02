import os
import datetime

def capture_screenshot(driver, test_name="error"):
    """
    Capture a screenshot from the Selenium WebDriver instance.

    Args:
        driver: Selenium WebDriver instance.
        test_name: Descriptive name for the screenshot file (e.g., test or step name).

    The screenshot will be saved under "./screenshots" directory
    with a timestamped filename for uniqueness.
    """
    screenshots_dir = "screenshots"
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{screenshots_dir}/{test_name}_{timestamp}.png"

    try:
        saved = driver.save_screenshot(filename)
        if saved:
            print(f"Screenshot saved: {filename}")
        else:
            print("Failed to save screenshot.")
    except Exception as e:
        print(f"Exception occurred while saving screenshot: {e}")
