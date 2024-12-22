from typing import List, Dict, Any
from domain.models.agent import Agent

class Traits:
    def __init__(self, id: str, traits: List[str], agent_id: str):
        self.id = id
        self.agent_id = agent_id
        self.traits = traits

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "agent_id": self.agent_id,
            "traits": self.traits
        }

    @staticmethod
    def from_dict(trait_data: Dict[str, Any]) -> "Traits":
        return Traits(
            id=trait_data['id'],
            agent_id=trait_data['agent_id'],
            traits=trait_data['traits']
        )
