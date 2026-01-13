# Example API 開發教學

本專案採用 **分層架構 (Layered Architecture)**，遵循 Clean Architecture 原則，實現關注點分離。

## 架構概述

```
┌─────────────────────────────────────────────────────────┐
│                    HTTP Request                         │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  Controller (接收 Schema，回傳 Schema)                  │
│  - 處理 HTTP 請求/回應                                   │
│  - 依賴注入 Service                                     │
│  - 使用 Pydantic Schema 驗證輸入輸出                     │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  Service (接收 Schema，回傳 DTO)                        │
│  - 商業邏輯處理                                         │
│  - 依賴 Repository 進行資料存取                          │
│  - 使用 DTO 作為回傳型別                                │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  Repository (操作 Entity)                               │
│  - 封裝資料庫操作                                       │
│  - 只負責 CRUD 操作                                     │
│  - 回傳 Entity 或 None                                  │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  Database (Entity ↔ Table)                              │
└─────────────────────────────────────────────────────────┘
```

## 目錄結構

```
src/example/
├── controller/
│   └── example_controller.py    # HTTP 端點
├── service/
│   └── example_service.py       # 商業邏輯
├── repository/
│   └── example_repository.py    # 資料庫操作
└── models/
    ├── entity/
    │   └── example_entity.py    # SQLAlchemy ORM Model
    ├── schema/
    │   └── example_schema.py    # Pydantic Request/Response
    └── dto/
        └── example_dto.py       # Data Transfer Object (POJO)
```

---

## Step 1: 建立 Entity (ORM Model)

Entity 代表資料庫表格的映射，使用 SQLAlchemy 定義。

```python
# src/example/models/entity/example_entity.py
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from src.config.db_config import Base


class ExampleEntity(Base):
    """資料庫 Entity - 對應 examples 表"""

    __tablename__ = "examples"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
```

> **重要**: 新增 Entity 後，需要在 `main.py` 中導入以自動建立資料表。

---

## Step 2: 建立 Schema (Request/Response 驗證)

Schema 使用 Pydantic 定義，用於 API 輸入輸出驗證。

```python
# src/example/models/schema/example_schema.py
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class ExampleCreateRequest(BaseModel):
    """建立請求 - 輸入驗證"""
    name: str = Field(..., min_length=1, max_length=255, description="名稱")
    description: Optional[str] = Field(None, description="描述")


class ExampleUpdateRequest(BaseModel):
    """更新請求 - 輸入驗證"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None


class ExampleResponse(BaseModel):
    """回應格式 - 輸出驗證"""
    id: int
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # 允許從 ORM 物件轉換


class ExampleListResponse(BaseModel):
    """列表回應格式"""
    data: List[ExampleResponse]
    total: int
```

---

## Step 3: 建立 DTO (Data Transfer Object)

DTO 是純粹的資料容器 (POJO)，用於層與層之間傳遞資料。

```python
# src/example/models/dto/example_dto.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ExampleDTO:
    """DTO - 層間資料傳遞物件"""
    
    id: Optional[int] = None
    name: str = ""
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_entity(cls, entity) -> "ExampleDTO":
        """Entity → DTO 轉換"""
        return cls(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def to_dict(self) -> dict:
        """DTO → dict 轉換 (供 Schema 使用)"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
```

---

## Step 4: 建立 Repository (資料庫操作)

Repository 封裝所有資料庫操作，只負責 CRUD。

```python
# src/example/repository/example_repository.py
from typing import List, Optional
from sqlalchemy.orm import Session
from src.example.models.entity.example_entity import ExampleEntity


class ExampleRepository:
    """Repository - 資料庫操作層"""

    def __init__(self, db: Session):
        self.db = db

    def find_all(self) -> List[ExampleEntity]:
        """查詢所有"""
        return self.db.query(ExampleEntity).all()

    def find_by_id(self, example_id: int) -> Optional[ExampleEntity]:
        """依 ID 查詢"""
        return self.db.query(ExampleEntity).filter(
            ExampleEntity.id == example_id
        ).first()

    def save(self, entity: ExampleEntity) -> ExampleEntity:
        """儲存 (新增或更新)"""
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def delete(self, entity: ExampleEntity) -> bool:
        """刪除"""
        self.db.delete(entity)
        self.db.commit()
        return True
```

---

## Step 5: 建立 Service (商業邏輯)

Service 處理商業邏輯，透過 Repository 存取資料。

