import pytest
from config import Config

@pytest.fixture
def config():
    return Config()

@pytest.fixture
def api_client():
    from api.projects_api import ProjectsAPI
    return ProjectsAPI()