import sys
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Добавляем путь к родительской директории для импорта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


class TestSauceDemoShopping:

    @pytest.fixture
    def driver(self):
        """Фикстура для создания и закрытия драйвера"""
        options = Options()
        # options.add_argument("--headless")  # Раскомментируйте для headless режима
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)
        yield driver
        driver.quit()

    def test_complete_purchase_flow(self, driver):
        """Тест полного процесса покупки"""
        # Открытие сайта и авторизация
        login_page = LoginPage(driver)
        login_page.open().login("standard_user", "secret_sauce")

        # Проверяем, что авторизация прошла успешно
        assert "inventory" in driver.current_url

        # Добавление товаров в корзину
        products_page = ProductsPage(driver)
        (products_page
         .add_backpack_to_cart()
         .add_bolt_t_shirt_to_cart()
         .add_onesie_to_cart())

        # Проверяем, что товары добавлены в корзину
        cart_count = products_page.get_cart_count()
        assert cart_count == "3", f"Expected 3 items in cart, but got {cart_count}"

        # Переход в корзину
        products_page.go_to_cart()
        assert "cart" in driver.current_url

        # Переход к оформлению заказа
        cart_page = CartPage(driver)
        cart_page.click_checkout()
        assert "checkout-step-one" in driver.current_url

        # Заполнение информации для оформления заказа
        checkout_page = CheckoutPage(driver)
        (checkout_page
         .fill_checkout_info("John", "Doe", "12345")
         .click_continue())

        assert "checkout-step-two" in driver.current_url

        # Получение итоговой стоимости
        total_text = checkout_page.get_total_price()

        # Проверка итоговой суммы
        expected_total = "Total: $58.29"
        assert total_text == expected_total, f"Expected {expected_total}, but got {total_text}"

        # Завершение покупки
        checkout_page.finish_checkout()
        complete_message = checkout_page.get_complete_message()
        assert "Thank you for your order!" in complete_message
