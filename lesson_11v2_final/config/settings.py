import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Base URLs
    BASE_URL = "https://teachers.skyeng.ru"
    API_BASE_URL = "https://api-teachers.skyeng.ru"
    SKYENG_ID_URL = "https://id.skyeng.ru"

    # Auth data
    EMAIL = "test.tst345@skyeng.ru"
    PASSWORD = "2DbhAAPG6q"
    TOKEN = os.getenv("SKYENG_TOKEN", "your_token_here")

    # Browser settings
    BROWSER = os.getenv("BROWSER", "chrome")
    HEADLESS = os.getenv("HEADLESS", "False").lower() == "true"
    TIMEOUT = 10

    # API endpoints - исправленные пути
    SCHEDULE_EVENTS = f"{API_BASE_URL}/v2/schedule/events"
    CREATE_PERSONAL = f"{API_BASE_URL}/v2/schedule/createPersonal"
    UPDATE_PERSONAL = f"{API_BASE_URL}/v2/schedule/updatePersonal"
    REMOVE_PERSONAL = f"{API_BASE_URL}/v2/schedule/removePersonal"
    AUTH_CONFIG = f"{BASE_URL}/users/api/v2/auth/config"

    # UI endpoints
    SCHEDULE_PAGE = f"{BASE_URL}/schedule"
    LOGIN_PAGE = f"{SKYENG_ID_URL}/login"


settings = Settings()
