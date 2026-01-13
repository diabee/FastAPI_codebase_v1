"""
Dependency Injection module for Example feature
"""
from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.db_config import get_db_session
from app.example.repository.example_repository import ExampleRepository
from app.example.service.example_service import ExampleService


def get_example_service(db: Session = Depends(get_db_session)) -> ExampleService:
    """Dependency injection for ExampleService"""
    repository = ExampleRepository(db)
    return ExampleService(repository)
