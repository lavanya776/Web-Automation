from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


class HomePage:
    BASE_URL = "https://b-there.in"
    QR_GENERATOR_URL = "https://b-there.in/sf/qr-generator"
    PRODUCTS_URL = "https://b-there.in/sf/products"

    SIDEBAR_MENU_BTN = (By.ID, "menu")
    SIDEBAR_PROFILE_BTN = (By.XPATH, "//a[@href='https://b-there.in/myaccount']")
    SIDEBAR_CART_BTN = (By.XPATH, "//a[@href='https://b-there.in/cart']")
    FOOTER_CONTACT_PHONE = (By.LINK_TEXT, "+91 9811450553")
    FOOTER_CONTACT_EMAIL = (By.LINK_TEXT, "info@b-there.in")

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.BASE_URL)

    def click_sidebar_menu(self):
        self.driver.find_element(*self.SIDEBAR_MENU_BTN).click()
        time.sleep(1)

    def test_sidebar_home_link(self):
        self.click_sidebar_menu()
        link = self.driver.find_element(By.LINK_TEXT, "Home")
        link.click()
        time.sleep(1)
        assert self.driver.current_url.startswith("https://b-there.in"), f"Home link failed: {self.driver.current_url}"
        print(f"PASS: Home navigates to {self.driver.current_url}")

    def test_sidebar_about_us_link(self):
        self.click_sidebar_menu()
        link = self.driver.find_element(By.LINK_TEXT, "About Us")
        link.click()
        time.sleep(1)
        assert self.driver.current_url.startswith("https://b-there.in/pages/about-us"), f"About Us link failed: {self.driver.current_url}"
        print(f"PASS: About Us navigates to {self.driver.current_url}")

    def test_sidebar_qr_generator_link(self):
        self.click_sidebar_menu()
        link = self.driver.find_element(By.LINK_TEXT, "QR Generator")
        link.click()
        time.sleep(1)
        assert self.driver.current_url.startswith("https://b-there.in/sf/qr-generator"), f"QR Generator link failed: {self.driver.current_url}"
        print(f"PASS: QR Generator navigates to {self.driver.current_url}")

    def test_sidebar_products_link(self):
        self.click_sidebar_menu()
        link = self.driver.find_element(By.LINK_TEXT, "Products")
        link.click()
        time.sleep(1)
        assert self.driver.current_url.startswith("https://b-there.in/sf/products"), f"Products link failed: {self.driver.current_url}"
        print(f"PASS: Products navigates to {self.driver.current_url}")

    def test_sidebar_nav_urls(self):
        self.click_sidebar_menu()
        nav_links = self.driver.find_elements(By.CSS_SELECTOR, "nav.sidebar #sidebarNav .nav-link")
        results = {}
        for link in nav_links:
            text = link.text.strip()
            href = link.get_attribute("href")
            results[text] = href
        return results

    def click_profile(self):
        self.driver.find_element(*self.SIDEBAR_PROFILE_BTN).click()

    def click_cart(self):
        self.driver.find_element(*self.SIDEBAR_CART_BTN).click()

    def get_footer_contact_phone(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        return self.driver.find_element(*self.FOOTER_CONTACT_PHONE).text

    def get_footer_contact_email(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        return self.driver.find_element(*self.FOOTER_CONTACT_EMAIL).text


def test_home_page():
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=chrome_options)

    try:
        home_page = HomePage(driver)

        home_page.open()
        time.sleep(2)  # Let page load

        home_page.test_sidebar_home_link()
        home_page.test_sidebar_about_us_link()
        home_page.test_sidebar_qr_generator_link()
        home_page.test_sidebar_products_link()

        nav_urls = home_page.test_sidebar_nav_urls()
        print("Sidebar Navigation Links and URLs:")
        for text, url in nav_urls.items():
            print(f"{text}: {url}")

        # Demonstrate profile and cart clicks (optional)
        home_page.click_profile()
        time.sleep(2)
        driver.back()
        time.sleep(1)

        home_page.click_cart()
        time.sleep(2)
        driver.back()
        time.sleep(1)

        phone = home_page.get_footer_contact_phone()
        email = home_page.get_footer_contact_email()
        print(f"Footer Phone: {phone}")
        print(f"Footer Email: {email}")

    finally:
        driver.quit()


if __name__ == "__main__":
    test_home_page()
