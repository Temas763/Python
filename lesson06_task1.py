from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Инициализация драйвера
driver = webdriver.Chrome()
driver.get("http://uitestingplayground.com/ajax")

try:
    # Нажимаем на синюю кнопку
    blue_button = driver.find_element(By.ID, "ajaxButton")
    blue_button.click()

    # Увеличиваем время ожидания и используем более надежный локатор
    green_banner = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "content"))
    )

    # Ждем, пока внутри content появится текст
    WebDriverWait(driver, 20).until(
        EC.text_to_be_present_in_element((By.ID, "content"), "Data loaded")
    )

    # Получаем текст из зеленой плашки
    success_element = driver.find_element(By.CSS_SELECTOR, "p.bg-success")
    banner_text = success_element.text
    print(banner_text)

except Exception as e:
    print(f"Произошла ошибка: {e}")

finally:
    # Закрываем браузер
    driver.quit()
