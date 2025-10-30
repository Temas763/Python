import requests
import json

# Данные для авторизации - ЗАМЕНИТЕ на свои реальные
auth_data = {
    "login": "temas7@yandex.ru",  # ЗАМЕНИТЕ на ваш email
    "password": "zDk-2nV-Y9Y-SUKpython get_token.py"         # ЗАМЕНИТЕ на ваш пароль
}

try:
    response = requests.post(
        "https://ru.yougile.com/api-v2/auth/keys",
        json=auth_data,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 201:
        token_data = response.json()
        api_token = token_data['key']
        print(f"\n🎉 Ваш API токен: {api_token}")
        print(f"\n📝 Добавьте эту строку в .env файл:")
        print(f"API_TOKEN={api_token}")
    else:
        print("❌ Ошибка получения токена")
        
except Exception as e:
    print(f"❌ Ошибка: {e}")