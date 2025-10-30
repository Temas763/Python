from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
import allure


class ProductsPage:
    """Page Object для страницы товаров Sauce Demo."""
    
    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация страницы товаров.
        
        Args:
            driver: WebDriver instance для управления браузером
        """
        self.driver = driver
    
    @allure.step("Добавить товар 'Sauce Labs Backpack' в корзину")
    def add_backpack_to_cart(self) -> 'ProductsPage':
        """
        Добавляет рюкзак Sauce Labs Backpack в корзину.
        
        Returns:
            ProductsPage: Текущий экземпляр страницы
        """
        add_to_cart_button = self.driver.find_element(
            By.ID, "add-to-cart-sauce-labs-backpack"
        )
        add_to_cart_button.click()
        return self
    
    @allure.step("Добавить товар 'Sauce Labs Bolt T-Shirt' в корзину")
    def add_bolt_t_shirt_to_cart(self) -> 'ProductsPage':
        """
        Добавляет футболку Sauce Labs Bolt T-Shirt в корзину.
        
        Returns:
            ProductsPage: Текущий экземпляр страницы
        """
        add_to_cart_button = self.driver.find_element(
            By.ID, "add-to-cart-sauce-labs-bolt-t-shirt"
        )
        add_to_cart_button.click()
        return self
    
    @allure.step("Добавить товар 'Sauce Labs Onesie' в корзину")
    def add_onesie_to_cart(self) -> 'ProductsPage':
        """
        Добавляет комбинезон Sauce Labs Onesie в корзину.
        
        Returns:
            ProductsPage: Текущий экземпляр страницы
        """
        add_to_cart_button = self.driver.find_element(
            By.ID, "add-to-cart-sauce-labs-onesie"
        )
        add_to_cart_button.click()
        return self
    
    @allure.step("Получить количество товаров в корзине")
    def get_cart_count(self) -> str:
        """
        Получает количество товаров в корзине из бейджа.
        
        Returns:
            str: Количество товаров в корзине
        """
        cart_badge = self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        return cart_badge.text
    
    @allure.step("Перейти в корзину")
    def go_to_cart(self) -> 'ProductsPage':
        """
        Переходит на страницу корзины.
        
        Returns:
            ProductsPage: Текущий экземпляр страницы
        """
        cart_link = self.driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart_link.click()
        return self