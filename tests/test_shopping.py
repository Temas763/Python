import sys
import os
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Добавляем путь для импорта модулей
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@allure.feature("Оформление заказа")
@allure.severity(allure.severity_level.CRITICAL)
class TestSauceDemoShopping:
    """Тесты для проверки функциональности интернет-магазина Sauce Demo."""
    
    @pytest.fixture
    def driver(self):
        """Фикстура для создания и закрытия драйвера."""
        with allure.step("Настройка драйвера браузера"):
            options = Options()
            # options.add_argument("--headless")  # Раскомментируйте для headless режима
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            
            driver = webdriver.Chrome(options=options)
            driver.implicitly_wait(10)
            yield driver
            with allure.step("Закрытие браузера"):
                driver.quit()
    
    @allure.title("Полный процесс оформления заказа")
    @allure.description("""
    Тест проверяет полный процесс оформления заказа в интернет-магазине:
    1. Авторизация пользователя
    2. Добавление товаров в корзину
    3. Переход в корзину и оформление заказа
    4. Заполнение информации о покупателе
    5. Проверка итоговой стоимости
    6. Завершение заказа
    """)
    def test_complete_purchase_flow(self, driver):
        """Тест полного процесса покупки с проверкой итоговой стоимости."""
        
        with allure.step("Открытие сайта и авторизация пользователя"):
            login_page = LoginPage(driver)
            login_page.open().login("standard_user", "secret_sauce")
            
            # Проверка успешной авторизации
            with allure.step("Проверить успешную авторизацию"):
                assert "inventory" in driver.current_url
                allure.attach(driver.get_screenshot_as_png(), 
                            name="after_login", 
                            attachment_type=allure.attachment_type.PNG)
        
        with allure.step("Добавление товаров в корзину"):
            products_page = ProductsPage(driver)
            (products_page
             .add_backpack_to_cart()
             .add_bolt_t_shirt_to_cart()
             .add_onesie_to_cart())
            
            # Проверка количества товаров в корзине
            with allure.step("Проверить количество товаров в корзине"):
                cart_count = products_page.get_cart_count()
                assert cart_count == "3", f"Expected 3 items in cart, but got {cart_count}"
        
        with allure.step("Переход в корзину и оформление заказа"):
            products_page.go_to_cart()
            
            # Проверка перехода в корзину
            with allure.step("Проверить переход в корзину"):
                assert "cart" in driver.current_url
            
            cart_page = CartPage(driver)
            cart_page.click_checkout()
            
            # Проверка перехода к оформлению заказа
            with allure.step("Проверить переход к оформлению заказа"):
                assert "checkout-step-one" in driver.current_url
        
        with allure.step("Заполнение информации для оформления заказа"):
            checkout_page = CheckoutPage(driver)
            (checkout_page
             .fill_checkout_info("John", "Doe", "12345")
             .click_continue())
            
            # Добавляем проверку на ошибки заполнения формы
            with allure.step("Проверить отсутствие ошибок заполнения формы"):
                # Проверяем, что мы перешли на следующую страницу
                if "checkout-step-one" in driver.current_url:
                    # Если остались на той же странице, ищем сообщения об ошибках
                    error_elements = driver.find_elements(By.CLASS_NAME, "error-message-container")
                    if error_elements:
                        error_text = error_elements[0].text
                        allure.attach(f"Ошибка при заполнении формы: {error_text}", 
                                    name="form_error", 
                                    attachment_type=allure.attachment_type.TEXT)
                        raise AssertionError(f"Form validation error: {error_text}")
                
                # Проверка перехода к подтверждению заказа
                with allure.step("Проверить переход к подтверждению заказа"):
                    assert "checkout-step-two" in driver.current_url
                    allure.attach(driver.get_screenshot_as_png(), 
                                name="checkout_overview", 
                                attachment_type=allure.attachment_type.PNG)
        
        with allure.step("Проверка итоговой стоимости заказа"):
            total_text = checkout_page.get_total_price()
            
            # Основная проверка теста
            with allure.step("Проверить корректность итоговой суммы"):
                expected_total = "Total: $58.29"
                assert total_text == expected_total, f"Expected {expected_total}, but got {total_text}"
                allure.attach(f"Итоговая стоимость: {total_text}", 
                            name="total_price", 
                            attachment_type=allure.attachment_type.TEXT)
        
        with allure.step("Завершение оформления заказа"):
            checkout_page.finish_checkout()
            complete_message = checkout_page.get_complete_message()
            
            # Проверка успешного завершения заказа
            with allure.step("Проверить успешное завершение заказа"):
                assert "Thank you for your order!" in complete_message
                allure.attach(driver.get_screenshot_as_png(), 
                            name="order_complete", 
                            attachment_type=allure.attachment_type.PNG)
    
    @allure.title("Добавление товаров в корзину")
    @allure.description("Тест проверяет функциональность добавления товаров в корзину")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_items_to_cart(self, driver):
        """Тест добавления товаров в корзину."""
        
        with allure.step("Авторизация и добавление товаров"):
            login_page = LoginPage(driver)
            login_page.open().login("standard_user", "secret_sauce")
            
            products_page = ProductsPage(driver)
            products_page.add_backpack_to_cart()
            
        with allure.step("Проверить добавление товара в корзину"):
            cart_count = products_page.get_cart_count()
            assert cart_count == "1", f"Expected 1 item in cart, but got {cart_count}"