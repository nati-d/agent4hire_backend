from typing import Any, Dict
import uuid

from domain.models.kpi import KPI
from domain.models.module import Module


class Workstream:
    def __init__(self, work_stream_id: str, sub_goal_id: str, goal_id: str, agent_id: str, workstream: str, modules: list[Module], frequency: str, kpis: list[KPI] = []):
        self.id = work_stream_id
        self.sub_goal_id = sub_goal_id
        self.goal_id = goal_id
        self.agent_id = agent_id
        self.workstream = workstream
        self.modules = modules
        self.frequency = frequency
        self.kpis = kpis

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "sub_goal_id": self.sub_goal_id,
            "goal_id": self.goal_id,
            "agent_id": self.agent_id,
            "workstream": self.workstream,
            "modules": [module.to_dict() for module in self.modules],
            "frequency": self.frequency,
            "kpis": [kpi.to_dict() for kpi in self.kpis]
        }
    
    @staticmethod
    def from_dict(workstream_data: Dict[str, Any]) -> "Workstream":
        return Workstream(
            work_stream_id=workstream_data["id"] if "id" in workstream_data else None,
            sub_goal_id=workstream_data["sub_goal_id"] if "sub_goal_id" in workstream_data else None,
            goal_id=workstream_data["goal_id"] if "goal_id" in workstream_data else None,
            agent_id=workstream_data["agent_id"] if "agent_id" in workstream_data else None,
            workstream=workstream_data["workstream"],
            modules=[Module.from_dict(module_data) for module_data in workstream_data["modules"]],
            frequency=workstream_data["frequency"],
            kpis=[KPI.from_dict(kpi_data) for kpi_data in workstream_data["kpis"]] if "kpis" in workstream_data else []
        )