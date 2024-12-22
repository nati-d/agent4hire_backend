from typing import Dict, Any, List

class Category:
    def __init__(self, id: str, name: str, description: str, agent_id: str = None):
        self.id = id
        self.name = name
        self.description = description
        self.agent_id = agent_id

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "agent_id": self.agent_id
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Category":
        return Category(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            agent_id=data.get('agent_id')
        )

# Predefined categories
AGENT_CATEGORIES = [
    {
        "name": "Personal Assistant",
        "description": "Helps with daily tasks, scheduling, and organization"
    },
    {
        "name": "Knowledge Expert",
        "description": "Specializes in specific domains of knowledge and research"
    },
    {
        "name": "Creative Assistant",
        "description": "Assists with creative tasks, content creation, and ideation"
    },
    {
        "name": "Business Analyst",
        "description": "Helps with business analysis, strategy, and decision making"
    },
    {
        "name": "Technical Expert",
        "description": "Specializes in technical tasks, programming, and system design"
    },
    {
        "name": "Education Assistant",
        "description": "Helps with learning, teaching, and educational content"
    },
    {
        "name": "Healthcare Assistant",
        "description": "Assists with health-related information and wellness tracking"
    },
    {
        "name": "Financial Advisor",
        "description": "Helps with financial planning, analysis, and advice"
    }
]
