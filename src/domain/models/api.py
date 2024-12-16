from typing import Any, Dict


class API:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description
        }
    
    @staticmethod   
    def from_dict(api_data: Dict[str, Any]) -> "API":
        return API(
            name=api_data["name"],
            description=api_data["description"]
        )