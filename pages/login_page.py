from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
import allure


class LoginPage:
    """Page Object для страницы авторизации Sauce Demo."""
    
    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация страницы авторизации.
        
        Args:
            driver: WebDriver instance для управления браузером
        """
        self.driver = driver
        self.url = "https://www.saucedemo.com/"
    
    @allure.step("Открыть страницу авторизации")
    def open(self) -> 'LoginPage':
        """
        Открывает страницу авторизации.
        
        Returns:
            LoginPage: Текущий экземпляр страницы
        """
        self.driver.get(self.url)
        return self
    
    @allure.step("Ввести имя пользователя: {username}")
    def enter_username(self, username: str) -> 'LoginPage':
        """
        Вводит имя пользователя в поле ввода.
        
        Args:
            username: Имя пользователя для ввода
            
        Returns:
            LoginPage: Текущий экземпляр страницы
        """
        username_field = self.driver.find_element(By.ID, "user-name")
        username_field.clear()
        username_field.send_keys(username)
        return self
    
    @allure.step("Ввести пароль")
    def enter_password(self, password: str) -> 'LoginPage':
        """
        Вводит пароль в поле ввода.
        
        Args:
            password: Пароль для ввода
            
        Returns:
            LoginPage: Текущий экземпляр страницы
        """
        password_field = self.driver.find_element(By.ID, "password")
        password_field.clear()
        password_field.send_keys(password)
        return self
    
    @allure.step("Нажать кнопку Login")
    def click_login(self) -> 'LoginPage':
        """
        Нажимает кнопку входа в систему.
        
        Returns:
            LoginPage: Текущий экземпляр страницы
        """
        login_button = self.driver.find_element(By.ID, "login-button")
        login_button.click()
        return self
    
    @allure.step("Выполнить авторизацию с пользователем {username}")
    def login(self, username: str, password: str) -> 'LoginPage':
        """
        Выполняет полный процесс авторизации.
        
        Args:
            username: Имя пользователя
            password: Пароль
            
        Returns:
            LoginPage: Текущий экземпляр страницы
        """
        self.enter_username(username)
        self.enter_password(password)
        return self.click_login()