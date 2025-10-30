from selenium.webdriver.common.by import By


class ProductsPage:
    def __init__(self, driver):
        self.driver = driver
    
    def add_backpack_to_cart(self):
        add_to_cart_button = self.driver.find_element(
            By.ID, "add-to-cart-sauce-labs-backpack"
        )
        add_to_cart_button.click()
        return self
    
    def add_bolt_t_shirt_to_cart(self):
        add_to_cart_button = self.driver.find_element(
            By.ID, "add-to-cart-sauce-labs-bolt-t-shirt"
        )
        add_to_cart_button.click()
        return self
    
    def add_onesie_to_cart(self):
        add_to_cart_button = self.driver.find_element(
            By.ID, "add-to-cart-sauce-labs-onesie"
        )
        add_to_cart_button.click()
        return self
    
    def get_cart_count(self):
        cart_badge = self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        return cart_badge.text
    
    def go_to_cart(self):
        cart_link = self.driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart_link.click()
        return self