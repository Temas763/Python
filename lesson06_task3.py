from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Инициализация драйвера
driver = webdriver.Chrome()
driver.get("https://bonigarcia.dev/selenium-webdriver-java/loading-images.html")

try:
    # Ждем, пока появится контейнер с картинками и загрузятся все 4 картинки
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "image-container"))
    )

    # Ждем, пока загрузятся все 4 картинки
    images = WebDriverWait(driver, 15).until(
        lambda driver: driver.find_elements(By.CSS_SELECTOR, "#image-container img")
    )

    # Проверяем, что загружено 4 картинки
    WebDriverWait(driver, 15).until(
        lambda driver: len(driver.find_elements(By.CSS_SELECTOR, "#image-container img")) == 4
    )

    # Получаем все картинки еще раз после полной загрузки
    images = driver.find_elements(By.CSS_SELECTOR, "#image-container img")

    # Получаем значение атрибута src у 3-й картинки (индекс 2)
    third_image_src = images[2].get_attribute("src")
    print(third_image_src)

except Exception as e:
    print(f"Произошла ошибка: {e}")

finally:
    # Закрываем браузер
    driver.quit()
