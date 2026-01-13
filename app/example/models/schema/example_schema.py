from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ExampleCreateRequest(BaseModel):
    """Request schema for creating an example"""

    name: str = Field(..., min_length=1, max_length=255, description="Example name")
    description: Optional[str] = Field(None, description="Example description")


class ExampleUpdateRequest(BaseModel):
    """Request schema for updating an example"""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None


class ExampleResponse(BaseModel):
    """Response schema for an example"""

    id: int
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

