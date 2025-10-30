from selenium.webdriver.common.by import By


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://www.saucedemo.com/"
    
    def open(self):
        self.driver.get(self.url)
        return self
    
    def enter_username(self, username):
        username_field = self.driver.find_element(By.ID, "user-name")
        username_field.clear()
        username_field.send_keys(username)
        return self
    
    def enter_password(self, password):
        password_field = self.driver.find_element(By.ID, "password")
        password_field.clear()
        password_field.send_keys(password)
        return self
    
    def click_login(self):
        login_button = self.driver.find_element(By.ID, "login-button")
        login_button.click()
        return self
    
    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        return self.click_login()