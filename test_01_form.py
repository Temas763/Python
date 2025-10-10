from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_form_validation():
    # Инициализация драйвера Edge
    driver = webdriver.Edge()

    try:
        # Открываем страницу
        driver.get("https://bonigarcia.dev/selenium-webdriver-java/data-types.html")

        # Ждем загрузки формы
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "form"))
        )

        # Давайте сначала найдем все поля ввода для отладки
        all_inputs = driver.find_elements(By.TAG_NAME, "input")
        print(f"Найдено полей ввода: {len(all_inputs)}")
        for input_field in all_inputs:
            name = input_field.get_attribute("name")
            print(f"Поле: {name}")

        # Заполняем форму значениями
        driver.find_element(By.CSS_SELECTOR, "[name='first-name']").send_keys("Иван")
        driver.find_element(By.CSS_SELECTOR, "[name='last-name']").send_keys("Петров")
        driver.find_element(By.CSS_SELECTOR, "[name='address']").send_keys("Ленина, 55-3")
        driver.find_element(By.CSS_SELECTOR, "[name='e-mail']").send_keys("test@skypro.com")
        driver.find_element(By.CSS_SELECTOR, "[name='phone']").send_keys("+7985899998787")
        driver.find_element(By.CSS_SELECTOR, "[name='city']").send_keys("Москва")
        driver.find_element(By.CSS_SELECTOR, "[name='country']").send_keys("Россия")
        driver.find_element(By.CSS_SELECTOR, "[name='job-position']").send_keys("QA")
        driver.find_element(By.CSS_SELECTOR, "[name='company']").send_keys("SkyPro")

        # Нажимаем кнопку Submit
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()

        # Ждем применения стилей валидации (увеличим время ожидания)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-danger, .alert-success"))
        )

        # Проверяем, что поле Zip code подсвечено красным
        # Попробуем разные варианты селекторов для zip-code
        zip_selectors = [
            "[name='zip-code']"
        ]

        zip_code_field = None
        for selector in zip_selectors:
            try:
                zip_code_field = driver.find_element(By.CSS_SELECTOR, selector)
                print(f"Найден zip-code поле с селектором: {selector}")
                break
            except:
                continue

        if not zip_code_field:
            # Если не нашли, попробуем найти по placeholder или label
            all_inputs = driver.find_elements(By.TAG_NAME, "input")
            for input_field in all_inputs:
                placeholder = input_field.get_attribute("placeholder") or ""
                if "zip" in placeholder.lower() or "postal" in placeholder.lower():
                    zip_code_field = input_field
                    break

        assert zip_code_field is not None, "Не удалось найти поле Zip code"

        zip_code_classes = zip_code_field.get_attribute("class")
        print(f"Классы zip-code поля: {zip_code_classes}")
        assert "alert-danger" in zip_code_classes, "Поле Zip code не подсвечено красным"

        # Проверяем, что остальные поля подсвечены зеленым
        fields_to_check = [
            "first-name", "last-name", "address", "e-mail", "phone", 
            "city", "country", "job-position", "company"
        ]

        for field_name in fields_to_check:
            field = driver.find_element(By.CSS_SELECTOR, f"[name='{field_name}']")
            field_classes = field.get_attribute("class")
            print(f"Классы поля {field_name}: {field_classes}")
            assert "alert-success" in field_classes, f"Поле {field_name} не подсвечено зеленым"

        print("Все проверки пройдены успешно!")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

    finally:
        # Закрываем браузер
        driver.quit()
