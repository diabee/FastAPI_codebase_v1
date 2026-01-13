from fastapi import APIRouter, Depends, status

from app.example.models.schema.example_schema import (
    ExampleCreateRequest,
    ExampleUpdateRequest,
    ExampleResponse,
)
from app.example.service.example_service import ExampleService
from app.example.dependencies import get_example_service
from app.models.response import ApiResponse, ApiListResponse

example_router = APIRouter(prefix="/api/v1/examples", tags=["Example"])


@example_router.get(
    "/",
    response_model=ApiListResponse[ExampleResponse],
    summary="取得所有 Examples",
    description="取得所有 Example 資料列表",
)
async def get_examples(service: ExampleService = Depends(get_example_service)):
    """取得所有 Examples"""
    examples = service.get_all()
    data = [ExampleResponse.model_validate(dto.to_dict()) for dto in examples]
    return ApiListResponse.success(data=data, message="get list success")


@example_router.get(
    "/{example_id}",
    response_model=ApiResponse[ExampleResponse],
    summary="取得單一 Example",
    description="根據 ID 取得單一 Example 資料",
)
async def get_example(
    example_id: int, service: ExampleService = Depends(get_example_service)
):
    """取得單一 Example"""
    dto = service.get_by_id(example_id)
    data = ExampleResponse.model_validate(dto.to_dict())
    return ApiResponse.success(data=data, message="get example success")


@example_router.post(
    "/",
    response_model=ApiResponse[ExampleResponse],
    status_code=status.HTTP_201_CREATED,
    summary="建立新 Example",
    description="建立一筆新的 Example 資料",
)
async def create_example(
    request: ExampleCreateRequest,
    service: ExampleService = Depends(get_example_service),
):
    """建立新 Example"""
    dto = service.create(request)
    data = ExampleResponse.model_validate(dto.to_dict())
    return ApiResponse.success(data=data, message="create success", status="201")


@example_router.put(
    "/{example_id}",
    response_model=ApiResponse[ExampleResponse],
    summary="更新 Example",
    description="根據 ID 更新現有 Example 資料",
)
async def update_example(
    example_id: int,
    request: ExampleUpdateRequest,
    service: ExampleService = Depends(get_example_service),
):
    """更新 Example"""
    dto = service.update(example_id, request)
    data = ExampleResponse.model_validate(dto.to_dict())
    return ApiResponse.success(data=data, message="update success")


@example_router.delete(
    "/{example_id}",
    response_model=ApiResponse[None],
    summary="刪除 Example",
    description="根據 ID 刪除 Example 資料",
)
async def delete_example(
    example_id: int, service: ExampleService = Depends(get_example_service)
):
    """刪除 Example"""
    service.delete(example_id)
    return ApiResponse.success(data=None, message="delete success")
