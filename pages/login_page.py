from selenium.webdriver.common.by import By
from .base_page import BasePage
from config.settings import settings
import allure
import time

class LoginPage(BasePage):
    # Используем правильный URL с параметрами
    LOGIN_URL = "https://id.skyeng.ru/login?_gl=1*1jg2b62*_gcl_au*ODQ5MDY3Njg0LjE3NjIyNDQxOTQ.*_ga*MTUyMjYyMTA1My4xNzYyMjQ0MTk1*_ga_03EGKN82H3*czE3NjIyNjg1ODIkbzIkZzEkdDE3NjIyNjk1NzEkajYwJGwwJGgw*_ga_5DWC4JK87M*czE3NjIyNjg1ODMkbzIkZzEkdDE3NjIyNjk1NzEkajYwJGwwJGhw"
    
    # Правильные локаторы на основе анализа
    PASSWORD_LINK = (By.XPATH, "//a[contains(., 'Войти с помощью пароля')]")
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit' and contains(@class, 'button--primary')]")
    
    @allure.step("Open Skyeng ID login page")
    def open_login_page(self):
        """Открывает страницу логина Skyeng ID с правильным URL"""
        self.open(self.LOGIN_URL)
        time.sleep(5)
        
        print(f"Current URL: {self.driver.current_url}")
        print(f"Page title: {self.driver.title}")
        
        # Проверяем, что страница загрузилась
        assert self.is_login_page_displayed(), "Login page not loaded properly"
    
    @allure.step("Login with email: {email}")
    def login(self, email, password):
        """Выполняет вход в систему"""
        print("=== STARTING LOGIN PROCESS ===")
        
        # Шаг 1: Сначала нажимаем "Войти с помощью пароля"
        try:
            print("Step 1: Clicking 'Войти с помощью пароля'...")
            self.click(self.PASSWORD_LINK)
            print("✓ Password link clicked")
            time.sleep(5)  # Ждем появления формы
        except Exception as e:
            print(f"✗ Failed to click password link: {e}")
            raise Exception("Password login link not found")
        
        # Шаг 2: Вводим email в поле "Телефон, почта или логин"
        try:
            print("Step 2: Entering email...")
            self.input_text(self.USERNAME_INPUT, email)
            print("✓ Email entered successfully")
            time.sleep(1)
        except Exception as e:
            print(f"✗ Failed to enter email: {e}")
            raise Exception("Email input field not found after password link")
        
        # Шаг 3: Вводим пароль
        try:
            print("Step 3: Entering password...")
            self.input_text(self.PASSWORD_INPUT, password)
            print("✓ Password entered successfully")
            time.sleep(1)
        except Exception as e:
            print(f"✗ Failed to enter password: {e}")
            raise Exception("Password input field not found")
        
        # Шаг 4: Нажимаем кнопку "Войти"
        try:
            print("Step 4: Clicking submit button...")
            self.click(self.SUBMIT_BUTTON)
            print("✓ Submit button clicked")
            time.sleep(5)  # Ждем редиректа
        except Exception as e:
            print(f"✗ Failed to submit login form: {e}")
            
            # Альтернативный подход: используем JavaScript
            try:
                print("Trying JavaScript click...")
                submit_button = self.driver.find_element(*self.SUBMIT_BUTTON)
                self.driver.execute_script("arguments[0].click();", submit_button)
                print("✓ Submit button clicked via JavaScript")
                time.sleep(5)
            except Exception as js_e:
                print(f"✗ JavaScript click also failed: {js_e}")
                raise Exception("Submit button not found and JavaScript click failed")
        
        print(f"After login - URL: {self.driver.current_url}")
        print(f"After login - Title: {self.driver.title}")
        
        # Проверяем успешность логина
        if "teachers.skyeng.ru" in self.driver.current_url:
            print("🎉 LOGIN SUCCESSFUL!")
            return True
        else:
            print("⚠️ Login may have failed or redirected elsewhere")
            return False
    
    @allure.step("Check if login page is displayed")
    def is_login_page_displayed(self):
        """Проверяет, отображается ли страница логина"""
        return "id.skyeng.ru/login" in self.driver.current_url