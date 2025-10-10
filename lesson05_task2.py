from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time


def test_blue_button_dynamic_id():
    """Тестирование клика по синей кнопке с динамическим ID"""
    try:
        # Настройка Chrome драйвера
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

        # Открытие страницы
        driver.get("http://uitestingplayground.com/dynamicid")
        print("Страница dynamicid загружена")

        # Поиск синей кнопки по классу (так как ID динамический и меняется)
        blue_button = driver.find_element(By.CSS_SELECTOR, "button.btn-primary")
        print("Синяя кнопка с динамическим ID найдена")

        # Клик по кнопке
        blue_button.click()
        print("Успешно: Синяя кнопка с динамическим ID была нажата")

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
    test_blue_button_dynamic_id()
