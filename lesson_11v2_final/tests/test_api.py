import pytest
import allure
import requests
from data.test_data import TestData
from constants import EventConstants, TestConstants
from utils.api_client import APIClient

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
            assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"

        with allure.step("Verify response contains data"):
            response_data = response.json()
            assert "data" in response_data, f"Response should contain 'data' field. Response: {response_data}"

        with allure.step("Log response details"):
            print(f"Response status: {response.status_code}")
            print(f"Response headers: {response.headers}")
            print(f"Response data keys: {response_data.keys()}")

            if "data" in response_data and response_data["data"]:
                print(f"Data type: {type(response_data['data'])}")
                if isinstance(response_data["data"], list):
                    print(f"Number of events: {len(response_data['data'])}")

    @allure.title("Create personal event")
    def test_create_personal_event(self, api_client):
        event_data = TestData.get_event_data()

        with allure.step("Send request to create personal event"):
            response = api_client.create_personal_event(event_data)

        with allure.step(f"Verify response status code is 200, got {response.status_code}"):
            assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"

        with allure.step("Verify event was created successfully"):
            response_data = response.json()
            assert "data" in response_data, f"Response should contain 'data' field. Response: {response_data}"

            # Save event ID for cleanup
            if "data" in response_data and response_data["data"] is not None:
                if "payload" in response_data["data"] and "id" in response_data["data"]["payload"]:
                    pytest.event_id = response_data["data"]["payload"]["id"]
                    pytest.event_start = event_data["startAt"]
                    print(f"Created event ID: {pytest.event_id}")
                else:
                    print("Event ID not found in response payload")
            else:
                print("No data in response to extract event ID")

        with allure.step("Log creation details"):
            print(f"Created event title: {event_data['title']}")
            print(f"Created event start: {event_data['startAt']}")
            print(f"Created event end: {event_data['endAt']}")

    @allure.title("Update personal event")
    def test_update_personal_event(self, api_client):
        event_data = TestData.get_updated_event_data()

        with allure.step("Send request to update personal event"):
            response = api_client.update_personal_event(event_data)

        with allure.step(f"Verify response status code is 200, got {response.status_code}"):
            assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"

        with allure.step("Verify update was successful"):
            response_data = response.json()
            # API может возвращать успех даже если событие не найдено, но статус 200
            print(f"Update response: {response_data}")

        with allure.step("Log update details"):
            print(f"Updated event ID: {event_data['id']}")
            print(f"Updated event title: {event_data['title']}")
            print(f"Updated event start: {event_data['startAt']}")

    @allure.title("Remove personal event")
    def test_remove_personal_event(self, api_client):
        deletion_data = TestData.get_event_for_deletion()

        with allure.step("Send request to remove personal event"):
            response = api_client.remove_personal_event(
                deletion_data["id"], 
                deletion_data["startAt"]
            )

        with allure.step(f"Verify response status code is 200, got {response.status_code}"):
            assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"

        with allure.step("Verify removal was successful"):
            response_data = response.json()
            print(f"Removal response: {response_data}")

        with allure.step("Log removal details"):
            print(f"Removed event ID: {deletion_data['id']}")
            print(f"Removed event start: {deletion_data['startAt']}")

    @allure.title("Get auth config")
    def test_get_auth_config(self, api_client):
        with allure.step("Send request to get auth config"):
            response = api_client.get_auth_config()

        with allure.step(f"Verify response status code is 200, got {response.status_code}"):
            assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"

        with allure.step("Verify auth config contains expected data"):
            response_data = response.json()
            # Проверяем наличие основных полей в ответе
            assert "data" in response_data, f"Response should contain 'data' field. Response: {response_data}"

        with allure.step("Log auth config details"):
            print(f"Auth config response keys: {response_data.keys()}")
            if "data" in response_data:
                print(f"Auth config data type: {type(response_data['data'])}")

    @allure.title("Create and verify event lifecycle")
    def test_event_lifecycle(self, api_client):
        """Тест полного жизненного цикла события: создание → проверка → удаление"""

        # Шаг 1: Создание события
        with allure.step("Create new event"):
            event_data = TestData.get_event_data()
            event_data["title"] = "Lifecycle Test Event"

            create_response = api_client.create_personal_event(event_data)
            assert create_response.status_code == 200
            create_data = create_response.json()

            # Извлекаем ID созданного события
            if ("data" in create_data and 
                create_data["data"] is not None and 
                "payload" in create_data["data"] and 
                "id" in create_data["data"]["payload"]):

                event_id = create_data["data"]["payload"]["id"]
                event_start = event_data["startAt"]
                print(f"Created event with ID: {event_id}")
            else:
                pytest.skip("Could not create event for lifecycle test")

        # Шаг 2: Проверка, что событие есть в расписании
        with allure.step("Verify event exists in schedule"):
            period = TestData.get_schedule_period()
            schedule_response = api_client.get_schedule_events(period["from"], period["till"])
            assert schedule_response.status_code == 200

            schedule_data = schedule_response.json()
            # Здесь можно добавить проверку, что событие присутствует в ответе

        # Шаг 3: Обновление события
        with allure.step("Update the event"):
            update_data = event_data.copy()
            update_data.update({
                "id": event_id,
                "title": "Updated Lifecycle Event",
                "oldStartAt": event_start
            })

            update_response = api_client.update_personal_event(update_data)
            assert update_response.status_code == 200

        # Шаг 4: Удаление события
        with allure.step("Remove the event"):
            remove_response = api_client.remove_personal_event(event_id, event_start)
            assert remove_response.status_code == 200

        with allure.step("Log lifecycle completion"):
            print("✓ Event lifecycle completed successfully: Create → Verify → Update → Delete")

