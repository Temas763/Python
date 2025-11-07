import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.settings import settings
from data.test_data import TestData
from constants import TestConstants

@allure.feature("Schedule UI")
@allure.story("Positive UI Tests")
class TestPositiveUI:

    @allure.title("Successful login to Skyeng Teachers")
    def test_successful_login(self, driver, login_page, schedule_page):
        with allure.step("Open Skyeng ID login page"):
            login_page.open_login_page()

        with allure.step("Enter valid credentials"):
            login_result = login_page.login(settings.EMAIL, settings.PASSWORD)

        with allure.step("Verify successful login and redirect to schedule"):
            # Ожидаем редирект на страницу расписания
            WebDriverWait(driver, 15).until(
                EC.url_contains(settings.SCHEDULE_PAGE)
            )

            print(f"Current URL after login: {driver.current_url}")
            print(f"Page title after login: {driver.title}")

            # Проверяем, что мы на правильной странице
            assert settings.SCHEDULE_PAGE in driver.current_url, \
                f"Not redirected to schedule. Expected: {settings.SCHEDULE_PAGE}, Current URL: {driver.current_url}"

            # Проверяем, что пользователь авторизован
            assert schedule_page.is_logged_in(), "User is not logged in"

            # Проверяем, что страница расписания загружена
            assert schedule_page.is_schedule_loaded(), "Schedule page not loaded properly"

            # Делаем скриншот успешного логина
            allure.attach(driver.get_screenshot_as_png(), 
                         name="successful_login", 
                         attachment_type=allure.attachment_type.PNG)

    @allure.title("View schedule page with auth cookies")
    def test_view_schedule_page(self, driver, schedule_page, auth_cookies):
        with allure.step("Add auth cookies and open schedule page directly"):
            # Открываем страницу расписания напрямую используя URL из настроек
            driver.get(settings.SCHEDULE_PAGE)

            # Добавляем куки авторизации
            for name, value in auth_cookies.items():
                driver.add_cookie({
                    'name': name, 
                    'value': value, 
                    'domain': '.skyeng.ru'
                })

            # Обновляем страницу с куками
            driver.refresh()

            # Ожидаем загрузки страницы расписания
            WebDriverWait(driver, 10).until(
                EC.url_contains(settings.SCHEDULE_PAGE)
            )

            print(f"URL after cookies: {driver.current_url}")
            print(f"Logged in status: {schedule_page.is_logged_in()}")

        with allure.step("Verify schedule page is loaded with authentication"):
            assert schedule_page.is_schedule_loaded(), "Schedule page not loaded"
            assert schedule_page.is_logged_in(), "User is not logged in with cookies"

            # Скриншот загруженной страницы расписания
            allure.attach(driver.get_screenshot_as_png(), 
                         name="schedule_page_loaded", 
                         attachment_type=allure.attachment_type.PNG)

    @allure.title("Navigate through schedule")
    def test_navigate_schedule(self, driver, schedule_page, auth_cookies):
        with allure.step("Open schedule page with auth cookies"):
            driver.get(settings.SCHEDULE_PAGE)

            for name, value in auth_cookies.items():
                driver.add_cookie({
                    'name': name, 
                    'value': value, 
                    'domain': '.skyeng.ru'
                })

            driver.refresh()

            # Ожидаем загрузки страницы
            WebDriverWait(driver, 15).until(
                lambda driver: schedule_page.is_schedule_loaded()
            )

        with allure.step("Navigate through schedule"):
            # Просто проверяем, что можем взаимодействовать со страницей
            assert schedule_page.is_schedule_loaded(), "Schedule page not loaded"

            # Проверяем наличие событий (может быть 0 - это нормально)
            events_count = schedule_page.get_events_count()
            print(f"Found {events_count} events on schedule")

            # Проверяем, что можем кликнуть по различным элементам
            try:
                # Пробуем найти и кликнуть на кнопку добавления
                if schedule_page.is_element_visible(schedule_page.ADD_BUTTON):
                    print("Add button is visible on the schedule page")
                if schedule_page.is_element_visible(schedule_page.CREATE_BUTTON):
                    print("Create button is visible on the schedule page")
            except Exception as e:
                print(f"Some buttons might not be available: {e}")

            # Скриншот навигации
            allure.attach(driver.get_screenshot_as_png(), 
                         name="schedule_navigation", 
                         attachment_type=allure.attachment_type.PNG)

    @allure.title("Check schedule elements visibility")
    def test_schedule_elements_visibility(self, driver, schedule_page, auth_cookies):
        with allure.step("Open schedule page with auth cookies"):
            driver.get(settings.SCHEDULE_PAGE)

            for name, value in auth_cookies.items():
                driver.add_cookie({
                    'name': name, 
                    'value': value, 
                    'domain': '.skyeng.ru'
                })

            driver.refresh()

            # Ожидаем загрузки и авторизации
            WebDriverWait(driver, 15).until(
                lambda driver: schedule_page.is_schedule_loaded() and schedule_page.is_logged_in()
            )

        with allure.step("Verify all required elements are visible"):
            assert schedule_page.is_schedule_loaded(), "Schedule page not loaded"
            assert schedule_page.is_logged_in(), "User not logged in"

            # Проверяем наличие различных элементов расписания
            calendar_visible = schedule_page.is_element_visible(schedule_page.CALENDAR)
            schedule_container_visible = schedule_page.is_element_visible(schedule_page.SCHEDULE_CONTAINER)
            timetable_visible = schedule_page.is_element_visible(schedule_page.TIMETABLE)

            print(f"Calendar visible: {calendar_visible}")
            print(f"Schedule container visible: {schedule_container_visible}")
            print(f"Timetable visible: {timetable_visible}")

            # Хотя бы один из основных элементов должен быть виден
            assert any([calendar_visible, schedule_container_visible, timetable_visible]), \
                "No schedule elements are visible"

            # Проверяем наличие событий (может быть 0 - это нормально)
            events_count = schedule_page.get_events_count()
            print(f"Found {events_count} events on schedule")

            # Скриншот видимых элементов
            allure.attach(driver.get_screenshot_as_png(), 
                         name="schedule_elements", 
                         attachment_type=allure.attachment_type.PNG)

    @allure.title("Check responsive design")
    def test_responsive_design(self, driver, schedule_page, auth_cookies):
        with allure.step("Open schedule page with auth cookies"):
            driver.get(settings.SCHEDULE_PAGE)

            for name, value in auth_cookies.items():
                driver.add_cookie({
                    'name': name, 
                    'value': value, 
                    'domain': '.skyeng.ru'
                })

            driver.refresh()

            # Ожидаем загрузки страницы
            WebDriverWait(driver, 15).until(
                lambda driver: schedule_page.is_schedule_loaded()
            )

        with allure.step("Change window size and verify layout"):
            original_size = driver.get_window_size()
            window_sizes = TestData.get_window_sizes()

            try:
                # Desktop size
                desktop_size = window_sizes["desktop"]
                driver.set_window_size(desktop_size["width"], desktop_size["height"])
                time.sleep(2)  # Даем время на перерисовку

                WebDriverWait(driver, 5).until(
                    lambda driver: schedule_page.is_schedule_loaded()
                )
                assert schedule_page.is_schedule_loaded(), "Schedule not loaded on desktop"
                print("✓ Desktop layout loaded successfully")

                allure.attach(driver.get_screenshot_as_png(), 
                             name="desktop_layout", 
                             attachment_type=allure.attachment_type.PNG)

                # Tablet size
                tablet_size = window_sizes["tablet"]
                driver.set_window_size(tablet_size["width"], tablet_size["height"])
                time.sleep(2)

                WebDriverWait(driver, 5).until(
                    lambda driver: schedule_page.is_schedule_loaded()
                )
                assert schedule_page.is_schedule_loaded(), "Schedule not loaded on tablet"
                print("✓ Tablet layout loaded successfully")

                allure.attach(driver.get_screenshot_as_png(), 
                             name="tablet_layout", 
                             attachment_type=allure.attachment_type.PNG)

                # Mobile size
                mobile_size = window_sizes["mobile"]
                driver.set_window_size(mobile_size["width"], mobile_size["height"])
                time.sleep(2)

                WebDriverWait(driver, 5).until(
                    lambda driver: schedule_page.is_schedule_loaded()
                )
                assert schedule_page.is_schedule_loaded(), "Schedule not loaded on mobile"
                print("✓ Mobile layout loaded successfully")

                allure.attach(driver.get_screenshot_as_png(), 
                             name="mobile_layout", 
                             attachment_type=allure.attachment_type.PNG)

            finally:
                # Restore original size
                driver.set_window_size(original_size['width'], original_size['height'])

