from selenium.webdriver.common.by import By


class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver
    
    def enter_first_name(self, first_name):
        first_name_field = self.driver.find_element(By.ID, "first-name")
        first_name_field.clear()
        first_name_field.send_keys(first_name)
        return self
    
    def enter_last_name(self, last_name):
        last_name_field = self.driver.find_element(By.ID, "last-name")
        last_name_field.clear()
        last_name_field.send_keys(last_name)
        return self
    
    def enter_postal_code(self, postal_code):
        postal_code_field = self.driver.find_element(By.ID, "postal-code")
        postal_code_field.clear()
        postal_code_field.send_keys(postal_code)
        return self
    
    def fill_checkout_info(self, first_name, last_name, postal_code):
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_postal_code(postal_code)
        return self
    
    def click_continue(self):
        continue_button = self.driver.find_element(By.ID, "continue")
        continue_button.click()
        return self
    
    def get_total_price(self):
        total_element = self.driver.find_element(
            By.CLASS_NAME, "summary_total_label"
        )
        return total_element.text
    
    def finish_checkout(self):
        finish_button = self.driver.find_element(By.ID, "finish")
        finish_button.click()
        return self
    
    def get_complete_message(self):
        complete_message = self.driver.find_element(By.CLASS_NAME, "complete-header")
        return complete_message.text