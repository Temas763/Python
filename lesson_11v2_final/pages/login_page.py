from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from .base_page import BasePage
from config.settings import settings
from constants import TestConstants
import allure
import time
import logging

# Настройка логирования
logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """
    Page Object для страницы логина Skyeng ID
    """

    # Локаторы элементов страницы логина
    PASSWORD_LINK = (By.XPATH, "//a[contains(., 'Войти с помощью пароля') or contains(., 'Password')]")
    USERNAME_INPUT = (By.NAME, "username")
    PHONE_INPUT = (By.NAME, "phone")  # Альтернативное поле для телефона
    EMAIL_INPUT = (By.NAME, "email")  # Альтернативное поле для email
    PASSWORD_INPUT = (By.NAME, "password")
    SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit' and contains(@class, 'button--primary')]")
    CONTINUE_BUTTON = (By.XPATH, "//button[contains(., 'Продолжить') or contains(., 'Continue')]")

    # Локаторы для сообщений об ошибках
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
    ERROR_TEXT = (By.CSS_SELECTOR, "[class*='error']")
    AUTH_ERROR = (By.XPATH, "//*[contains(text(), 'Неверный') or contains(text(), 'неверный') or contains(text(), 'Invalid') or contains(text(), 'invalid')]")

    # Локаторы для проверки успешного логина
    USER_AVATAR = (By.CLASS_NAME, "user-avatar")
    PROFILE_MENU = (By.CLASS_NAME, "profile-menu")
    DASHBOARD_HEADER = (By.XPATH, "//h1[contains(., 'Расписание') or contains(., 'Schedule')]")

    # Локаторы для альтернативных вариантов входа
    GOOGLE_BUTTON = (By.XPATH, "//button[contains(., 'Google')]")
    APPLE_BUTTON = (By.XPATH, "//button[contains(., 'Apple')]")
    FACEBOOK_BUTTON = (By.XPATH, "//button[contains(., 'Facebook')]")

    # Локаторы для восстановления пароля
    FORGOT_PASSWORD_LINK = (By.XPATH, "//a[contains(., 'Забыли пароль') or contains(., 'Forgot password')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 15)  # Увеличиваем время ожидания для логина

    @allure.step("Open Skyeng ID login page")
    def open_login_page(self):
        """Открывает страницу логина Skyeng ID"""
        try:
            logger.info("Opening login page")
            self.open(settings.LOGIN_PAGE)
            time.sleep(3)  # Ждем загрузки страницы

            print(f"Current URL: {self.driver.current_url}")
            print(f"Page title: {self.driver.title}")

            # Проверяем, что страница загрузилась
            if not self.is_login_page_displayed():
                logger.warning("Login page might not have loaded properly")
                # Пробуем обновить страницу
                self.driver.refresh()
                time.sleep(3)

            # Делаем скриншот открытой страницы
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="login_page_opened",
                attachment_type=allure.attachment_type.PNG
            )

            return True

        except Exception as e:
            logger.error(f"Failed to open login page: {e}")
            raise Exception(f"Could not open login page: {e}")

    @allure.step("Login with email: {email}")
    def login(self, email, password):
        """Выполняет вход в систему с указанными учетными данными"""
        logger.info(f"Attempting login with email: {email}")

        print("=== STARTING LOGIN PROCESS ===")

        try:
            # Шаг 1: Переход к форме ввода пароля
            self._click_password_login_option()

            # Шаг 2: Ввод email
            self._enter_username(email)

            # Шаг 3: Ввод пароля
            self._enter_password(password)

            # Шаг 4: Нажатие кнопки входа
            self._click_submit_button()

            # Шаг 5: Проверка результата
            return self._verify_login_success()

        except Exception as e:
            logger.error(f"Login process failed: {e}")
            # Делаем скриншот при ошибке
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="login_failed",
                attachment_type=allure.attachment_type.PNG
            )
            raise

    @allure.step("Click password login option")
    def _click_password_login_option(self):
        """Нажимает на опцию 'Войти с помощью пароля'"""
        try:
            logger.info("Looking for password login option")

            # Пробуем разные локаторы для кнопки пароля
            password_selectors = [
                self.PASSWORD_LINK,
                (By.XPATH, "//button[contains(., 'Пароль')]"),
                (By.XPATH, "//*[contains(text(), 'парол')]")
            ]

            password_link = None
            for selector in password_selectors:
                try:
                    password_link = self.wait.until(EC.element_to_be_clickable(selector))
                    logger.info(f"Found password link with selector: {selector}")
                    break
                except TimeoutException:
                    continue

            if password_link:
                # Пробуем обычный клик
                try:
                    password_link.click()
                    logger.info("Password link clicked successfully")
                except ElementClickInterceptedException:
                    # Пробуем клик через JavaScript
                    self.driver.execute_script("arguments[0].click();", password_link)
                    logger.info("Password link clicked via JavaScript")

                time.sleep(3)  # Ждем появления формы
                return True
            else:
                logger.warning("Password link not found, might already be on password form")
                return True

        except Exception as e:
            logger.error(f"Failed to click password option: {e}")
            # Если не нашли кнопку пароля, возможно мы уже на форме с паролем
            print("Password option not found, continuing...")
            return True

    @allure.step("Enter username: {username}")
    def _enter_username(self, username):
        """Вводит email/username в соответствующее поле"""
        try:
            logger.info(f"Entering username: {username}")

            # Пробуем разные локаторы для поля ввода
            username_selectors = [
                self.USERNAME_INPUT,
                self.EMAIL_INPUT,
                self.PHONE_INPUT,
                (By.ID, "username"),
                (By.ID, "email"),
                (By.ID, "phone"),
                (By.XPATH, "//input[@type='email']"),
                (By.XPATH, "//input[contains(@placeholder, 'почт') or contains(@placeholder, 'email')]")
            ]

            username_field = None
            for selector in username_selectors:
                try:
                    username_field = self.wait.until(EC.element_to_be_clickable(selector))
                    logger.info(f"Found username field with selector: {selector}")
                    break
                except TimeoutException:
                    continue

            if username_field:
                username_field.clear()
                username_field.send_keys(username)
                logger.info("Username entered successfully")
                time.sleep(1)
                return True
            else:
                raise Exception("Username input field not found")

        except Exception as e:
            logger.error(f"Failed to enter username: {e}")
            raise Exception(f"Could not enter username: {e}")

    @allure.step("Enter password")
    def _enter_password(self, password):
        """Вводит пароль в поле пароля"""
        try:
            logger.info("Entering password")

            # Пробуем разные локаторы для поля пароля
            password_selectors = [
                self.PASSWORD_INPUT,
                (By.ID, "password"),
                (By.XPATH, "//input[@type='password']"),
                (By.XPATH, "//input[contains(@placeholder, 'парол')]")
            ]

            password_field = None
            for selector in password_selectors:
                try:
                    password_field = self.wait.until(EC.element_to_be_clickable(selector))
                    logger.info(f"Found password field with selector: {selector}")
                    break
                except TimeoutException:
                    continue

            if password_field:
                password_field.clear()
                password_field.send_keys(password)
                logger.info("Password entered successfully")
                time.sleep(1)
                return True
            else:
                raise Exception("Password input field not found")

        except Exception as e:
            logger.error(f"Failed to enter password: {e}")
            raise Exception(f"Could not enter password: {e}")

    @allure.step("Click submit button")
    def _click_submit_button(self):
        """Нажимает кнопку отправки формы"""
        try:
            logger.info("Looking for submit button")

            # Пробуем разные локаторы для кнопки отправки
            submit_selectors = [
                self.SUBMIT_BUTTON,
                self.CONTINUE_BUTTON,
                (By.XPATH, "//button[contains(., 'Войти')]"),
                (By.XPATH, "//button[contains(., 'Login')]"),
                (By.XPATH, "//button[contains(., 'Sign in')]"),
                (By.XPATH, "//button[@type='submit']")
            ]

            submit_button = None
            for selector in submit_selectors:
                try:
                    submit_button = self.wait.until(EC.element_to_be_clickable(selector))
                    logger.info(f"Found submit button with selector: {selector}")
                    break
                except TimeoutException:
                    continue

            if submit_button:
                # Пробуем обычный клик
                try:
                    submit_button.click()
                    logger.info("Submit button clicked successfully")
                except ElementClickInterceptedException:
                    # Пробуем клик через JavaScript
                    self.driver.execute_script("arguments[0].click();", submit_button)
                    logger.info("Submit button clicked via JavaScript")

                time.sleep(5)  # Ждем обработки формы
                return True
            else:
                raise Exception("Submit button not found")

        except Exception as e:
            logger.error(f"Failed to click submit button: {e}")

            # Пробуем отправить форму через JavaScript
            try:
                logger.info("Trying to submit form via JavaScript")
                form = self.driver.find_element(By.TAG_NAME, "form")
                self.driver.execute_script("arguments[0].submit();", form)
                logger.info("Form submitted via JavaScript")
                time.sleep(5)
                return True
            except Exception as js_e:
                logger.error(f"JavaScript form submission also failed: {js_e}")
                raise Exception(f"Submit button not found and form submission failed: {e}")

    @allure.step("Verify login success")
    def _verify_login_success(self):
        """Проверяет успешность логина"""
        try:
            logger.info("Verifying login success")

            print(f"After login attempt - URL: {self.driver.current_url}")
            print(f"After login attempt - Title: {self.driver.title}")

            # Делаем скриншот после попытки логина
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="after_login_attempt",
                attachment_type=allure.attachment_type.PNG
            )

            # Проверяем различные признаки успешного логина
            success_indicators = [
                "teachers.skyeng.ru" in self.driver.current_url,
                "schedule" in self.driver.current_url,
                self._is_element_present(self.USER_AVATAR),
                self._is_element_present(self.PROFILE_MENU),
                self._is_element_present(self.DASHBOARD_HEADER)
            ]

            if any(success_indicators):
                logger.info("🎉 LOGIN SUCCESSFUL!")
                print("🎉 LOGIN SUCCESSFUL!")
                return True
            else:
                logger.warning("Login might have failed or redirected elsewhere")
                print("⚠️ Login may have failed or redirected elsewhere")

                # Проверяем наличие ошибок
                error_message = self.get_error_message()
                if error_message:
                    logger.error(f"Login error: {error_message}")
                    raise Exception(f"Login failed: {error_message}")

                return False

        except Exception as e:
            logger.error(f"Error verifying login success: {e}")
            return False

    @allure.step("Check if login page is displayed")
    def is_login_page_displayed(self):
        """Проверяет, отображается ли страница логина"""
        try:
            current_url = self.driver.current_url
            is_login_page = (
                "id.skyeng.ru/login" in current_url or
                settings.LOGIN_PAGE in current_url or
                "auth" in current_url or
                "signin" in current_url
            )

            # Также проверяем наличие элементов логина на странице
            login_elements_present = (
                self._is_element_present(self.USERNAME_INPUT) or
                self._is_element_present(self.PASSWORD_INPUT) or
                self._is_element_present(self.SUBMIT_BUTTON)
            )

            return is_login_page and login_elements_present

        except Exception as e:
            logger.error(f"Error checking login page: {e}")
            return False

    @allure.step("Get error message")
    def get_error_message(self):
        """Получает сообщение об ошибке, если оно есть"""
        try:
            error_selectors = [
                self.ERROR_MESSAGE,
                self.ERROR_TEXT,
                self.AUTH_ERROR,
                (By.CLASS_NAME, "alert-error"),
                (By.CLASS_NAME, "validation-error"),
                (By.XPATH, "//*[contains(@class, 'error') and string-length(text()) > 0]"),
                (By.XPATH, "//*[contains(text(), 'Ошибка')]")
            ]

            for selector in error_selectors:
                try:
                    error_element = self.driver.find_element(*selector)
                    if error_element.is_displayed() and error_element.text.strip():
                        return error_element.text.strip()
                except NoSuchElementException:
                    continue

            return None

        except Exception as e:
            logger.error(f"Error getting error message: {e}")
            return None

    @allure.step("Login with invalid credentials")
    def login_with_invalid_credentials(self, email=None, password=None):
        """Выполняет вход с невалидными данными"""
        invalid_email = email or TestConstants.INVALID_EMAIL
        invalid_password = password or TestConstants.INVALID_PASSWORD

        logger.info(f"Attempting login with invalid credentials: {invalid_email}")

        try:
            return self.login(invalid_email, invalid_password)
        except Exception as e:
            logger.info(f"Expected login failure: {e}")
            # Для невалидных данных ожидаем исключение
            return False

    @allure.step("Click forgot password link")
    def click_forgot_password(self):
        """Нажимает на ссылку 'Забыли пароль'"""
        try:
            forgot_password_link = self.wait.until(
                EC.element_to_be_clickable(self.FORGOT_PASSWORD_LINK)
            )
            forgot_password_link.click()
            logger.info("Forgot password link clicked")
            time.sleep(3)
            return True
        except Exception as e:
            logger.error(f"Failed to click forgot password link: {e}")
            return False

    @allure.step("Check if social login buttons are visible")
    def are_social_buttons_visible(self):
        """Проверяет видимость кнопок социальных сетей"""
        try:
            social_buttons = [
                self.GOOGLE_BUTTON,
                self.APPLE_BUTTON,
                self.FACEBOOK_BUTTON
            ]

            visible_buttons = []
            for button in social_buttons:
                if self._is_element_present(button):
                    visible_buttons.append(button)

            return len(visible_buttons) > 0, visible_buttons

        except Exception as e:
            logger.error(f"Error checking social buttons: {e}")
            return False, []

    @allure.step("Get current page URL")
    def get_current_url(self):
        """Возвращает текущий URL"""
        return self.driver.current_url

    @allure.step("Get page title")
    def get_page_title(self):
        """Возвращает заголовок страницы"""
        return self.driver.title

    def _is_element_present(self, locator):
        """Вспомогательный метод для проверки наличия элемента"""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False

    @allure.step("Wait for page load")
    def wait_for_page_load(self, timeout=10):
        """Ожидает загрузки страницы"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            return True
        except TimeoutException:
            logger.warning(f"Page not fully loaded after {timeout} seconds")
            return False

    @allure.step("Take screenshot")
    def take_screenshot(self, name="screenshot"):
        """Делает скриншот текущей страницы"""
        try:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name=name,
                attachment_type=allure.attachment_type.PNG
            )
            return True
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
            return False

    @allure.step("Clear browser cookies")
    def clear_cookies(self):
        """Очищает cookies браузера"""
        try:
            self.driver.delete_all_cookies()
            logger.info("Browser cookies cleared")
            return True
        except Exception as e:
            logger.error(f"Failed to clear cookies: {e}")
            return False
