import pytest
from selenium import webdriver
from pages.calculator_page import CalculatorPage


class TestCalculator:
    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.driver = webdriver.Chrome()  # или другой браузер
        self.driver.implicitly_wait(10)
        self.calculator_page = CalculatorPage(self.driver)

    def teardown_method(self):
        """Завершение после каждого теста"""
        self.driver.quit()

    def test_slow_calculator_addition(self):
        """Тест сложения с задержкой"""
        # Открыть страницу калькулятора
        self.calculator_page.open()

        # Ввести значение задержки
        self.calculator_page.set_delay(45)

        # Выполнить вычисление: 7 + 8
        self.calculator_page.enter_calculation("7+8=")

        # Проверить результат
        result = self.calculator_page.get_result(timeout=50)
        assert result == "15", f"Ожидался результат 15, но получен {result}"