```python
# src/example/service/example_service.py
from typing import List, Optional
from src.example.models.dto.example_dto import ExampleDTO
from src.example.models.entity.example_entity import ExampleEntity
from src.example.models.schema.example_schema import ExampleCreateRequest
from src.example.repository.example_repository import ExampleRepository


class ExampleService:
    """Service - 商業邏輯層"""

    def __init__(self, repository: ExampleRepository):
        self.repository = repository

    def get_all(self) -> List[ExampleDTO]:
        """取得所有並轉換為 DTO"""
        entities = self.repository.find_all()
        return [ExampleDTO.from_entity(e) for e in entities]

    def get_by_id(self, example_id: int) -> Optional[ExampleDTO]:
        """依 ID 查詢"""
        entity = self.repository.find_by_id(example_id)
        return ExampleDTO.from_entity(entity) if entity else None

    def create(self, request: ExampleCreateRequest) -> ExampleDTO:
        """
        建立新資料
        1. 接收 Schema (已驗證的請求)
        2. 建立 Entity
        3. 透過 Repository 儲存
        4. 回傳 DTO
        """
        entity = ExampleEntity(
            name=request.name,
            description=request.description,
        )
        saved = self.repository.save(entity)
        return ExampleDTO.from_entity(saved)

    def delete(self, example_id: int) -> bool:
        """刪除"""
        entity = self.repository.find_by_id(example_id)
        if not entity:
            return False
        return self.repository.delete(entity)
```

---

## Step 6: 建立 Controller (HTTP 端點)

Controller 處理 HTTP 請求，使用依賴注入取得 Service。

```python
# src/example/controller/example_controller.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.config.db_config import get_db_session
from src.example.models.schema.example_schema import (
    ExampleCreateRequest, ExampleResponse, ExampleListResponse
)
from src.example.repository.example_repository import ExampleRepository
from src.example.service.example_service import ExampleService

example_router = APIRouter(prefix="/api/v1/examples", tags=["Example"])


def get_example_service(db: Session = Depends(get_db_session)) -> ExampleService:
    """依賴注入：建立 Service (自動注入 Repository)"""
    repository = ExampleRepository(db)
    return ExampleService(repository)


@example_router.post("/", response_model=ExampleResponse, status_code=status.HTTP_201_CREATED)
async def create_example(
    request: ExampleCreateRequest,
    service: ExampleService = Depends(get_example_service),
):
    """
    建立新 Example
    
    資料流: Schema → Service → Repository → Entity → DTO → Schema
    """
    dto = service.create(request)
    return ExampleResponse.model_validate(dto.to_dict())


@example_router.get("/", response_model=ExampleListResponse)
async def get_examples(service: ExampleService = Depends(get_example_service)):
    """取得所有 Examples"""
    examples = service.get_all()
    return ExampleListResponse(
        data=[ExampleResponse.model_validate(dto.to_dict()) for dto in examples],
        total=len(examples),
    )
```

---

## Step 7: 註冊路由

在 `router_config.py` 中註冊 Controller。

```python
# src/config/router_config.py
from src.example.controller.example_controller import example_router


class RoutesConfig:
    def __init__(self, app):
        app.include_router(example_router)
```

---

## 測試 API

### POST /api/v1/examples/

```bash
curl -X POST http://localhost:8000/api/v1/examples/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Example", "description": "This is a test"}'
```

**回應:**
```json
{
  "id": 1,
  "name": "Test Example",
  "description": "This is a test",
  "created_at": "2026-01-13T11:30:00",
  "updated_at": "2026-01-13T11:30:00"
}
```

### GET /api/v1/examples/

```bash
curl http://localhost:8000/api/v1/examples/
```

---

## 物件角色對照表

| 物件類型 | 用途 | 位置 |
|---------|------|------|
| **Entity** | ORM 資料庫映射 | `models/entity/` |
| **Schema** | API 輸入/輸出驗證 | `models/schema/` |
| **DTO** | 層間資料傳遞 (POJO) | `models/dto/` |
| **Repository** | 資料庫 CRUD 操作 | `repository/` |
| **Service** | 商業邏輯處理 | `service/` |
| **Controller** | HTTP 端點處理 | `controller/` |

---

## 新增功能 Checklist

建立新功能時，依照以下順序：

- [ ] 建立 Entity (`models/entity/xxx_entity.py`)
- [ ] 在 `main.py` 導入 Entity (自動建表)
- [ ] 建立 Schema (`models/schema/xxx_schema.py`)
- [ ] 建立 DTO (`models/dto/xxx_dto.py`)
- [ ] 建立 Repository (`repository/xxx_repository.py`)
- [ ] 建立 Service (`service/xxx_service.py`)
- [ ] 建立 Controller (`controller/xxx_controller.py`)
- [ ] 在 `router_config.py` 註冊路由
