from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
import allure


class CheckoutPage:
    """Page Object для страницы оформления заказа Sauce Demo."""
    
    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация страницы оформления заказа.
        
        Args:
            driver: WebDriver instance для управления браузером
        """
        self.driver = driver
    
    @allure.step("Ввести имя: {first_name}")
    def enter_first_name(self, first_name: str) -> 'CheckoutPage':
        """
        Вводит имя в форму оформления заказа.
        
        Args:
            first_name: Имя покупателя
            
        Returns:
            CheckoutPage: Текущий экземпляр страницы
        """
        first_name_field = self.driver.find_element(By.ID, "first-name")
        first_name_field.clear()
        first_name_field.send_keys(first_name)
        return self
    
    @allure.step("Ввести фамилию: {last_name}")
    def enter_last_name(self, last_name: str) -> 'CheckoutPage':
        """
        Вводит фамилию в форму оформления заказа.
        
        Args:
            last_name: Фамилия покупателя
            
        Returns:
            CheckoutPage: Текущий экземпляр страницы
        """
        last_name_field = self.driver.find_element(By.ID, "last-name")
        last_name_field.clear()
        last_name_field.send_keys(last_name)
        return self
    
    @allure.step("Ввести почтовый индекс: {postal_code}")
    def enter_postal_code(self, postal_code: str) -> 'CheckoutPage':
        """
        Вводит почтовый индекс в форму оформления заказа.
        
        Args:
            postal_code: Почтовый индекс
            
        Returns:
            CheckoutPage: Текущий экземпляр страницы
        """
        postal_code_field = self.driver.find_element(By.ID, "postal-code")
        postal_code_field.clear()
        postal_code_field.send_keys(postal_code)
        return self
    
    @allure.step("Заполнить информацию для оформления заказа")
    def fill_checkout_info(self, first_name: str, last_name: str, postal_code: str) -> 'CheckoutPage':
        """
        Заполняет всю информацию для оформления заказа.
        
        Args:
            first_name: Имя покупателя
            last_name: Фамилия покупателя
            postal_code: Почтовый индекс
            
        Returns:
            CheckoutPage: Текущий экземпляр страницы
        """
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_postal_code(postal_code)
        return self
    
    @allure.step("Нажать кнопку Continue")
    def click_continue(self) -> 'CheckoutPage':
        """
        Нажимает кнопку продолжения оформления заказа.
        
        Returns:
            CheckoutPage: Текущий экземпляр страницы
        """
        continue_button = self.driver.find_element(By.ID, "continue")
        continue_button.click()
        return self
    
    @allure.step("Получить итоговую стоимость заказа")
    def get_total_price(self) -> str:
        """
        Получает итоговую стоимость заказа.
        
        Returns:
            str: Текст с итоговой стоимостью
        """
        total_element = self.driver.find_element(
            By.CLASS_NAME, "summary_total_label"
        )
        return total_element.text
    
    @allure.step("Завершить оформление заказа")
    def finish_checkout(self) -> 'CheckoutPage':
        """
        Завершает оформление заказа.
        
        Returns:
            CheckoutPage: Текущий экземпляр страницы
        """
        finish_button = self.driver.find_element(By.ID, "finish")
        finish_button.click()
        return self
    
    @allure.step("Получить сообщение об успешном оформлении заказа")
    def get_complete_message(self) -> str:
        """
        Получает сообщение об успешном оформлении заказа.
        
        Returns:
            str: Текст сообщения
        """
        complete_message = self.driver.find_element(By.CLASS_NAME, "complete-header")
        return complete_message.text
    
    @allure.step("Проверить наличие ошибок валидации")
    def get_error_message(self) -> str:
        """
        Получает сообщение об ошибке валидации формы.
        
        Returns:
            str: Текст ошибки или пустая строка если ошибок нет
        """
        try:
            error_container = self.driver.find_element(By.CLASS_NAME, "error-message-container")
            return error_container.text
        except:
            return ""