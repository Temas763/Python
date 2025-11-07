import requests
import allure
import json
from config.settings import settings


class APIClient:
    def __init__(self):
        self.base_url = settings.API_BASE_URL
        self.headers = {
            "Content-Type": "application/json",
            "Cookie": f"token_global={settings.TOKEN}"
        }

    @allure.step("GET request to {url}")
    def get(self, url, **kwargs):
        return requests.get(url, headers=self.headers, **kwargs)

    @allure.step("POST request to {url}")
    def post(self, url, data=None, **kwargs):
        return requests.post(url, json=data, headers=self.headers, **kwargs)

    @allure.step("PUT request to {url}")
    def put(self, url, data=None, **kwargs):
        return requests.put(url, json=data, headers=self.headers, **kwargs)

    @allure.step("DELETE request to {url}")
    def delete(self, url, **kwargs):
        return requests.delete(url, headers=self.headers, **kwargs)


class ScheduleAPI(APIClient):
    @allure.step("Get schedule events")
    def get_schedule_events(self, from_date, till_date):
        data = {
            "from": from_date,
            "till": till_date
        }
        return self.post(settings.SCHEDULE_EVENTS, data=data)

    @allure.step("Create personal event")
    def create_personal_event(self, event_data):
        return self.post(settings.CREATE_PERSONAL, data=event_data)

    @allure.step("Update personal event")
    def update_personal_event(self, event_data):
        return self.post(settings.UPDATE_PERSONAL, data=event_data)

    @allure.step("Remove personal event")
    def remove_personal_event(self, event_id, start_at):
        data = {
            "id": event_id,
            "startAt": start_at
        }
        return self.post(settings.REMOVE_PERSONAL, data=data)

    @allure.step("Get auth config")
    def get_auth_config(self):
        # Для этого endpoint используем другой базовый URL
        headers = self.headers.copy()
        return requests.post(
            settings.AUTH_CONFIG, 
            headers=headers,
            data=""
        )
