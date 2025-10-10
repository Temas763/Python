from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_slow_calculator():
    # Инициализация драйвера Chrome
    driver = webdriver.Chrome()

    try:
        # Открываем страницу
        driver.get("https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")

        # Ждем загрузки калькулятора
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "delay"))
        )

        # Вводим значение 45 в поле delay
        delay_field = driver.find_element(By.ID, "delay")
        delay_field.clear()
        delay_field.send_keys("45")

        # Нажимаем кнопки: 7 + 8 =
        driver.find_element(By.XPATH, "//span[text()='7']").click()
        driver.find_element(By.XPATH, "//span[text()='+']").click()
        driver.find_element(By.XPATH, "//span[text()='8']").click()
        driver.find_element(By.XPATH, "//span[text()='=']").click()

        # Ждем отображения результата 15 через 45 секунд
        result = WebDriverWait(driver, 46).until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, "screen"), "15")
        )

        # Получаем фактический результат для assert
        screen_element = driver.find_element(By.CLASS_NAME, "screen")
        actual_result = screen_element.text

        # Проверяем, что результат равен 15
        assert actual_result == "15", f"Ожидался результат 15, но получили {actual_result}"

        print("Тест пройден успешно! Результат: 15")

    finally:
        # Закрываем браузер
        driver.quit()
