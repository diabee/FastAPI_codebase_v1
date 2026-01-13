from typing import Generic, TypeVar, Optional, List, Any
from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """
    統一 API 回應格式
    
    Example:
    {
        "data": [...],
        "message": "get list success",
        "status": "200"
    }
    """
    data: Optional[T] = None
    message: str = "success"
    status: str = "200"

    @classmethod
    def success(
        cls,
        data: T = None,
        message: str = "success",
        status: str = "200",
    ) -> "ApiResponse[T]":
        """建立成功回應"""
        return cls(data=data, message=message, status=status)

    @classmethod
    def error(
        cls,
        message: str,
        status: str,
        data: T = None,
    ) -> "ApiResponse[T]":
        """建立錯誤回應"""
        return cls(data=data, message=message, status=status)


class ApiListResponse(BaseModel, Generic[T]):
    """
    統一列表 API 回應格式
    
    Example:
    {
        "data": [{"name": "新增", "value": "add"}],
        "message": "get list success",
        "status": "200"
    }
    """
    data: List[T] = []
    message: str = "success"
    status: str = "200"

    @classmethod
    def success(
        cls,
        data: List[T] = None,
        message: str = "get list success",
        status: str = "200",
    ) -> "ApiListResponse[T]":
        """建立成功回應"""
        return cls(data=data or [], message=message, status=status)
