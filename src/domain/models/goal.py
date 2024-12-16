from typing import Any, Dict

from domain.models.kpi import KPI


class Goal:
    def __init__(self, goal_id: str, agent_id: str, goal: str, kpis: list[KPI] = []):
        self.id = goal_id
        self.agent_id = agent_id
        self.goal = goal
        self.kpis = kpis

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "agent_id": self.agent_id,
            "goal": self.goal,
            "kpis": [kpi.to_dict() for kpi in self.kpis]
        }
        
    @staticmethod
    def from_dict(goal_data: Dict[str, Any]) -> "Goal":
        return Goal(
            goal_id=goal_data["id"] if "id" in goal_data else None,
            agent_id=goal_data["agent_id"] if "agent_id" in goal_data else None,
            goal=goal_data["goal"],
            kpis=[KPI.from_dict(kpi_data) for kpi_data in goal_data["kpis"]] if "kpis" in goal_data else []
        )