from typing import List, Dict, Any
from domain.models.agent import Agent

class Skill:
    def __init__(self, id: str, name: str, agent_id: str):
        self.id = id
        self.agent_id = agent_id
        self.name = name

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "agent_id": self.agent_id
        }

    @staticmethod
    def from_dict(skill_data: Dict[str, Any]) -> "Skill":
        return Skill(
            id=skill_data['id'],
            name=skill_data['name'],
            agent_id=skill_data['agent_id']
        )
