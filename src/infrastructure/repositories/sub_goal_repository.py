import json
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

from domain.models.sub_goal import SubGoal

class SubGoalRepository:
    def __init__(self):
        self.database = firestore.Client(database='agent-square')
        self._collection_name = "sub_goals"

    def create_sub_goal(self, sub_goal_data: SubGoal) -> None:
        try:
            self.database.collection(self._collection_name).document(sub_goal_data.id).set(sub_goal_data.to_dict())
        except Exception as e:
            raise e
        
    def get_sub_goal(self, sub_goal_id: str) -> SubGoal:
        try:
            sub_goal = self.database.collection(self._collection_name).document(sub_goal_id).get()
            return SubGoal.from_dict(sub_goal.to_dict())
        except Exception as e:
            raise e
        
    def get_sub_goals(self) -> list:
        try:
            sub_goals = self.database.collection(self._collection_name).stream()
            return [SubGoal.from_dict(sub_goal.to_dict()) for sub_goal in sub_goals]
        except Exception as e:
            raise e
    
    def update_sub_goal(self, sub_goal_data: SubGoal) -> None:
        try:
            self.database.collection(self._collection_name).document(sub_goal_data.id).update(sub_goal_data.to_dict())
        except Exception as e:
            raise e
    
    def get_sub_goals_by_goal_id(self, goal_id: str) -> list:
        try:
            sub_goals = self.database.collection(self._collection_name).where(
                filter=FieldFilter("goal_id", "==", goal_id)).stream()
            return [SubGoal.from_dict(sub_goal.to_dict()) for sub_goal in sub_goals]
        except Exception as e:
            raise e
        
    def add_performance_data(self, sub_goal_id: str, performance_data: dict) -> None:
        try:
            self.database.collection("sub_goal_performance").document(sub_goal_id).set(performance_data)
        except Exception as e:
            raise e
        
    def get_performance_data(self, sub_goal_id: str) -> list:
        try:
            performance_data = self.database.collection("sub_goal_performance").document(sub_goal_id).get()
            if performance_data.exists == False:
                return {}
            return performance_data.to_dict()
        except Exception as e:
            raise e