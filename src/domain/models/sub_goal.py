from typing import Any, Dict

from domain.models.kpi import KPI

class SubGoal:
    def __init__(self, sub_goal_id: str, goal_id: str, agent_id: str, sub_goal: str, kpis: list[KPI] = []):
        self.id = sub_goal_id
        self.goal_id = goal_id
        self.agent_id = agent_id
        self.sub_goal = sub_goal
        self.kpis = kpis

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "goal_id": self.goal_id,
            "agent_id": self.agent_id,
            "sub_goal": self.sub_goal,
            "kpis": [kpi.to_dict() for kpi in self.kpis]
        }
    
    @staticmethod
    def from_dict(sub_goal_data: Dict[str, Any]) -> "SubGoal":
        return SubGoal(
            sub_goal_id=sub_goal_data["id"] if "id" in sub_goal_data else None,
            goal_id=sub_goal_data["goal_id"] if "goal_id" in sub_goal_data else None,
            agent_id=sub_goal_data["agent_id"] if "agent_id" in sub_goal_data else None,
            sub_goal=sub_goal_data["sub_goal"],
            kpis=[KPI.from_dict(kpi_data) for kpi_data in sub_goal_data["kpis"]] if "kpis" in sub_goal_data else []
        )