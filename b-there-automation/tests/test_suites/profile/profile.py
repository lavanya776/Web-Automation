

from selenium.webdriver.chrome.options import Options
import pytest
import time 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver


class ProfilePage:
    BASE_URL = "https://b-there.in/login"

    def __init__(self, driver):
        self.driver = driver


    @pytest.mark.run(order=1)
    def open(self):
        self.driver.get(self.BASE_URL)


    @pytest.mark.run(order=2)
    def login_successful(self, email, password):
        self.open()
        self.driver.find_element(By.ID, "loginEmail").clear()
        self.driver.find_element(By.ID, "loginEmail").send_keys(email)
        self.driver.find_element(By.ID, "loginPassword").clear()
        self.driver.find_element(By.ID, "loginPassword").send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        # Wait for navigation to myaccount or dashboard
        WebDriverWait(self.driver, 15).until(
            EC.url_contains("myaccount")
        )
        assert "myaccount" in self.driver.current_url, f"Login failed: {self.driver.current_url}"
        print("PASS: Profile login successful")



    @pytest.mark.run(order=3)
    def update_profile_details(self, gender: str, dob: str):
        # Wait for gender dropdown
        gender_dropdown = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "gender"))
        )
        select = Select(gender_dropdown)
        select.select_by_visible_text(gender)

        # Wait for DOB input and enter value
        dob_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "exampleInputDOB1"))
        )
        dob_input.clear()
        dob_input.send_keys(dob)

        # Click Update Profile button
        update_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input.btn-main.btnProfile[value='Update Profile']"))
        )
        update_btn.click()

        # Wait for a success message or page reload (customize as needed)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Profile updated') or contains(text(), 'successfully') or contains(text(), 'updated')]"))
        )
        print("PASS: Profile gender and DOB updated successfully")


    @pytest.mark.run(order=4)
    def navigate_sidebar_links(self):
        """
        Click each sidebar link and wait for navigation. Navigates to:
        - My Account
        - Address Details
        - My Order
        - Wishlist’s
        """
        sidebar_links = [
            ("My Account", "myaccount"),
            ("Address Details", "addresses"),
            ("My Order", "orders"),
            ("Wishlist’s", "wishlists"),
        ]
        for link_text, url_part in sidebar_links:
            link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, link_text))
            )
            link.click()
            WebDriverWait(self.driver, 10).until(
                EC.url_contains(url_part)
            )
            print(f"PASS: Navigated to {link_text}")
            # Navigate back to profile page except for the last link
            if url_part != "wishlists":
                self.driver.get("https://b-there.in/myaccount")
                WebDriverWait(self.driver, 10).until(
                    EC.url_contains("myaccount")
                )
def test_profile():
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        profile_page = ProfilePage(driver)

        # Login with your credentials
        profile_page.login_successful("lavanyap@parasightsolutions.com", "Test@1234")

        # Update profile (example data)
        profile_page.update_profile_details(gender="Female", dob="01/01/1990")

        # Navigate sidebar links
        profile_page.navigate_sidebar_links()

    finally:
        driver.quit()


if __name__ == "__main__":
    test_profile()