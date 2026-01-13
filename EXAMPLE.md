# Example API 開發教學

本專案採用 **分層架構 (Layered Architecture)**，遵循 Clean Architecture 原則。

## 架構概述

```
HTTP Request
     ↓
Controller (Schema 驗證) → Service (商業邏輯) → Repository (資料庫) → Database
     ↓
HTTP Response (統一格式)
```

## 目錄結構

```
app/example/
├── controller/
│   └── example_controller.py    # API 端點
├── service/
│   └── example_service.py       # 商業邏輯
├── repository/
│   └── example_repository.py    # 資料庫操作
├── models/
│   ├── entity/                  # SQLAlchemy Entity
│   ├── schema/                  # Pydantic Schema
│   └── dto/                     # Data Transfer Object
├── dependencies.py              # 依賴注入
└── exception.py                 # 例外處理
```

---

## 新增功能步驟

### Step 1: 建立 Entity

```python
# app/example/models/entity/example_entity.py
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.config.db_config import Base

class ExampleEntity(Base):
    __tablename__ = "examples"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
```

> **重要**: 在 `main.py` 中導入 Entity 以自動建表。

### Step 2: 建立 Schema

```python
# app/example/models/schema/example_schema.py
from pydantic import BaseModel, Field
from typing import Optional

class ExampleCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None

class ExampleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True
```

### Step 3: 建立 DTO

```python
# app/example/models/dto/example_dto.py
from dataclasses import dataclass

@dataclass
class ExampleDTO:
    id: int = None
    name: str = ""
    description: str = None

    @classmethod
    def from_entity(cls, entity) -> "ExampleDTO":
        return cls(id=entity.id, name=entity.name, description=entity.description)

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "description": self.description}
```

### Step 4: 建立 Repository

```python
# app/example/repository/example_repository.py
from sqlalchemy.orm import Session
from app.example.models.entity.example_entity import ExampleEntity

class ExampleRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_all(self):
        return self.db.query(ExampleEntity).all()

    def find_by_id(self, id: int):
        return self.db.query(ExampleEntity).filter(ExampleEntity.id == id).first()

    def save(self, entity: ExampleEntity):
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity
```

### Step 5: 建立 Service

```python
# app/example/service/example_service.py
from app.example.repository.example_repository import ExampleRepository
from app.example.models.dto.example_dto import ExampleDTO

class ExampleService:
    def __init__(self, repository: ExampleRepository):
        self.repository = repository

    def get_all(self):
        entities = self.repository.find_all()
        return [ExampleDTO.from_entity(e) for e in entities]

    def create(self, request):
        entity = ExampleEntity(name=request.name, description=request.description)
        saved = self.repository.save(entity)
        return ExampleDTO.from_entity(saved)
```

### Step 6: 建立 Dependencies

```python
# app/example/dependencies.py
from fastapi import Depends
from sqlalchemy.orm import Session
from app.config.db_config import get_db_session
from app.example.repository.example_repository import ExampleRepository
from app.example.service.example_service import ExampleService

def get_example_service(db: Session = Depends(get_db_session)) -> ExampleService:
    repository = ExampleRepository(db)
    return ExampleService(repository)
```

### Step 7: 建立 Controller

```python
# app/example/controller/example_controller.py
from fastapi import APIRouter, Depends, status
from app.example.dependencies import get_example_service
from app.models.response import ApiResponse

example_router = APIRouter(prefix="/api/v1/examples", tags=["Example"])

@example_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_example(request: ExampleCreateRequest, service = Depends(get_example_service)):
    dto = service.create(request)
    return ApiResponse.success(data=dto.to_dict(), message="create success", status="201")
```

### Step 8: 註冊路由

```python
# app/config/router_config.py
from app.example.controller.example_controller import example_router

class RoutesConfig:
    def __init__(self, app):
        app.include_router(example_router)
```

---

## API 回應格式

所有 API 使用統一回應格式：

```json
{
  "data": {...},
  "message": "success",
  "status": "200"
}
```

---

## 新增功能 Checklist

- [ ] 建立 Entity (`models/entity/`)
- [ ] 在 `main.py` 導入 Entity
- [ ] 建立 Schema (`models/schema/`)
- [ ] 建立 DTO (`models/dto/`)
- [ ] 建立 Repository (`repository/`)
- [ ] 建立 Service (`service/`)
- [ ] 建立 Dependencies (`dependencies.py`)
- [ ] 建立 Controller (`controller/`)
- [ ] 在 `router_config.py` 註冊路由
