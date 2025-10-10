from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Инициализация драйвера
driver = webdriver.Chrome()
driver.get("http://uitestingplayground.com/textinput")

try:
    # Находим поле ввода и вводим текст SkyPro
    input_field = driver.find_element(By.ID, "newButtonName")
    input_field.clear()  # Очищаем поле на случай, если там есть текст
    input_field.send_keys("SkyPro")

    # Находим синюю кнопку и нажимаем на нее
    blue_button = driver.find_element(By.ID, "updatingButton")
    blue_button.click()

    # Ждем обновления текста кнопки
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.ID, "updatingButton"), "SkyPro")
    )

    # Получаем обновленный текст кнопки
    button_text = blue_button.text
    print(button_text)

finally:
    # Закрываем браузер
    driver.quit()
