from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import time


def test_login():
    """Тестирование авторизации на странице логина"""
    driver = None
    try:
        # Настройка Firefox драйвера
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

        # Открытие страницы логина
        driver.get("http://the-internet.herokuapp.com/login")
        print("Страница логина загружена")

        # Поиск и ввод username
        username_field = driver.find_element(By.ID, "username")
        username_field.send_keys("tomsmith")
        print("Введен username: tomsmith")

        # Поиск и ввод password
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys("SuperSecretPassword!")
        print("Введен password")

        # Небольшая пауза перед кликом
        time.sleep(1)

        # Поиск и нажатие кнопки Login
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        print("Кнопка Login нажата")

        # Пауза для загрузки страницы после логина
        time.sleep(2)

        # Поиск и вывод текста с зеленой плашки (flash success)
        success_message = driver.find_element(By.CSS_SELECTOR, ".flash.success")
        message_text = success_message.text.strip()
        print(f"Текст с зеленой плашки: '{message_text}'")

        # Пауза чтобы увидеть результат
        time.sleep(5)

    except Exception as e:
        print(f"Ошибка: {e}")

    finally:
        # Закрытие браузера
        if driver:
            driver.quit()
            print("Браузер закрыт")


if __name__ == "__main__":
    test_login()
