from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_shopping_cart_total():
    # Инициализация драйвера Firefox
    driver = webdriver.Firefox()

    try:
        # Открываем сайт магазина
        driver.get("https://www.saucedemo.com/")

        # Ждем загрузки формы авторизации
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "user-name"))
        )

        # Авторизуемся как standard_user
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        # Ждем загрузки страницы товаров
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
        )

        # Добавляем товары в корзину
        # Sauce Labs Backpack
        driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
        # Sauce Labs Bolt T-Shirt
        driver.find_element(By.ID, "add-to-cart-sauce-labs-bolt-t-shirt").click()
        # Sauce Labs Onesie
        driver.find_element(By.ID, "add-to-cart-sauce-labs-onesie").click()

        # Переходим в корзину
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

        # Ждем загрузки корзины
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "checkout"))
        )

        # Нажимаем Checkout
        driver.find_element(By.ID, "checkout").click()

        # Ждем загрузки формы
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "first-name"))
        )

        # Заполняем форму данными
        driver.find_element(By.ID, "first-name").send_keys("Иван")
        driver.find_element(By.ID, "last-name").send_keys("Петров")
        driver.find_element(By.ID, "postal-code").send_keys("123456")

        # Нажимаем Continue
        driver.find_element(By.ID, "continue").click()

        # Ждем загрузки страницы с итоговой стоимостью
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "summary_total_label"))
        )

        # Читаем итоговую стоимость
        total_element = driver.find_element(By.CLASS_NAME, "summary_total_label")
        total_text = total_element.text

        # Извлекаем числовое значение из текста
        total_amount = total_text.replace("Total: $", "")

        # Проверяем, что итоговая сумма равна $58.29
        assert total_amount == "58.29", f"Ожидалась сумма $58.29, но получили ${total_amount}"

        print(f"Тест пройден! Итоговая сумма: ${total_amount}")

    finally:
        # Закрываем браузер
        driver.quit()
