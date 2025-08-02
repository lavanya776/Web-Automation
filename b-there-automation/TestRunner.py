
# # from selenium import webdriver
# from selenium.webdriver.chrome.options import Options

# from tests.test_suites.profile.profile import ProfilePage
# from tests.test_suites.homepage.home_page import HomePage
# from tests.test_suites.product_detail.productDetail import ProductDetailPage
# from tests.test_suites.product.product_navigation import ProductNavigationPage
# from test.test_suites.cart.cart import CartPage


# def run_all_tests():
#     chrome_options = Options()
#     chrome_options.add_argument("--start-maximized")
#     driver = webdriver.Chrome(options=chrome_options)

#     try:
#         # Profile tests
#         profile_page = ProfilePage(driver)
#         profile_page.login("your_email@example.com", "your_password")
#         profile_page.update_profile_details(gender="Female", dob="01/01/1990")
#         profile_page.navigate_sidebar_links()

#         # Home tests
#         home_page = HomePage(driver)
#         home_page.open()
#         time.sleep(2)
#         home_page.test_sidebar_home_link()
#         home_page.test_sidebar_about_us_link()
#         home_page.test_sidebar_qr_generator_link()
#         home_page.test_sidebar_products_link()
#         phone = home_page.get_footer_contact_phone()
#         email = home_page.get_footer_contact_email()
#         print(f"Footer Phone: {phone}")
#         print(f"Footer Email: {email}")

#         # Product detail tests
#         product_page = ProductDetailPage(driver)
#         product_page.open_products_page()
#         product_page.search_and_select_product("frame")
#         details = product_page.get_product_details()
#         print("Product Details:")
#         print(f"Name: {details['name']}")
#         print(f"Price: {details['price']}")
#         print(f"Description: {details['description']}")
#         product_page.set_quantity(2)
#         product_page.add_to_cart()

#         print("\nAll tests completed successfully.")

#     finally:
#         driver.quit()

# if __name__ == "__main__":
#     run_all_tests()


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# Import your page classes or test functions here
# Adjust import paths if your files are in packages or folders
from tests.test_suites.profile.profile import ProfilePage
from tests.test_suites.homepage.HomePage import HomePage
from tests.test_suites.product_detail.productDetail import ProductDetailPage
from tests.test_suites.product.ProductPage import ProductPage
from tests.test_suites.cart.cart import CartPage

class TestRunner:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(options=chrome_options)

        # Initialize page objects with the same driver
        self.product_page = ProductDetailPage(self.driver)
        self.product_page1 = ProductPage(self.driver)
        self.cart_page = CartPage(self.driver)
        self.profile_page = ProfilePage(self.driver)
        self.home_page = HomePage(self.driver)

    def run_all_tests(self):
        print("Starting all tests...\n")

        # Example: Profile tests
        print("Running ProfilePage tests:")
        self.profile_page.login("your_email@example.com", "your_password")
        self.profile_page.update_profile_details(gender="Female", dob="01/01/1990")
        self.profile_page.navigate_sidebar_links()
        print("ProfilePage tests completed.\n")

        # Home page tests
        print("Running HomePage tests:")
        self.home_page.open()
        time.sleep(2)
        self.home_page.test_sidebar_home_link()
        self.home_page.test_sidebar_about_us_link()
        self.home_page.test_sidebar_qr_generator_link()
        self.home_page.test_sidebar_products_link()
        phone = self.home_page.get_footer_contact_phone()
        email = self.home_page.get_footer_contact_email()
        print(f"Footer Phone: {phone}")
        print(f"Footer Email: {email}\n")

        # Product page tests
        print("Running ProductPage tests:")
        self.product_page.open_products_page()
        count = self.product_page.get_product_count()
        print(f"Total products displayed: {count}")

        titles = self.product_page.get_product_titles()
        prices = self.product_page.get_product_prices()
        print("Product Titles:", titles)
        print("Product Prices:", prices)

        self.product_page.search_product("frame")
        time.sleep(2)

        self.product_page.set_price_range(100, 1000)
        time.sleep(2)

        self.product_page.select_category(0)
        time.sleep(2)

        self.product_page.add_to_wishlist(0)
        time.sleep(1)

        self.product_page.click_shop_now(0)
        time.sleep(1)

        # Navigate to cart and perform cart related tests
        self.product_page.go_to_cart()
        time.sleep(2)

        self.cart_page.open_cart()  # Ensure cart page is loaded
        items = self.cart_page.get_cart_items()
        print(f"Number of items in cart: {len(items)}")

        cart_titles = self.cart_page.get_cart_item_titles()
        cart_prices = self.cart_page.get_cart_item_prices()
        print("Cart Item Titles:", cart_titles)
        print("Cart Item Prices:", cart_prices)

        # Optional checkout test
        # self.cart_page.click_checkout()
        # time.sleep(2)

        # Navigate to profile page as an example
        self.product_page.go_to_profile()
        time.sleep(2)

        print("\nAll tests completed successfully.")

    def cleanup(self):
        self.driver.quit()


if __name__ == "__main__":
    runner = TestRunner()
    try:
        runner.run_all_tests()
    finally:
        runner.cleanup()
