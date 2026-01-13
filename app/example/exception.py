from fastapi import HTTPException


class ExampleNotFoundException(HTTPException):
    """Exception raised when example is not found"""

    def __init__(self, example_id: int):
        super().__init__(
            status_code=404,
            detail=f"Example with id {example_id} not found",
        )


class ExampleValidationError(HTTPException):
    """Exception raised when example validation fails"""

    def __init__(self, message: str):
        super().__init__(
            status_code=400,
            detail=message,
        )
