from typing import List

from app.example.exception import ExampleNotFoundException
from app.example.models.dto.example_dto import ExampleDTO
from app.example.models.entity.example_entity import ExampleEntity
from app.example.models.schema.example_schema import (
    ExampleCreateRequest,
    ExampleUpdateRequest,
)
from app.example.repository.example_repository import ExampleRepository


class ExampleService:
    """Service layer for business logic - uses Repository for data access"""

    def __init__(self, repository: ExampleRepository):
        self.repository = repository

    def get_all(self) -> List[ExampleDTO]:
        """Get all examples and convert to DTOs"""
        entities = self.repository.find_all()
        return [ExampleDTO.from_entity(entity) for entity in entities]

    def get_by_id(self, example_id: int) -> ExampleDTO:
        """Get example by ID and convert to DTO"""
        entity = self.repository.find_by_id(example_id)
        if not entity:
            raise ExampleNotFoundException(example_id)
        return ExampleDTO.from_entity(entity)

    def create(self, request: ExampleCreateRequest) -> ExampleDTO:
        """
        Create a new example
        - Receives Schema (validated request)
        - Creates Entity
        - Saves via Repository
        - Returns DTO
        """
        entity = ExampleEntity(
            name=request.name,
            description=request.description,
        )
        saved_entity = self.repository.save(entity)
        return ExampleDTO.from_entity(saved_entity)

    def update(self, example_id: int, request: ExampleUpdateRequest) -> ExampleDTO:
        """
        Update an existing example
        - Receives Schema (validated request)
        - Finds Entity via Repository
        - Updates and saves
        - Returns DTO
        """
        entity = self.repository.find_by_id(example_id)
        if not entity:
            raise ExampleNotFoundException(example_id)

        if request.name is not None:
            entity.name = request.name
        if request.description is not None:
            entity.description = request.description

        saved_entity = self.repository.save(entity)
        return ExampleDTO.from_entity(saved_entity)

    def delete(self, example_id: int) -> bool:
        """Delete an example by ID"""
        entity = self.repository.find_by_id(example_id)
        if not entity:
            raise ExampleNotFoundException(example_id)
        return self.repository.delete(entity)

    def exists(self, example_id: int) -> bool:
        """Check if example exists"""
        return self.repository.exists_by_id(example_id)
