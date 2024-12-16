import json
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

from domain.models.workstream import Workstream

class WorkstreamRepository:
    def __init__(self):
        self.database = firestore.Client(database='agent-square')
        self._collection_name = "workstreams"

    def create_workstream(self, workstream_data: Workstream) -> None:
        try:
            self.database.collection(self._collection_name).document(workstream_data.id).set(workstream_data.to_dict())
        except Exception as e:
            raise e
        
    def get_workstream(self, workstream_id: str) -> Workstream:
        try:
            workstream = self.database.collection(self._collection_name).document(workstream_id).get()
            if workstream.exists == False:
                return {}
            return Workstream.from_dict(workstream.to_dict())
        except Exception as e:
            raise e
        
    def get_workstreams(self) -> list:
        try:
            workstreams = self.database.collection(self._collection_name).stream()
            return [Workstream.from_dict(workstream.to_dict()) for workstream in workstreams]
        except Exception as e:
            raise e

    def update_workstream(self, workstream_data: Workstream) -> None:
        try:
            print(workstream_data)
            self.database.collection(self._collection_name).document(workstream_data.id).update(workstream_data.to_dict())
        except Exception as e:
            raise e
    
    def get_workstreams_by_sub_goal_id(self, sub_goal_id: str) -> list:
        try:
            workstreams = self.database.collection(self._collection_name).where(
                filter=FieldFilter("sub_goal_id", "==", sub_goal_id)).stream()
            return [Workstream.from_dict(workstream.to_dict()) for workstream in workstreams]
        except Exception as e:
            raise e

      
    def add_performance_data(self, workstream_id: str, performance_data: dict) -> None:
        try:
            self.database.collection("workstream_performance").document(workstream_id).set(performance_data)
        except Exception as e:
            raise e
        
    def get_performance_data(self, workstream_id: str) -> list:
        try:
            performance_data = self.database.collection("workstream_performance").document(workstream_id).get()
            if performance_data.exists == False:
                return {}
            
            return performance_data.to_dict()
        except Exception as e:
            raise e
