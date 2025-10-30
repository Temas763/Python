import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_URL = os.getenv('BASE_URL', 'https://ru.yougile.com')
    API_TOKEN = os.getenv('API_TOKEN')  # Токен обязателен для YouGile
    
    @property
    def headers(self):
        if not self.API_TOKEN:
            raise ValueError("API_TOKEN is required for YouGile API")
        
        return {
            'Authorization': f'Bearer {self.API_TOKEN}',
            'Content-Type': 'application/json'
        }