from datetime import datetime, timedelta
from constants import EventConstants, TimeConstants, TestConstants


class TestData:
    # Test event data
    @staticmethod
    def get_event_data():
        start_time = datetime.now() + timedelta(days=TimeConstants.DAYS_OFFSET_FUTURE)
        end_time = start_time + timedelta(hours=TimeConstants.HOURS_DURATION)

        return {
            "title": EventConstants.DEFAULT_EVENT_TITLE,
            "description": EventConstants.EVENT_DESCRIPTION,
            "startAt": start_time.strftime("%Y-%m-%dT%H:%M:%S+03:00"),
            "endAt": end_time.strftime("%Y-%m-%dT%H:%M:%S+03:00"),
            "backgroundColor": EventConstants.BACKGROUND_COLOR,
            "color": EventConstants.TEXT_COLOR
        }

    @staticmethod
    def get_schedule_period():
        from_date = datetime.now()
        till_date = from_date + timedelta(days=TimeConstants.SCHEDULE_PERIOD_DAYS)

        return {
            "from": from_date.strftime("%Y-%m-%dT00:00:00+03:00"),
            "till": till_date.strftime("%Y-%m-%dT00:00:00+03:00")
        }

    @staticmethod
    def get_updated_event_data():
        """Данные для обновления события"""
        event_data = TestData.get_event_data()
        event_data.update({
            "title": EventConstants.UPDATED_EVENT_TITLE,
            "id": EventConstants.EXISTING_EVENT_ID,
            "oldStartAt": EventConstants.EXISTING_EVENT_START
        })
        return event_data

    @staticmethod
    def get_event_for_deletion():
        """Данные для удаления события"""
        return {
            "id": EventConstants.EVENT_TO_DELETE_ID,
            "startAt": EventConstants.EVENT_TO_DELETE_START
        }

    # Invalid data for negative tests
    INVALID_EVENT_DATA = {
        "title": "A" * 1000,  # Very long title
        "startAt": "invalid_date",
        "endAt": "invalid_date"
    }

    EVENT_WITH_START_AFTER_END = {
        "title": "Invalid Time Event",
        "startAt": "2025-05-27T20:30:00+03:00",
        "endAt": "2025-05-27T20:00:00+03:00",
        "backgroundColor": EventConstants.BACKGROUND_COLOR,
        "color": EventConstants.TEXT_COLOR
    }

    EVENT_WITH_MISSING_REQUIRED_FIELDS = {
        "title": "Test Event",
        "description": "Test Description"
        # Missing startAt and endAt - required fields
    }

    EVENT_WITH_INVALID_DATE_FORMAT = {
        "title": "Invalid Date Event",
        "startAt": "invalid_date_format",
        "endAt": "invalid_date_format",
        "id": EventConstants.EXISTING_EVENT_ID,
        "oldStartAt": EventConstants.EXISTING_EVENT_START
    }

    @staticmethod
    def get_nonexistent_event_data():
        """Данные для несуществующего события"""
        return {
            "id": TestConstants.NON_EXISTENT_EVENT_ID,
            "startAt": EventConstants.EVENT_TO_DELETE_START
        }

    @staticmethod
    def get_invalid_credentials():
        """Невалидные учетные данные"""
        return {
            "email": TestConstants.INVALID_EMAIL,
            "password": TestConstants.INVALID_PASSWORD
        }

    @staticmethod
    def get_window_sizes():
        """Размеры окон для тестирования responsive design"""
        return {
            "desktop": {"width": 1920, "height": 1080},
            "tablet": {"width": 768, "height": 1024},
            "mobile": {"width": 375, "height": 667}
        }
