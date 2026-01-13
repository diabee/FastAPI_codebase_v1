"""
Unit tests for API Response models
"""
import pytest
from app.models.response import ApiResponse, ApiListResponse


class TestApiResponse:
    """Test cases for ApiResponse"""

    def test_success_with_data(self):
        """Test success response with data"""
        # Arrange
        data = {"id": 1, "name": "Test"}

        # Act
        result = ApiResponse.success(data=data, message="success")

        # Assert
        assert result.data == data
        assert result.message == "success"
        assert result.status == "200"

    def test_success_with_custom_status(self):
        """Test success response with custom status"""
        # Arrange
        data = {"id": 1}

        # Act
        result = ApiResponse.success(data=data, message="created", status="201")

        # Assert
        assert result.status == "201"
        assert result.message == "created"

    def test_error_response(self):
        """Test error response"""
        # Act
        result = ApiResponse.error(message="Not found", status="404")

        # Assert
        assert result.data is None
        assert result.message == "Not found"
        assert result.status == "404"


class TestApiListResponse:
    """Test cases for ApiListResponse"""

    def test_success_with_list_data(self):
        """Test success response with list data"""
        # Arrange
        data = [{"id": 1}, {"id": 2}]

        # Act
        result = ApiListResponse.success(data=data)

        # Assert
        assert result.data == data
        assert result.message == "get list success"
        assert result.status == "200"

    def test_success_with_empty_list(self):
        """Test success response with empty list"""
        # Act
        result = ApiListResponse.success(data=[])

        # Assert
        assert result.data == []

    def test_success_with_none_defaults_to_empty_list(self):
        """Test success with None defaults to empty list"""
        # Act
        result = ApiListResponse.success(data=None)

        # Assert
        assert result.data == []
