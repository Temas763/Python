import pytest
import allure
from data.test_data import TestData

@allure.feature("Schedule API")
@allure.story("Positive API Tests")
class TestPositiveAPI:
    
    @allure.title("Get schedule events")
    def test_get_schedule_events(self, api_client):
        period = TestData.get_schedule_period()
        
        with allure.step("Send request to get schedule events"):
            response = api_client.get_schedule_events(
                period["from"], 
                period["till"]
            )
        
        with allure.step(f"Verify response status code is 200, got {response.status_code}"):
            assert response.status_code == 200
        
        with allure.step("Verify response contains data"):
            response_data = response.json()
            assert "data" in response_data
    
    @allure.title("Create personal event")
    def test_create_personal_event(self, api_client):
        event_data = TestData.get_event_data()
        
        with allure.step("Send request to create personal event"):
            response = api_client.create_personal_event(event_data)
        
        with allure.step(f"Verify response status code is 200, got {response.status_code}"):
            assert response.status_code == 200
        
        with allure.step("Verify event was created successfully"):
            response_data = response.json()
            assert "data" in response_data
            
            # Save event ID for cleanup
            if "data" in response_data and response_data["data"] is not None:
                if "payload" in response_data["data"] and "id" in response_data["data"]["payload"]:
                    pytest.event_id = response_data["data"]["payload"]["id"]
                    pytest.event_start = event_data["startAt"]
    
    @allure.title("Update personal event")
    def test_update_personal_event(self, api_client):
        event_data = TestData.get_event_data()
        event_data.update({
            "title": "Updated Event",
            "id": 100859699,
            "oldStartAt": "2025-05-27T20:00:00+03:00"
        })
        
        with allure.step("Send request to update personal event"):
            response = api_client.update_personal_event(event_data)
        
        with allure.step(f"Verify response status code is 200, got {response.status_code}"):
            assert response.status_code == 200
    
    @allure.title("Remove personal event")
    def test_remove_personal_event(self, api_client):
        event_id = 100861623
        start_at = "2025-05-23T19:30:00+03:00"
        
        with allure.step("Send request to remove personal event"):
            response = api_client.remove_personal_event(event_id, start_at)
        
        with allure.step(f"Verify response status code is 200, got {response.status_code}"):
            assert response.status_code == 200
    
    @allure.title("Get auth config")
    def test_get_auth_config(self, api_client):
        with allure.step("Send request to get auth config"):
            response = api_client.get_auth_config()
        
        with allure.step(f"Verify response status code is 200, got {response.status_code}"):
            assert response.status_code == 200

@allure.feature("Schedule API")
@allure.story("Negative API Tests")
class TestNegativeAPI:
    
    @allure.title("Create event without required fields")
    def test_create_event_without_required_fields(self, api_client):
        invalid_data = {
            "title": "Test Event",
            "description": "Test Description"
            # Missing startAt and endAt
        }
        
        with allure.step("Send request with missing required fields"):
            response = api_client.create_personal_event(invalid_data)
        
        with allure.step("Verify response contains validation errors"):
            print(f"Response status: {response.status_code}")
            print(f"Response text: {response.text}")
            response_data = response.json()
            
            # API возвращает 200 даже при ошибках, но с errors в ответе
            assert response.status_code == 200
            assert "errors" in response_data
            assert len(response_data["errors"]) > 0
    
    @allure.title("Create event with start time after end time")
    def test_create_event_start_after_end(self, api_client):
        with allure.step("Send request with invalid time range"):
            response = api_client.create_personal_event(
                TestData.EVENT_WITH_START_AFTER_END
            )
        
        with allure.step("Verify response contains validation errors"):
            print(f"Response status: {response.status_code}")
            print(f"Response text: {response.text}")
            response_data = response.json()
            
            assert response.status_code == 200
            assert "errors" in response_data
            assert len(response_data["errors"]) > 0
    
    @allure.title("Update event with invalid data")
    def test_update_event_with_invalid_data(self, api_client):
        invalid_data = {
            "title": "A" * 1000,  # Very long title
            "startAt": "invalid_date_format",
            "endAt": "invalid_date_format",
            "id": 100859699,
            "oldStartAt": "2025-06-29T7:30:00+03:00"
        }
        
        with allure.step("Send request with invalid data"):
            response = api_client.update_personal_event(invalid_data)
        
        with allure.step("Verify response contains validation errors"):
            print(f"Response status: {response.status_code}")
            print(f"Response text: {response.text}")
            response_data = response.json()
            
            assert response.status_code == 200
            assert "errors" in response_data
            assert len(response_data["errors"]) > 0
    
    @allure.title("Remove non-existent event")
    def test_remove_nonexistent_event(self, api_client):
        with allure.step("Send request to remove non-existent event"):
            response = api_client.remove_personal_event(999999, "2025-05-23T19:30:00+03:00")
        
        with allure.step("Verify response contains error"):
            print(f"Response status: {response.status_code}")
            print(f"Response text: {response.text}")
            response_data = response.json()
            
            assert response.status_code == 200
            assert "errors" in response_data
            assert len(response_data["errors"]) > 0
    
    @allure.title("Access API without authentication")
    def test_access_without_auth(self):
        from utils.api_client import APIClient
        client = APIClient()
        client.headers = {"Content-Type": "application/json"}  # Remove auth cookie
        
        with allure.step("Send request without authentication"):
            response = client.post(
                "https://api-teachers.skyeng.ru/v2/schedule/createPersonal",
                data=TestData.get_event_data()
            )
        
        with allure.step(f"Verify response indicates unauthorized, got {response.status_code}"):
            print(f"Response status: {response.status_code}")
            print(f"Response text: {response.text}")
            # Без авторизации должен возвращать ошибку
            assert response.status_code != 200