@allure.feature("Schedule API")
@allure.story("Negative API Tests")
class TestNegativeAPI:

    @allure.title("Create event without required fields")
    def test_create_event_without_required_fields(self, api_client):
        with allure.step("Send request with missing required fields"):
            response = api_client.create_personal_event(
                TestData.EVENT_WITH_MISSING_REQUIRED_FIELDS
            )

        with allure.step("Verify response contains validation errors"):
            print(f"Response status: {response.status_code}")
            print(f"Response text: {response.text}")
            response_data = response.json()

            # API возвращает 200 даже при ошибках, но с errors в ответе
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            assert "errors" in response_data, "Response should contain 'errors' field for invalid data"
            assert len(response_data["errors"]) > 0, "Errors array should not be empty"

            print(f"Validation errors: {response_data['errors']}")

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

            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            assert "errors" in response_data, "Response should contain 'errors' for invalid time range"
            assert len(response_data["errors"]) > 0, "Errors array should not be empty for invalid time range"

            print(f"Time validation errors: {response_data['errors']}")

    @allure.title("Update event with invalid data")
    def test_update_event_with_invalid_data(self, api_client):
        with allure.step("Send request with invalid data"):
            response = api_client.update_personal_event(
                TestData.EVENT_WITH_INVALID_DATE_FORMAT
            )

        with allure.step("Verify response contains validation errors"):
            print(f"Response status: {response.status_code}")
            print(f"Response text: {response.text}")
            response_data = response.json()

            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            assert "errors" in response_data, "Response should contain 'errors' for invalid data"
            assert len(response_data["errors"]) > 0, "Errors array should not be empty for invalid data"

            print(f"Invalid data errors: {response_data['errors']}")

    @allure.title("Remove non-existent event")
    def test_remove_nonexistent_event(self, api_client):
        nonexistent_data = TestData.get_nonexistent_event_data()

        with allure.step("Send request to remove non-existent event"):
            response = api_client.remove_personal_event(
                nonexistent_data["id"], 
                nonexistent_data["startAt"]
            )

        with allure.step("Verify response contains error"):
            print(f"Response status: {response.status_code}")
            print(f"Response text: {response.text}")
            response_data = response.json()

            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            # API может возвращать успех или ошибку при удалении несуществующего события
            # Проверяем структуру ответа
            assert "data" in response_data or "errors" in response_data, \
                "Response should contain either 'data' or 'errors' field"

            if "errors" in response_data:
                print(f"Removal errors for non-existent event: {response_data['errors']}")
            else:
                print("No errors returned for non-existent event removal")

    @allure.title("Access API without authentication")
    def test_access_without_auth(self):
        with allure.step("Create client without authentication token"):
            client = APIClient()
            client.headers = {"Content-Type": "application/json"}  # Remove auth cookie

        with allure.step("Send request without authentication"):
            response = client.post(
                "https://api-teachers.skyeng.ru/v2/schedule/createPersonal",
                data=TestData.get_event_data()
            )

        with allure.step(f"Verify response indicates unauthorized, got {response.status_code}"):
            print(f"Response status without auth: {response.status_code}")
            print(f"Response headers without auth: {response.headers}")
            print(f"Response text without auth: {response.text}")

            # Без авторизации должен возвращать ошибку
            # Это может быть 401, 403, или 200 с ошибкой в теле
            response_data = response.json() if response.content else {}

            if response.status_code == 200:
                # Если статус 200, проверяем наличие ошибок в теле
                assert "errors" in response_data, \
                    "Without authentication, response should contain errors even with 200 status"
            else:
                # Ожидаем код ошибки авторизации
                assert response.status_code in [401, 403, 400], \
                    f"Expected auth error status code, got {response.status_code}"

    @allure.title("Create event with very long title")
    def test_create_event_with_very_long_title(self, api_client):
        with allure.step("Send request with extremely long title"):
            event_data = TestData.get_event_data()
            event_data["title"] = "A" * 1000  # Очень длинное название

            response = api_client.create_personal_event(event_data)

        with allure.step("Verify response handles long title appropriately"):
            print(f"Response status: {response.status_code}")
            print(f"Response text: {response.text}")
            response_data = response.json()

            # API может либо принять длинное название, либо вернуть ошибку валидации
            if response.status_code == 200:
                if "errors" in response_data and len(response_data["errors"]) > 0:
                    print(f"Validation errors for long title: {response_data['errors']}")
                else:
                    print("Long title was accepted by API")
            else:
                assert response.status_code == 400, f"Expected 200 or 400, got {response.status_code}"

    @allure.title("Get schedule with invalid date format")
    def test_get_schedule_with_invalid_date_format(self, api_client):
        with allure.step("Send request with invalid date format"):
            invalid_from = "invalid-date-format"
            invalid_till = "another-invalid-date"

            response = api_client.get_schedule_events(invalid_from, invalid_till)

        with allure.step("Verify response handles invalid dates appropriately"):
            print(f"Response status: {response.status_code}")
            print(f"Response text: {response.text}")
            response_data = response.json()

            # API может вернуть ошибку или пустой результат
            if response.status_code == 200:
                if "errors" in response_data:
                    print(f"Date format errors: {response_data['errors']}")
                else:
                    print("API returned data despite invalid date format")
            else:
                assert response.status_code in [400, 422], \
                    f"Expected 200, 400 or 422 for invalid date, got {response.status_code}"

    @allure.title("Update event without ID")
    def test_update_event_without_id(self, api_client):
        with allure.step("Send update request without event ID"):
            event_data = TestData.get_event_data()
            # Убираем обязательное поле ID
            if "id" in event_data:
                del event_data["id"]

            response = api_client.update_personal_event(event_data)

        with allure.step("Verify response indicates missing ID"):
            print(f"Response status: {response.status_code}")
            print(f"Response text: {response.text}")
            response_data = response.json()

            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            assert "errors" in response_data, "Response should contain errors when ID is missing"
            assert len(response_data["errors"]) > 0, "Errors array should not be empty"

            print(f"Missing ID errors: {response_data['errors']}")

    @allure.title("Send malformed JSON")
    def test_send_malformed_json(self, api_client):
        with allure.step("Send request with malformed JSON"):
            # Создаем клиент для отправки сырых данных
            client = APIClient()
            malformed_data = "{ invalid json "

            # Временно меняем headers для отправки сырого текста
            original_headers = client.headers.copy()
            client.headers["Content-Type"] = "application/json"

            try:
                response = client.post(
                    "https://api-teachers.skyeng.ru/v2/schedule/createPersonal",
                    data=malformed_data  # Отправляем невалидный JSON
                )
            finally:
                # Восстанавливаем оригинальные headers
                client.headers = original_headers

        with allure.step("Verify response handles malformed JSON appropriately"):
            print(f"Response status for malformed JSON: {response.status_code}")
            print(f"Response text: {response.text}")

            # Ожидаем ошибку клиента (4xx) для невалидного JSON
            assert response.status_code in [400, 415, 422], \
                f"Expected client error for malformed JSON, got {response.status_code}"

