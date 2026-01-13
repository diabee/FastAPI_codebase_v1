"""
Unit tests for DTO models
"""
import pytest
from unittest.mock import MagicMock
from datetime import datetime
from app.example.models.dto.example_dto import ExampleDTO
from app.example.models.entity.example_entity import ExampleEntity


class TestExampleDTO:
    """Test cases for ExampleDTO"""

    def test_from_entity_converts_correctly(self):
        """Test from_entity creates DTO from entity"""
        # Arrange
        entity = MagicMock(spec=ExampleEntity)
        entity.id = 1
        entity.name = "Test Name"
        entity.description = "Test Description"
        entity.created_at = datetime(2026, 1, 13, 12, 0, 0)
        entity.updated_at = datetime(2026, 1, 13, 12, 0, 0)

        # Act
        dto = ExampleDTO.from_entity(entity)

        # Assert
        assert dto.id == 1
        assert dto.name == "Test Name"
        assert dto.description == "Test Description"
        assert dto.created_at == datetime(2026, 1, 13, 12, 0, 0)
        assert dto.updated_at == datetime(2026, 1, 13, 12, 0, 0)

    def test_to_dict_returns_correct_dict(self):
        """Test to_dict returns correct dictionary"""
        # Arrange
        dto = ExampleDTO(
            id=1,
            name="Test Name",
            description="Test Description",
            created_at=datetime(2026, 1, 13, 12, 0, 0),
            updated_at=datetime(2026, 1, 13, 12, 0, 0),
        )

        # Act
        result = dto.to_dict()

        # Assert
        assert result["id"] == 1
        assert result["name"] == "Test Name"
        assert result["description"] == "Test Description"
        assert result["created_at"] == datetime(2026, 1, 13, 12, 0, 0)
        assert result["updated_at"] == datetime(2026, 1, 13, 12, 0, 0)

    def test_dto_with_defaults(self):
        """Test DTO with default values"""
        # Act
        dto = ExampleDTO()

        # Assert
        assert dto.id is None
        assert dto.name == ""
        assert dto.description is None
        assert dto.created_at is None
        assert dto.updated_at is None
