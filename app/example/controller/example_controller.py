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


@example_router.get("/", response_model=ApiListResponse[ExampleResponse])
async def get_examples(service: ExampleService = Depends(get_example_service)):
    """
    Get all examples

    Response:
    {
        "data": [...],
        "message": "get list success",
        "status": "200"
    }
    """
    examples = service.get_all()
    data = [ExampleResponse.model_validate(dto.to_dict()) for dto in examples]
    return ApiListResponse.success(data=data, message="get list success")


@example_router.get("/{example_id}", response_model=ApiResponse[ExampleResponse])
async def get_example(
    example_id: int, service: ExampleService = Depends(get_example_service)
):
    """
    Get example by ID

    Response:
    {
        "data": {...},
        "message": "get example success",
        "status": "200"
    }
    """
    dto = service.get_by_id(example_id)
    data = ExampleResponse.model_validate(dto.to_dict())
    return ApiResponse.success(data=data, message="get example success")


@example_router.post(
    "/", response_model=ApiResponse[ExampleResponse], status_code=status.HTTP_201_CREATED
)
async def create_example(
    request: ExampleCreateRequest,
    service: ExampleService = Depends(get_example_service),
):
    """
    Create a new example

    Response:
    {
        "data": {...},
        "message": "create success",
        "status": "201"
    }
    """
    dto = service.create(request)
    data = ExampleResponse.model_validate(dto.to_dict())
    return ApiResponse.success(data=data, message="create success", status="201")


@example_router.put("/{example_id}", response_model=ApiResponse[ExampleResponse])
async def update_example(
    example_id: int,
    request: ExampleUpdateRequest,
    service: ExampleService = Depends(get_example_service),
):
    """
    Update an existing example

    Response:
    {
        "data": {...},
        "message": "update success",
        "status": "200"
    }
    """
    dto = service.update(example_id, request)
    data = ExampleResponse.model_validate(dto.to_dict())
    return ApiResponse.success(data=data, message="update success")


@example_router.delete("/{example_id}", response_model=ApiResponse[None])
async def delete_example(
    example_id: int, service: ExampleService = Depends(get_example_service)
):
    """
    Delete example by ID

    Response:
    {
        "data": null,
        "message": "delete success",
        "status": "200"
    }
    """
    service.delete(example_id)
    return ApiResponse.success(data=None, message="delete success")
