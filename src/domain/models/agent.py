from typing import Any, Dict
from domain.models.kpi import KPI

class Agent:
    def __init__(self, id: str, user_id: str, role: str, description: dict,
                 kpis: list[KPI], feedbacks: list = [], available_apis: list = [], 
                 team_id: str = None, category_id: str = None):  
        self.id = id
        self.user_id = user_id
        self.role = role
        self.description = description
        self.feedbacks = feedbacks
        self.kpis = kpis
        self.available_apis = available_apis
        self.team_id = team_id
        self.category_id = category_id

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "role": self.role,
            "description": self.description,
            "feedbacks": self.feedbacks,
            "kpis": [kpi.to_dict() for kpi in self.kpis],
            "available_apis": self.available_apis,
            "team_id": self.team_id,
            "category_id": self.category_id
        }

    @staticmethod
    def from_dict(agent_data: Dict[str, Any]) -> "Agent":
        return Agent(
            id=agent_data['id'],
            user_id=agent_data['user_id'],
            role=agent_data['role'],
            description=agent_data['description'],
            feedbacks=agent_data.get('feedbacks', []),
            kpis=[KPI.from_dict(kpi) for kpi in agent_data.get('kpis', [])],
            available_apis=agent_data.get('available_apis', []),
            team_id=agent_data.get('team_id'),
            category_id=agent_data.get('category_id')
        )
