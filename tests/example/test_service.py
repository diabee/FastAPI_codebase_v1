"""
Unit tests for ExampleService
"""
import pytest
from unittest.mock import MagicMock, patch
from app.example.service.example_service import ExampleService
from app.example.repository.example_repository import ExampleRepository
from app.example.models.entity.example_entity import ExampleEntity
from app.example.models.schema.example_schema import (
    ExampleCreateRequest,
    ExampleUpdateRequest,
)
from app.example.exception import ExampleNotFoundException


class TestExampleService:
    """Test cases for ExampleService"""

    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository"""
        return MagicMock(spec=ExampleRepository)

    @pytest.fixture
    def service(self, mock_repository):
        """Create service with mock repository"""
        return ExampleService(mock_repository)

    @pytest.fixture
    def sample_entity(self):
        """Sample entity for testing"""
        entity = MagicMock(spec=ExampleEntity)
        entity.id = 1
        entity.name = "Test"
        entity.description = "Test Description"
        entity.created_at = None
        entity.updated_at = None
        return entity

    def test_get_all_returns_dtos(self, service, mock_repository, sample_entity):
        """Test get_all returns list of DTOs"""
        # Arrange
        mock_repository.find_all.return_value = [sample_entity]

        # Act
        result = service.get_all()

        # Assert
        assert len(result) == 1
        assert result[0].id == 1
        assert result[0].name == "Test"
        mock_repository.find_all.assert_called_once()

    def test_get_all_returns_empty_list(self, service, mock_repository):
        """Test get_all returns empty list when no data"""
        # Arrange
        mock_repository.find_all.return_value = []

        # Act
        result = service.get_all()

        # Assert
        assert result == []

    def test_get_by_id_returns_dto(self, service, mock_repository, sample_entity):
        """Test get_by_id returns DTO when found"""
        # Arrange
        mock_repository.find_by_id.return_value = sample_entity

        # Act
        result = service.get_by_id(1)

        # Assert
        assert result.id == 1
        assert result.name == "Test"
        mock_repository.find_by_id.assert_called_once_with(1)

    def test_get_by_id_raises_not_found(self, service, mock_repository):
        """Test get_by_id raises exception when not found"""
        # Arrange
        mock_repository.find_by_id.return_value = None

        # Act & Assert
        with pytest.raises(ExampleNotFoundException):
            service.get_by_id(999)

    def test_create_returns_dto(self, service, mock_repository, sample_entity):
        """Test create returns DTO after saving"""
        # Arrange
        request = ExampleCreateRequest(name="Test", description="Test Description")
        mock_repository.save.return_value = sample_entity

        # Act
        result = service.create(request)

        # Assert
        assert result.id == 1
        assert result.name == "Test"
        mock_repository.save.assert_called_once()

    def test_update_returns_dto(self, service, mock_repository, sample_entity):
        """Test update returns updated DTO"""
        # Arrange
        request = ExampleUpdateRequest(name="Updated Name")
        mock_repository.find_by_id.return_value = sample_entity
        mock_repository.save.return_value = sample_entity

        # Act
        result = service.update(1, request)

        # Assert
        assert result is not None
        mock_repository.find_by_id.assert_called_once_with(1)
        mock_repository.save.assert_called_once()

    def test_update_raises_not_found(self, service, mock_repository):
        """Test update raises exception when entity not found"""
        # Arrange
        request = ExampleUpdateRequest(name="Updated Name")
        mock_repository.find_by_id.return_value = None

        # Act & Assert
        with pytest.raises(ExampleNotFoundException):
            service.update(999, request)

    def test_delete_returns_true(self, service, mock_repository, sample_entity):
        """Test delete returns True on success"""
        # Arrange
        mock_repository.find_by_id.return_value = sample_entity
        mock_repository.delete.return_value = True

        # Act
        result = service.delete(1)

        # Assert
        assert result is True
        mock_repository.delete.assert_called_once_with(sample_entity)

    def test_delete_raises_not_found(self, service, mock_repository):
        """Test delete raises exception when entity not found"""
        # Arrange
        mock_repository.find_by_id.return_value = None

        # Act & Assert
        with pytest.raises(ExampleNotFoundException):
            service.delete(999)

    def test_exists_returns_true(self, service, mock_repository):
        """Test exists returns True when entity exists"""
        # Arrange
        mock_repository.exists_by_id.return_value = True

        # Act
        result = service.exists(1)

        # Assert
        assert result is True

    def test_exists_returns_false(self, service, mock_repository):
        """Test exists returns False when entity not exists"""
        # Arrange
        mock_repository.exists_by_id.return_value = False

        # Act
        result = service.exists(999)

        # Assert
        assert result is False
