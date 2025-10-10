from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import time


def test_input_field():
    """Тестирование работы с полем ввода в Firefox"""
    driver = None
    try:
        # Настройка Firefox драйвера
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

        # Открытие страницы
        driver.get("http://the-internet.herokuapp.com/inputs")
        print("Страница inputs загружена")

        # Поиск поля ввода
        input_field = driver.find_element(By.TAG_NAME, "input")
        print("Поле ввода найдено")

        # Ввести текст "Sky"
        input_field.send_keys("Sky")
        print("Текст 'Sky' введен в поле")

        # Небольшая пауза чтобы увидеть результат
        time.sleep(1)

        # Очистить поле
        input_field.clear()
        print("Поле очищено")

        # Небольшая пауза чтобы увидеть результат
        time.sleep(1)

        # Ввести текст "Pro"
        input_field.send_keys("Pro")
        print("Текст 'Pro' введен в поле")

        # Небольшая пауза чтобы увидеть результат
        time.sleep(1)

        print("✅ Все операции выполнены успешно")

    except Exception as e:
        print(f"❌ Ошибка: {e}")

    finally:
        # Закрытие браузера
        if driver:
            driver.quit()
            print("Браузер закрыт")


if __name__ == "__main__":
    test_input_field()
