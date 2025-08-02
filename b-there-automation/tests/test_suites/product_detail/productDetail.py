from pdb import main
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class ProductDetailPage:
    # URLs
    PRODUCTS_URL = "https://b-there.in/sf/products"
    
    # Product List Locators
    PRODUCT_ITEMS = (By.CSS_SELECTOR, ".personalized-prod")
    PRODUCT_TITLE = (By.CSS_SELECTOR, ".personalized-prod-details h5")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".personalized-prod-price p")
    SHOP_NOW_BTN = (By.CSS_SELECTOR, ".btn-shop.btn-shop1")
    
    # Search Locators
    SEARCH_BTN = (By.ID, "searchBtnInp")
    SEARCH_INPUT = (By.ID, "search-box")
    SEARCH_SUBMIT = (By.ID, "search-submit")
    
    # Product Detail Page Locators
    PRODUCT_NAME = (By.CSS_SELECTOR, ".product-detail-title h1")
    PRODUCT_DESCRIPTION = (By.CSS_SELECTOR, ".product-detail-description")
    ADD_TO_CART_BTN = (By.CSS_SELECTOR, ".add-to-cart-btn")
    QUANTITY_INPUT = (By.CSS_SELECTOR, ".quantity-input")
    DETAIL_PRICE = (By.CSS_SELECTOR, ".product-detail-price")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open_products_page(self):
        """Navigate directly to products page"""
        self.driver.get(self.PRODUCTS_URL)
        self.wait.until(EC.presence_of_element_located(self.PRODUCT_ITEMS))
        time.sleep(1)

    def scroll_to_top(self):
        """Scroll to top of the page"""
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)

    def scroll_to_products_section(self):
        """Scroll to the products section in the middle"""
        products_section = self.driver.find_element(By.CSS_SELECTOR, ".personalized-prod-list")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", products_section)
        time.sleep(1)

    def search_and_select_product(self, search_term, index=0):
        """Search for a product and click on it
        Args:
            search_term (str): Product name to search
            index (int): Index of the product to select (0 for first product)
        """
        # First scroll to top for search
        self.scroll_to_top()
        
        # Wait for search button and click
        search_btn = self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_BTN)
        )
        search_btn.click()
        time.sleep(1)
        
        # Enter search term
        search_input = self.wait.until(
            EC.presence_of_element_located(self.SEARCH_INPUT)
        )
        search_input.clear()
        search_input.send_keys(search_term)
        
        # Submit search
        self.driver.find_element(*self.SEARCH_SUBMIT).click()
        time.sleep(2)
        
        # Scroll to results
        self.scroll_to_products_section()
        
        # Wait for results and click on product
        shop_now_buttons = self.wait.until(
            EC.presence_of_all_elements_located(self.SHOP_NOW_BTN)
        )
        if len(shop_now_buttons) > index:
            # Scroll product into view
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",
                shop_now_buttons[index]
            )
            time.sleep(1)
            # Click will open in new tab
            shop_now_buttons[index].click()
            time.sleep(2)
            
            # Switch to the new tab (last opened window)
            self.driver.switch_to.window(self.driver.window_handles[-1])
            time.sleep(1)

    def get_product_details(self):
        """Get product details from the product detail page
        Returns:
            dict: Product details including name, price, description
        """
        # Wait for product details to load
        product_name = self.wait.until(
            EC.presence_of_element_located(self.PRODUCT_NAME)
        ).text
        
        product_price = self.wait.until(
            EC.presence_of_element_located(self.DETAIL_PRICE)
        ).text
        
        product_description = self.wait.until(
            EC.presence_of_element_located(self.PRODUCT_DESCRIPTION)
        ).text
        
        return {
            "name": product_name,
            "price": product_price,
            "description": product_description
        }

    def set_quantity(self, quantity):
        """Set product quantity
        Args:
            quantity (int): Quantity to set
        """
        quantity_input = self.wait.until(
            EC.presence_of_element_located(self.QUANTITY_INPUT)
        )
        quantity_input.clear()
        quantity_input.send_keys(str(quantity))
        time.sleep(1)

    def add_to_cart(self):
        """Click add to cart button"""
        add_to_cart_btn = self.wait.until(
            EC.element_to_be_clickable(self.ADD_TO_CART_BTN)
        )
        add_to_cart_btn.click()
        time.sleep(2)

def test_product_detail():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')
    
    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Create ProductDetailPage instance
        product_page = ProductDetailPage(driver)
        
        # Open the products page
        product_page.open_products_page()
        
        # Search for "frame" and click first result
        product_page.search_and_select_product("frame")
        
        # Get and print product details
        details = product_page.get_product_details()
        print("Product Details:")
        print(f"Name: {details['name']}")
        print(f"Price: {details['price']}")
        print(f"Description: {details['description']}")
        
        # Set quantity to 2
        product_page.set_quantity(2)
        
        # Add to cart
        product_page.add_to_cart()
        
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    # test_product_detail()
    main()
