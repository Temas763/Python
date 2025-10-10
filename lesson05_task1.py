from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time


def test_blue_button():
    """Тестирование клика по синей кнопке"""
    try:
        # Настройка Chrome драйвера
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

        # Открытие страницы
        driver.get("http://uitestingplayground.com/classattr")

        # Поиск и клик по синей кнопке
        blue_button = driver.find_element(By.XPATH, "//button[contains(@class, 'btn-primary')]")
        blue_button.click()

        print("Успешно: Синяя кнопка была нажата")

        # Небольшая пауза чтобы увидеть результат
        time.sleep(2)

    except Exception as e:
        print(f"Ошибка: {e}")

    finally:
        # Закрытие браузера
        if 'driver' in locals():
            driver.quit()
        print("Браузер закрыт")


if __name__ == "__main__":
    test_blue_button()
