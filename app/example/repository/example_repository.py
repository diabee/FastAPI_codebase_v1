from typing import List, Optional
from sqlalchemy.orm import Session

from app.example.models.entity.example_entity import ExampleEntity


class ExampleRepository:
    """Repository for database operations on ExampleEntity"""

    def __init__(self, db: Session):
        self.db = db

    def find_all(self) -> List[ExampleEntity]:
        """Retrieve all examples from database"""
        return self.db.query(ExampleEntity).all()

    def find_by_id(self, example_id: int) -> Optional[ExampleEntity]:
        """Find example by ID"""
        return (
            self.db.query(ExampleEntity)
            .filter(ExampleEntity.id == example_id)
            .first()
        )

    def find_by_name(self, name: str) -> Optional[ExampleEntity]:
        """Find example by name"""
        return (
            self.db.query(ExampleEntity)
            .filter(ExampleEntity.name == name)
            .first()
        )

    def save(self, entity: ExampleEntity) -> ExampleEntity:
        """Save (create or update) an entity"""
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def delete(self, entity: ExampleEntity) -> bool:
        """Delete an entity"""
        self.db.delete(entity)
        self.db.commit()
        return True

    def exists_by_id(self, example_id: int) -> bool:
        """Check if entity exists by ID"""
        return (
            self.db.query(ExampleEntity)
            .filter(ExampleEntity.id == example_id)
            .count()
            > 0
        )
