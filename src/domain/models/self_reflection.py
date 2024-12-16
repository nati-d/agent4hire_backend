from typing import Any, Dict, List
from domain.models.goal import Goal
from domain.models.sub_goal import SubGoal
from domain.models.workstream import Workstream
from domain.models.skill import Skill


class SelfReflection:
    def __init__(
        self,
        id: str,
        user_id: str,
        agent_id: str,
        role: str,
        description: dict,
        available_apis: list = [],
        interactions: list = [],
        workstreams: List[Workstream] = [],
        goals: List[Goal] = [],
        subgoals: List[SubGoal] = [],
        skills: List[Skill] = [],
    ) -> None:
        self.id = id
        self.user_id = user_id
        self.agent_id = agent_id
        self.role = role
        self.description = description
        self.available_apis = available_apis
        self.interactions = interactions
        self.workstreams = workstreams
        self.goals = goals
        self.subgoals = subgoals
        self.skills = []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "agent_id": self.agent_id,
            "role": self.role,
            "description": self.description,
            "available_apis": self.available_apis,
            "interactions": self.interactions,
            # Convert each nested object to dictionary
            "workstreams": [workstream.to_dict() if hasattr(workstream, 'to_dict') else workstream for workstream in self.workstreams] if self.workstreams else [],
            "goals": [goal.to_dict() if hasattr(goal, 'to_dict') else goal for goal in self.goals] if self.goals else [],
            "subgoals": [subgoal.to_dict() if hasattr(subgoal, 'to_dict') else subgoal for subgoal in self.subgoals] if self.subgoals else [],
            "skills": [skill.to_dict() if hasattr(skill, 'to_dict') else skill for skill in self.skills] if self.skills else []
        }

    @staticmethod
    def from_dict(self_reflection_data: Dict[str, Any]) -> "SelfReflection":
        # Convert dictionary data back to object instances
        workstreams = [
            Workstream.from_dict(workstream_data)
            for workstream_data in self_reflection_data.get("workstreams", [])
        ] if "workstreams" in self_reflection_data else []
        
        goals = [
            Goal.from_dict(goal_data)
            for goal_data in self_reflection_data.get("goals", [])
        ] if "goals" in self_reflection_data else []
        
        subgoals = [
            SubGoal.from_dict(subgoal_data)
            for subgoal_data in self_reflection_data.get("subgoals", [])
        ] if "subgoals" in self_reflection_data else []
        
        skills = [
            Skill.from_dict(skill_data)
            for skill_data in self_reflection_data.get("skills", [])
        ] if "skills" in self_reflection_data else []
        

        return SelfReflection(
            id=self_reflection_data.get("id"),
            user_id=self_reflection_data.get("user_id"),
            agent_id=self_reflection_data.get("agent_id"),
            role=self_reflection_data.get("role"),
            description=self_reflection_data.get("description", {}),
            available_apis=self_reflection_data.get("available_apis", []),
            interactions=self_reflection_data.get("interactions", []),
            workstreams=workstreams,
            goals=goals,
            subgoals=subgoals,
            skills=skills
        )