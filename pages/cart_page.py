from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
import allure


class CartPage:
    """Page Object для страницы корзины Sauce Demo."""
    
    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация страницы корзины.
        
        Args:
            driver: WebDriver instance для управления браузером
        """
        self.driver = driver
    
    @allure.step("Получить количество товаров в корзине")
    def get_cart_items_count(self) -> int:
        """
        Получает количество товаров в корзине.
        
        Returns:
            int: Количество товаров в корзине
        """
        cart_items = self.driver.find_elements(By.CLASS_NAME, "cart_item")
        return len(cart_items)
    
    @allure.step("Нажать кнопку Checkout")
    def click_checkout(self) -> 'CartPage':
        """
        Нажимает кнопку оформления заказа.
        
        Returns:
            CartPage: Текущий экземпляр страницы
        """
        checkout_button = self.driver.find_element(By.ID, "checkout")
        checkout_button.click()
        return self