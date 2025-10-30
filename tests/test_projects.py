import pytest
import json

class TestProjects:
    
    @pytest.fixture
    def sample_project_data(self):
        """Данные для создания проекта в YouGile"""
        return {
            "title": "Test Project API",
            "description": "Test project created by automated tests"
        }
    
    @pytest.fixture
    def created_project_id(self, api_client, sample_project_data):
        """Фикстура для создания тестового проекта"""
        response = api_client.create_project(sample_project_data)
        
        if hasattr(api_client, 'test_mode') and api_client.test_mode:
            # В тестовом режиме используем mock ID
            if response.status_code == 201:
                data = response.json()
                project_id = data.get('id', 'mock-project-123')
            else:
                project_id = 'mock-project-123'
            print(f"🔧 TEST MODE: Using project ID: {project_id}")
            yield project_id
        elif response.status_code == 201:
            data = response.json()
            project_id = data.get('id')
            if project_id:
                print(f"✅ Created project with ID: {project_id}")
                yield project_id
            else:
                pytest.skip("Не удалось получить ID созданного проекта")
        else:
            pytest.skip(f"Не удалось создать проект для теста: {response.status_code} - {response.text}")
    
    # POSITIVE TESTS
    
    def test_create_project_positive(self, api_client, sample_project_data):
        """Позитивный тест создания проекта с валидными данными"""
        response = api_client.create_project(sample_project_data)
        
        assert response.status_code == 201, f"Ожидался статус 201, получен {response.status_code}. Response: {response.text}"
        
        data = response.json()
        assert 'id' in data, "Ответ должен содержать ID проекта"
        print(f"✅ Project created with ID: {data['id']}")
    
    def test_get_project_positive(self, api_client, created_project_id):
        """Позитивный тест получения информации о проекте"""
        response = api_client.get_project(created_project_id)
        
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}. Response: {response.text}"
        
        data = response.json()
        assert data['id'] == created_project_id
        print(f"✅ Project retrieved: {data.get('title', 'No title')}")
    
    def test_update_project_positive(self, api_client, created_project_id):
        """Позитивный тест обновления проекта"""
        update_data = {
            "title": "Updated Project Name",
            "description": "Updated project description"
        }
        
        response = api_client.update_project(created_project_id, update_data)
        
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}. Response: {response.text}"
        
        data = response.json()
        assert data['title'] == update_data['title']
        print(f"✅ Project updated successfully")
    
    # NEGATIVE TESTS - ИСПРАВЛЕННЫЕ
    
    def test_create_project_negative_empty_title(self, api_client):
        """Негативный тест создания проекта с пустым названием"""
        invalid_data = {
            "title": "",  # Пустое название
            "description": "Project with empty title"
        }
        
        response = api_client.create_project(invalid_data)
        
        # Ожидаем ошибку валидации
        assert response.status_code in [400, 422], f"Ожидалась ошибка 400 или 422, получен {response.status_code}"
        print(f"✅ Correctly rejected empty title with status {response.status_code}")
    
    def test_create_project_negative_missing_title(self, api_client):
        """Негативный тест создания проекта без названия"""
        invalid_data = {
            "description": "Project without title field"  # Нет поля title
        }
        
        response = api_client.create_project(invalid_data)
        
        # Ожидаем ошибку валидации
        assert response.status_code in [400, 422], f"Ожидалась ошибка 400 или 422, получен {response.status_code}"
        print(f"✅ Correctly rejected missing title with status {response.status_code}")
    
    def test_get_project_negative_not_found(self, api_client):
        """Негативный тест получения несуществующего проекта"""
        non_existent_id = "00000000-0000-0000-0000-000000000000"
        
        response = api_client.get_project(non_existent_id)
        
        assert response.status_code == 404, f"Ожидался статус 404, получен {response.status_code}"
        print(f"✅ Correctly returned 404 for non-existent project")
    
    def test_update_project_negative_invalid_data(self, api_client):
        """Негативный тест обновления проекта с невалидными данными"""
        update_data = {
            "title": "",  # Пустое название
        }
        
        # Используем любой ID для теста
        test_id = "test-project-123"
        response = api_client.update_project(test_id, update_data)
        
        assert response.status_code in [400, 422], f"Ожидалась ошибка валидации, получен {response.status_code}"
        print(f"✅ Correctly rejected invalid data with status {response.status_code}")