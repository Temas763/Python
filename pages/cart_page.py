from selenium.webdriver.common.by import By


class CartPage:
    def __init__(self, driver):
        self.driver = driver
    
    def get_cart_items(self):
        cart_items = self.driver.find_elements(By.CLASS_NAME, "cart_item")
        return len(cart_items)
    
    def click_checkout(self):
        checkout_button = self.driver.find_element(By.ID, "checkout")
        checkout_button.click()
        return self