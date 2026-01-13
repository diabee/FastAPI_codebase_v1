"""
Pytest configuration and fixtures
"""
import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from app.main import app
from app.config.db_config import get_db_session
from app.example.repository.example_repository import ExampleRepository
from app.example.service.example_service import ExampleService
from app.example.models.entity.example_entity import ExampleEntity


@pytest.fixture
def mock_db_session():
    """Mock database session"""
    return MagicMock(spec=Session)


@pytest.fixture
def mock_repository(mock_db_session):
    """Mock repository with mocked db session"""
    return ExampleRepository(mock_db_session)


@pytest.fixture
def mock_service(mock_repository):
    """Mock service with mocked repository"""
    return ExampleService(mock_repository)


@pytest.fixture
def sample_entity():
    """Sample ExampleEntity for testing"""
    entity = ExampleEntity(
        name="Test Example",
        description="Test Description",
    )
    entity.id = 1
    return entity


@pytest.fixture
def client():
    """Test client for API testing"""
    return TestClient(app)


@pytest.fixture
def override_db_session():
    """Override database session dependency for testing"""
    mock_session = MagicMock(spec=Session)

    def _get_mock_db():
        yield mock_session

    app.dependency_overrides[get_db_session] = _get_mock_db
    yield mock_session
    app.dependency_overrides.clear()
