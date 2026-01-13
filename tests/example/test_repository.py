"""
Unit tests for ExampleRepository
"""
import pytest
from unittest.mock import MagicMock, patch
from app.example.repository.example_repository import ExampleRepository
from app.example.models.entity.example_entity import ExampleEntity


class TestExampleRepository:
    """Test cases for ExampleRepository"""

    def test_find_all_returns_list(self, mock_db_session):
        """Test find_all returns a list of entities"""
        # Arrange
        mock_entities = [MagicMock(spec=ExampleEntity), MagicMock(spec=ExampleEntity)]
        mock_db_session.query.return_value.all.return_value = mock_entities

        repository = ExampleRepository(mock_db_session)

        # Act
        result = repository.find_all()

        # Assert
        assert result == mock_entities
        mock_db_session.query.assert_called_once_with(ExampleEntity)

    def test_find_all_returns_empty_list(self, mock_db_session):
        """Test find_all returns empty list when no data"""
        # Arrange
        mock_db_session.query.return_value.all.return_value = []
        repository = ExampleRepository(mock_db_session)

        # Act
        result = repository.find_all()

        # Assert
        assert result == []

    def test_find_by_id_returns_entity(self, mock_db_session, sample_entity):
        """Test find_by_id returns entity when found"""
        # Arrange
        mock_db_session.query.return_value.filter.return_value.first.return_value = (
            sample_entity
        )
        repository = ExampleRepository(mock_db_session)

        # Act
        result = repository.find_by_id(1)

        # Assert
        assert result == sample_entity
        assert result.id == 1

    def test_find_by_id_returns_none(self, mock_db_session):
        """Test find_by_id returns None when not found"""
        # Arrange
        mock_db_session.query.return_value.filter.return_value.first.return_value = None
        repository = ExampleRepository(mock_db_session)

        # Act
        result = repository.find_by_id(999)

        # Assert
        assert result is None

    def test_save_creates_entity(self, mock_db_session, sample_entity):
        """Test save persists entity and returns it"""
        # Arrange
        repository = ExampleRepository(mock_db_session)

        # Act
        result = repository.save(sample_entity)

        # Assert
        mock_db_session.add.assert_called_once_with(sample_entity)
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once_with(sample_entity)
        assert result == sample_entity

    def test_delete_removes_entity(self, mock_db_session, sample_entity):
        """Test delete removes entity and returns True"""
        # Arrange
        repository = ExampleRepository(mock_db_session)

        # Act
        result = repository.delete(sample_entity)

        # Assert
        mock_db_session.delete.assert_called_once_with(sample_entity)
        mock_db_session.commit.assert_called_once()
        assert result is True

    def test_exists_by_id_returns_true(self, mock_db_session):
        """Test exists_by_id returns True when entity exists"""
        # Arrange
        mock_db_session.query.return_value.filter.return_value.count.return_value = 1
        repository = ExampleRepository(mock_db_session)

        # Act
        result = repository.exists_by_id(1)

        # Assert
        assert result is True

    def test_exists_by_id_returns_false(self, mock_db_session):
        """Test exists_by_id returns False when entity not exists"""
        # Arrange
        mock_db_session.query.return_value.filter.return_value.count.return_value = 0
        repository = ExampleRepository(mock_db_session)

        # Act
        result = repository.exists_by_id(999)

        # Assert
        assert result is False
