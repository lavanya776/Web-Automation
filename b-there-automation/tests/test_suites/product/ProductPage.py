from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class ProductPage:    
    # URLs
    PRODUCTS_URL = "https://b-there.in/sf/products"
    
    # Product List Locators
    PRODUCT_ITEMS = (By.CSS_SELECTOR, ".personalized-prod")
    PRODUCT_TITLE = (By.CSS_SELECTOR, ".personalized-prod-details h5")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".personalized-prod-price p")
    SHOP_NOW_BTN = (By.CSS_SELECTOR, ".btn-shop.btn-shop1")
    WISHLIST_BTN = (By.CSS_SELECTOR, ".wish-list")
    
    # Filter Locators
    FILTER_BUTTON = (By.ID, "filter-btn")
    FILTER_ACCORDION = (By.CSS_SELECTOR, "#filter-category")
    CATEGORY_OPTIONS = (By.CSS_SELECTOR, ".form-check-input.subCategory.filter_subcategory")
    PRICE_RANGE_MIN = (By.ID, "lower")
    PRICE_RANGE_MAX = (By.ID, "upper")
    PRICE_FILTER_BUTTON = (By.CSS_SELECTOR, "[data-bs-target='#filter-price']")
    
    # Search Locators
    SEARCH_BTN = (By.ID, "searchBtnInp")
    SEARCH_INPUT = (By.ID, "search-box")
    SEARCH_SUBMIT = (By.ID, "search-submit")
    
    # Header Elements
    CART_BUTTON = (By.CSS_SELECTOR, "a[href='https://b-there.in/cart']")
    PROFILE_BUTTON = (By.CSS_SELECTOR, "a[href='https://b-there.in/myaccount']")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open_products_page(self):
        """Navigate directly to products page"""
        self.driver.get(self.PRODUCTS_URL)
        self.wait.until(EC.presence_of_element_located(self.PRODUCT_ITEMS))
        time.sleep(1)  # Wait for page load

    def scroll_to_products_section(self):
        """Scroll to the products section in the middle"""
        # Find the products container
        products_section = self.driver.find_element(By.CSS_SELECTOR, ".personalized-prod-list")
        # Scroll to products section
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", products_section)
        time.sleep(1)

    def scroll_to_product(self, index=0):
        """Scroll to a specific product
        Args:
            index (int): Index of the product to scroll to (0 for first product)
        """
        products = self.driver.find_elements(*self.PRODUCT_ITEMS)
        if len(products) > index:
            # Scroll product into center view
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", products[index])
            time.sleep(1)

    def get_product_count(self):
        """Get the total number of products displayed"""
        self.scroll_to_products_section()
        products = self.driver.find_elements(*self.PRODUCT_ITEMS)
        return len(products)

    def get_product_titles(self):
        """Get list of all product titles"""
        self.scroll_to_products_section()
        products = self.wait.until(
            EC.presence_of_all_elements_located(self.PRODUCT_TITLE)
        )
        return [product.text for product in products]

    def get_product_prices(self):
        """Get list of all product prices"""
        self.scroll_to_products_section()
        prices = self.wait.until(
            EC.presence_of_all_elements_located(self.PRODUCT_PRICE)
        )
        return [price.text for price in prices]

    def scroll_to_top(self):
        """Scroll to top of the page"""
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)

    def click_filter_button(self):
        """Click the filter button"""
        try:
            # Wait for filter button to be present
            filter_btn = self.wait.until(
                EC.presence_of_element_located(self.FILTER_BUTTON)
            )
            
            # Scroll the page a bit up to ensure filter button is not covered
            self.driver.execute_script("window.scrollBy(0, -150);")
            time.sleep(1)
            
            try:
                # Try regular click first
                filter_btn.click()
            except:
                # If regular click fails, try JavaScript click
                self.driver.execute_script("arguments[0].click();", filter_btn)
                # If that fails, try the filterOpen() function directly
                self.driver.execute_script("filterOpen();")
            
            time.sleep(1)
            
        except Exception as e:
            print(f"Error clicking filter button: {str(e)}")
            # Try executing the filterOpen function directly as last resort
            self.driver.execute_script("filterOpen();")

    def open_category_filter(self):
        """Open the category filter accordion"""
        # Wait for and click category filter
        category_filter = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-bs-target='#filter-category']"))
        )
        category_filter.click()
        time.sleep(1)

    def open_price_filter(self):
        """Open the price filter accordion"""
        # Wait for and click price filter
        price_filter = self.wait.until(
            EC.element_to_be_clickable(self.PRICE_FILTER_BUTTON)
        )
        price_filter.click()
        time.sleep(1)

    def search_product(self, search_term):
        """Search for a product
        Args:
            search_term (str): Product name to search
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
        
        # Wait for results to load
        self.wait.until(
            EC.presence_of_all_elements_located(self.PRODUCT_ITEMS)
        )

    def click_shop_now(self, index=0):
        """Click Shop Now button for a product
        Args:
            index (int): Index of the product (0 for first product)
        """
        # First scroll to the product
        self.scroll_to_product(index)
        
        shop_now_buttons = self.wait.until(
            EC.presence_of_all_elements_located(self.SHOP_NOW_BTN)
        )
        if len(shop_now_buttons) > index:
            # Wait for button to be clickable
            self.wait.until(EC.element_to_be_clickable(shop_now_buttons[index]))
            shop_now_buttons[index].click()
            time.sleep(1)

    def add_to_wishlist(self, index=0):
        """Add product to wishlist
        Args:
            index (int): Index of the product (0 for first product)
        """
        # First scroll to the product
        self.scroll_to_product(index)
        
        wishlist_buttons = self.wait.until(
            EC.presence_of_all_elements_located(self.WISHLIST_BTN)
        )
        if len(wishlist_buttons) > index:
            # Wait for button to be clickable
            self.wait.until(EC.element_to_be_clickable(wishlist_buttons[index]))
            wishlist_buttons[index].click()
            time.sleep(1)

    def set_price_range(self, min_price, max_price):
        """Set price filter range
        Args:
            min_price (int): Minimum price
            max_price (int): Maximum price
        """
        # First scroll to products section for better filter interaction
        self.scroll_to_products_section()
        
        self.click_filter_button()
        self.open_price_filter()
        
        # Wait for and scroll to price filter section
        price_section = self.wait.until(
            EC.presence_of_element_located((By.ID, "filter-price"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", price_section)
        time.sleep(1)
        
        # Wait for sliders to be present
        min_slider = self.wait.until(
            EC.presence_of_element_located(self.PRICE_RANGE_MIN)
        )
        max_slider = self.wait.until(
            EC.presence_of_element_located(self.PRICE_RANGE_MAX)
        )
        
        # Set values using JavaScript
        self.driver.execute_script(f"arguments[0].value = '{min_price}'", min_slider)
        self.driver.execute_script(f"arguments[0].value = '{max_price}'", max_slider)
        
        # Trigger input events to apply filters
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input'))", min_slider)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input'))", max_slider)
        time.sleep(2)

    def select_category(self, index):
        """Select category from filter
        Args:
            index (int): Index of category to select (0 for first category)
        """
        # First scroll to products section for better filter interaction
        self.scroll_to_products_section()
        
        self.click_filter_button()
        self.open_category_filter()
        
        # Wait for and scroll to category filter section
        category_section = self.wait.until(
            EC.presence_of_element_located(self.FILTER_ACCORDION)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", category_section)
        time.sleep(1)
        
        # Wait for categories to be present
        categories = self.wait.until(
            EC.presence_of_all_elements_located(self.CATEGORY_OPTIONS)
        )
        
        if len(categories) > index:
            # Scroll category into view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", categories[index])
            time.sleep(1)
            categories[index].click()
            time.sleep(2)

    def go_to_cart(self):
        """Navigate to cart page"""
        self.driver.find_element(*self.CART_BUTTON).click()
        time.sleep(1)

    def go_to_profile(self):
        """Navigate to profile page"""
        self.driver.find_element(*self.PROFILE_BUTTON).click()
        time.sleep(1)

def test_product_page():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')
    
    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Create ProductPage instance
        product_page = ProductPage(driver)
        
        # Open the products page
        product_page.open_products_page()
        
        # Get initial product count
        initial_count = product_page.get_product_count()
        print(f"Total products displayed: {initial_count}")
        
        # Get product titles and prices
        titles = product_page.get_product_titles()
        prices = product_page.get_product_prices()
        print("Product titles:", titles)
        print("Product prices:", prices)
        
        # Scroll to products section first
        product_page.scroll_to_products_section()
        time.sleep(2)
        
        # Test search functionality
        product_page.search_product("frame")
        time.sleep(2)
        
        # Scroll back to products section
        product_page.scroll_to_products_section()
        time.sleep(2)
        
        # Test filter functionality with longer wait times
        product_page.set_price_range(100, 1000)
        time.sleep(3)
        
        # Scroll and test category filter
        product_page.scroll_to_products_section()
        time.sleep(1)
        product_page.select_category(0)  # Select first category
        time.sleep(3)
        
        # Test adding to wishlist
        product_page.add_to_wishlist(0)  # Add first product to wishlist
        time.sleep(1)
        
        # Test Shop Now button
        product_page.click_shop_now(0)  # Click Shop Now on first product
        time.sleep(1)
        
        # Test cart navigation
        product_page.go_to_cart()
        time.sleep(1)
        
        # Test profile navigation
        product_page.go_to_profile()
        
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    test_product_page()