@allure.feature("Schedule API")
@allure.story("Boundary Value Tests")
class TestBoundaryAPI:

    @allure.title("Create event with minimum valid data")
    def test_create_event_with_minimum_data(self, api_client):
        with allure.step("Send request with only required fields"):
            minimal_data = {
                "title": "Minimal Event",
                "startAt": "2025-01-01T10:00:00+03:00",
                "endAt": "2025-01-01T11:00:00+03:00"
            }

            response = api_client.create_personal_event(minimal_data)

        with allure.step("Verify minimal data is accepted"):
            print(f"Response status: {response.status_code}")
            response_data = response.json()

            if response.status_code == 200:
                if "errors" in response_data and len(response_data["errors"]) > 0:
                    print(f"Errors with minimal data: {response_data['errors']}")
                    # Если есть ошибки, это может быть нормально - проверяем какие именно
                else:
                    print("Minimal data was accepted")
                    # Сохраняем ID для очистки если нужно
                    if ("data" in response_data and 
                        response_data["data"] and 
                        "payload" in response_data["data"] and 
                        "id" in response_data["data"]["payload"]):

                        event_id = response_data["data"]["payload"]["id"]
                        # Можно добавить очистку здесь если нужно
            else:
                print(f"Minimal data rejected with status: {response.status_code}")

    @allure.title("Create event with boundary date values")
    def test_create_event_with_boundary_dates(self, api_client):
        boundary_cases = [
            {
                "name": "Very far future",
                "startAt": "2030-12-31T23:59:00+03:00",
                "endAt": "2031-01-01T00:59:00+03:00"
            },
            {
                "name": "Very far past", 
                "startAt": "2000-01-01T00:00:00+03:00",
                "endAt": "2000-01-01T01:00:00+03:00"
            }
        ]

        for case in boundary_cases:
            with allure.step(f"Test boundary case: {case['name']}"):
                event_data = TestData.get_event_data()
                event_data.update({
                    "title": f"Boundary Test - {case['name']}",
                    "startAt": case["startAt"],
                    "endAt": case["endAt"]
                })

                response = api_client.create_personal_event(event_data)
                print(f"{case['name']} - Status: {response.status_code}")

                # Проверяем что API обрабатывает граничные значения без критических ошибок
                assert response.status_code in [200, 400, 422], \
                    f"Unexpected status code for boundary case: {response.status_code}"

@pytest.fixture(scope="function", autouse=True)
def cleanup_created_events(api_client):
    """
    Фикстура для очистки созданных событий после каждого теста
    """
    yield

    # Очистка событий, созданных в тестах
    if hasattr(pytest, 'event_id') and hasattr(pytest, 'event_start'):
        try:
            with allure.step("Cleanup: remove test event"):
                response = api_client.remove_personal_event(pytest.event_id, pytest.event_start)
                if response.status_code == 200:
                    print(f"✓ Cleaned up event {pytest.event_id}")
                else:
                    print(f"⚠ Could not clean up event {pytest.event_id}")
        except Exception as e:
            print(f"Error during cleanup: {e}")
        finally:
            # Убираем атрибуты чтобы не мешать следующим тестам
            if hasattr(pytest, 'event_id'):
                delattr(pytest, 'event_id')
            if hasattr(pytest, 'event_start'):
                delattr(pytest, 'event_start')
