import json
from typing import Any


class JsonUtility:
    """Utility class for JSON operations"""

    def __init__(self):
        pass

    def to_json(self, obj: Any) -> str:
        """Convert object to JSON string"""
        return json.dumps(obj, ensure_ascii=False, default=str)

    def from_json(self, json_str: str) -> Any:
        """Convert JSON string to object"""
        return json.loads(json_str)

    def to_dict(self, pydantic_model) -> dict:
        """Convert Pydantic model to dictionary"""
        return json.loads(pydantic_model.json())
