import json
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

from domain.models.goal import Goal


class GoalRepository:

    def __init__(self):
        self.database = firestore.Client(database='agent-square')
        self._collection_name = "goals"

    def create_goal(self, goal_data: Goal) -> None:
        try:
            self.database.collection(self._collection_name).document(
                goal_data.id).set(goal_data.to_dict())
        except Exception as e:
            raise e

    def get_goal(self, goal_id: str) -> Goal:
        try:
            goal = self.database.collection(
                self._collection_name).document(goal_id).get()
            return Goal.from_dict(goal.to_dict())
        except Exception as e:
            raise e

    def get_goals(self) -> list:
        try:
            goals = self.database.collection(self._collection_name).stream()
            return [Goal.from_dict(goal.to_dict()) for goal in goals]
        except Exception as e:
            raise e

    def update_goal(self, goal_data: Goal) -> None:
        try:
            self.database.collection(self._collection_name).document(
                goal_data.id).update(goal_data.to_dict())
        except Exception as e:
            raise e

    def get_goals_by_agent_id(self, agent_id: str) -> list:
        try:
            goals = self.database.collection(self._collection_name).where(
                filter=FieldFilter("agent_id", "==", agent_id)).stream()
            
            return [Goal.from_dict(goal.to_dict()) for goal in goals]
        except Exception as e:
            raise e

    def add_performance_data(self, goal_id: str,
                             performance_data: dict) -> None:
        try:
            self.database.collection("goal_performance").document(goal_id).set(
                performance_data)
        except Exception as e:
            raise e

    def get_performance_data(self, goal_id: str) -> list:
        try:
            performance_data = self.database.collection("goal_performance").document(goal_id).get()
            if performance_data.exists == False:
                return {}
            return performance_data.to_dict()
        except Exception as e:
            raise e
