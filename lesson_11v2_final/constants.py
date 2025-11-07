"""
Константы для тестирования Skyeng Teachers
"""


class EventConstants:
    # ID тестовых событий (должны быть актуальными для тестовой среды)
    EXISTING_EVENT_ID = 100859699
    EXISTING_EVENT_START = "2025-05-27T20:00:00+03:00"
    EVENT_TO_DELETE_ID = 100861623
    EVENT_TO_DELETE_START = "2025-05-23T19:30:00+03:00"

    # Тексты событий
    DEFAULT_EVENT_TITLE = "Test Event"
    UPDATED_EVENT_TITLE = "Updated Event"
    EVENT_DESCRIPTION = "Test Description"

    # Цвета событий
    BACKGROUND_COLOR = "#F4F5F6"
    TEXT_COLOR = "#81888D"


class TestConstants:


    # Тестовые данные
    INVALID_EMAIL = "invalid@email.com"
    INVALID_PASSWORD = "wrongpassword123"
    NON_EXISTENT_PAGE = "/nonexistent-page"

    # ID для негативных тестов
    NON_EXISTENT_EVENT_ID = 999999


class TimeConstants:
    # Смещения времени для тестовых событий
    DAYS_OFFSET_FUTURE = 1
    HOURS_DURATION = 1
    SCHEDULE_PERIOD_DAYS = 7
