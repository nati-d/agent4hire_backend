from typing import List, Dict, Any
from domain.models.agent import Agent

class Tags:
    def __init__(self, id: str, tags: List[str], agent_id: str):
        self.id = id
        self.agent_id = agent_id
        self.tags = tags

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "agent_id": self.agent_id,
            "tags": self.tags
        }

    @staticmethod
    def from_dict(tag_data: Dict[str, Any]) -> "Tags":
        return Tags(
            id=tag_data['id'],
            agent_id=tag_data['agent_id'],
            tags=tag_data['tags']
        )