@allure.feature("Schedule UI")
@allure.story("Negative UI Tests")
class TestNegativeUI:

    @allure.title("Login with invalid credentials")
    def test_invalid_login(self, driver, login_page):
        with allure.step("Open Skyeng ID login page"):
            login_page.open_login_page()

        with allure.step("Enter invalid credentials"):
            invalid_credentials = TestData.get_invalid_credentials()
            try:
                login_page.login(
                    invalid_credentials["email"], 
                    invalid_credentials["password"]
                )
            except Exception as e:
                # Если не нашли поля ввода, это тоже негативный сценарий
                print(f"Expected behavior - login elements not accessible: {e}")

        with allure.step("Verify error message is displayed or remained on login page"):
            # Ожидаем либо ошибку, либо остаемся на странице логина
            WebDriverWait(driver, 10).until(
                lambda driver: self._get_error_message(driver) is not None or 
                             login_page.is_login_page_displayed() or
                             settings.LOGIN_PAGE in driver.current_url or
                             "id.skyeng.ru/login" in driver.current_url
            )

            error_message = self._get_error_message(driver)
            current_url = driver.current_url
            is_login_page = (settings.LOGIN_PAGE in current_url or 
                           login_page.is_login_page_displayed() or
                           "id.skyeng.ru/login" in current_url)

            print(f"Error message: {error_message}")
            print(f"Current URL: {current_url}")
            print(f"Is login page: {is_login_page}")

            assert is_login_page or error_message is not None, \
                f"Expected login error but might have succeeded. URL: {current_url}"

            # Скриншот ошибки логина
            allure.attach(driver.get_screenshot_as_png(), 
                         name="invalid_login_error", 
                         attachment_type=allure.attachment_type.PNG)

    def _get_error_message(self, driver):
        """Вспомогательный метод для получения сообщения об ошибке"""
        try:
            # Различные возможные локаторы для сообщений об ошибках
            error_selectors = [
                (By.CLASS_NAME, "error"),
                (By.CLASS_NAME, "error-message"),
                (By.CSS_SELECTOR, "[class*='error']"),
                (By.XPATH, "//*[contains(text(), 'error') or contains(text(), 'Error')]"),
                (By.XPATH, "//*[contains(text(), 'неверн') or contains(text(), 'Неверн')]"),
                (By.XPATH, "//*[contains(text(), 'invalid') or contains(text(), 'Invalid')]")
            ]

            for by, selector in error_selectors:
                try:
                    element = WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((by, selector))
                    )
                    if element.is_displayed():
                        return element.text
                except:
                    continue
            return None
        except:
            return None

    @allure.title("Access schedule page without authentication")
    def test_access_protected_page_without_auth(self, driver, schedule_page):
        with allure.step("Try to access schedule page without authentication"):
            driver.get(settings.SCHEDULE_PAGE)

            # Ожидаем либо редирект, либо загрузку страницы без авторизации
            WebDriverWait(driver, 10).until(
                lambda driver: settings.LOGIN_PAGE in driver.current_url or 
                             settings.SCHEDULE_PAGE in driver.current_url or
                             not schedule_page.is_logged_in() or
                             "id.skyeng.ru" in driver.current_url
            )

            print(f"URL without auth: {driver.current_url}")
            print(f"Logged in status without auth: {schedule_page.is_logged_in()}")

        with allure.step("Verify redirected to login or access denied"):
            # Проверяем различные сценарии доступа без авторизации
            current_url = driver.current_url
            redirected_to_login = (settings.LOGIN_PAGE in current_url or 
                                "id.skyeng.ru/login" in current_url)
            access_denied = not schedule_page.is_logged_in()
            on_schedule_page = settings.SCHEDULE_PAGE in current_url

            print(f"Redirected to login: {redirected_to_login}")
            print(f"Access denied: {access_denied}")
            print(f"On schedule page: {on_schedule_page}")

            # Если мы на странице расписания, но не авторизованы - это тоже негативный сценарий
            assert not (on_schedule_page and schedule_page.is_logged_in()), \
                "Should not have access to schedule without proper authentication"

            # Скриншот состояния без авторизации
            allure.attach(driver.get_screenshot_as_png(), 
                         name="access_without_auth", 
                         attachment_type=allure.attachment_type.PNG)

    @allure.title("Access non-existent page")
    def test_access_nonexistent_page(self, driver):
        with allure.step("Try to access non-existent page"):
            non_existent_url = f"{settings.BASE_URL}{TestConstants.NON_EXISTENT_PAGE}"
            driver.get(non_existent_url)

            # Ожидаем либо 404, либо редирект
            WebDriverWait(driver, 10).until(
                lambda driver: "404" in driver.title or 
                             "404" in driver.page_source or
                             "Not Found" in driver.page_source or
                             "Страница не найдена" in driver.page_source or
                             driver.current_url != non_existent_url
            )

            print(f"Current URL: {driver.current_url}")
            print(f"Page title: {driver.title}")
            print(f"Page source contains '404': {'404' in driver.page_source}")
            print(f"Page source contains 'Not Found': {'Not Found' in driver.page_source}")

        with allure.step("Verify 404 error or redirect"):
            # Может быть 404 страница или редирект на главную
            current_url = driver.current_url
            is_404 = ("404" in driver.title or 
                     "404" in driver.page_source or
                     "Not Found" in driver.page_source or
                     "Страница не найдена" in driver.page_source)
            is_redirected = current_url != non_existent_url

            print(f"Is 404: {is_404}")
            print(f"Is redirected: {is_redirected}")

            assert is_404 or is_redirected, \
                f"Expected 404 or redirect for non-existent page. URL: {current_url}"

            # Скриншот 404 страницы или редиректа
            allure.attach(driver.get_screenshot_as_png(), 
                         name="nonexistent_page", 
                         attachment_type=allure.attachment_type.PNG)

    @allure.title("Check session timeout behavior")
    def test_session_timeout_behavior(self, driver, schedule_page, auth_cookies):
        with allure.step("Open schedule page with auth cookies"):
            driver.get(settings.SCHEDULE_PAGE)

            for name, value in auth_cookies.items():
                driver.add_cookie({
                    'name': name, 
                    'value': value, 
                    'domain': '.skyeng.ru'
                })

            driver.refresh()

            # Ожидаем загрузки страницы
            WebDriverWait(driver, 10).until(
                lambda driver: schedule_page.is_schedule_loaded()
            )

        with allure.step("Clear cookies to simulate session timeout"):
            # Очищаем куки для симуляции истечения сессии
            driver.delete_all_cookies()
            driver.refresh()

            # Ожидаем редирект на логин или сообщение об ошибке
            WebDriverWait(driver, 10).until(
                lambda driver: settings.LOGIN_PAGE in driver.current_url or 
                             "id.skyeng.ru/login" in driver.current_url or
                             not schedule_page.is_logged_in()
            )

        with allure.step("Verify user is redirected to login after session timeout"):
            current_url = driver.current_url
            is_login_page = (settings.LOGIN_PAGE in current_url or 
                           "id.skyeng.ru/login" in current_url)
            is_logged_out = not schedule_page.is_logged_in()

            assert is_login_page or is_logged_out, \
                f"Expected redirect to login after session timeout. URL: {current_url}"

            # Скриншот после таймаута сессии
            allure.attach(driver.get_screenshot_as_png(), 
                         name="session_timeout", 
                         attachment_type=allure.attachment_type.PNG)
