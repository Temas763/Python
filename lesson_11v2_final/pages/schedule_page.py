from selenium.webdriver.common.by import By
from .base_page import BasePage
import allure


class SchedulePage(BasePage):
    # Более общие локаторы для Skyeng
    PAGE_CONTAINER = (By.TAG_NAME, "body")
    LOADING_INDICATOR = (By.CLASS_NAME, "loading")  # или другой индикатор загрузки

    # Попробуем разные возможные локаторы для элементов расписания
    CALENDAR = (By.CLASS_NAME, "calendar")
    SCHEDULE_CONTAINER = (By.CLASS_NAME, "schedule")
    TIMETABLE = (By.CLASS_NAME, "timetable")

    # Кнопки и элементы
    ADD_BUTTON = (By.XPATH, "//button[contains(., 'Добавить') or contains(., 'Add')]")
    CREATE_BUTTON = (By.XPATH, "//button[contains(., 'Создать') or contains(., 'Create')]")
    EVENT_CARD = (By.CLASS_NAME, "event")  # карточка события

    @allure.step("Check if schedule page is loaded")
    def is_schedule_loaded(self):
        """Проверяем, загружена ли страница расписания"""
        try:
            # Проверяем наличие body и что страница загружена
            self.find_element(self.PAGE_CONTAINER)

            # Проверяем различные возможные контейнеры расписания
            schedule_loaded = any([
                self.is_element_visible(self.CALENDAR),
                self.is_element_visible(self.SCHEDULE_CONTAINER),
                self.is_element_visible(self.TIMETABLE),
                "schedule" in self.driver.current_url,
                "calendar" in self.driver.current_url
            ])

            return schedule_loaded
        except Exception as e:
            print(f"Error checking schedule load: {e}")
            return False

    @allure.step("Get events count")
    def get_events_count(self):
        try:
            return len(self.driver.find_elements(*self.EVENT_CARD))
        except:
            return 0

    @allure.step("Check if user is logged in")
    def is_logged_in(self):
        """Проверяем, авторизован ли пользователь"""
        try:
            # Проверяем различные признаки авторизации
            current_url = self.driver.current_url
            not_logged_in_indicators = [
                "login" in current_url,
                "auth" in current_url,
                "signin" in current_url
            ]

            return not any(not_logged_in_indicators)
        except:
            return False
