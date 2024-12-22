from typing import List, Dict, Any
from domain.models.agent import Agent

class Skill:
    def __init__(self, id: str, skill: [] , agent_id: str):
        self.id = id
        self.agent_id = agent_id
        self.skills = skill

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "agent_id": self.agent_id,
            "skills": self.skills
        }

    @staticmethod
    def from_dict(skill_data: Dict[str, Any]) -> "Skill":
        return Skill(
            id=skill_data['id'],
            agent_id=skill_data['agent_id'],
            skill=skill_data['skills']
        )
