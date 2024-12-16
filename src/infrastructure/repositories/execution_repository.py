from datetime import datetime
import json
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from domain.models.executions import ModuleExecution

from typing import Any, Dict
import uuid
from datetime import datetime

class ModuleExecutionRepository:
    def __init__(self):
        self.database = firestore.Client(database='agent-square')
        self._collection_name = "module_executions"

    def create_execution(self, execution_data: ModuleExecution) -> None:
        """
        Adds a new execution record to the module_executions collection.
        """
        try:
            self.database.collection(self._collection_name).document(execution_data.agent_id).set(execution_data.to_dict())
        except Exception as e:
            raise e

    def get_execution(self, agent_id: str) -> ModuleExecution:
        """
        Retrieves a single execution record by execution_id.
        """
        try:
            execution = self.database.collection(self._collection_name).document(agent_id).get()
            if not execution.exists:
                return None
            return ModuleExecution.from_dict(execution.to_dict())
        except Exception as e:
            raise e

    def get_executions(self) -> list:
        """
        Retrieves all execution records.
        """
        try:
            executions = self.database.collection(self._collection_name).stream()
            return [ModuleExecution.from_dict(execution.to_dict()) for execution in executions]
        except Exception as e:
            raise e

    def update_execution(self, execution_data: ModuleExecution) -> None:
        """
        Updates an existing execution record.
        """
        try:
            self.database.collection(self._collection_name).document(execution_data.agent_id).update(execution_data.to_dict())
        except Exception as e:
            raise e

    def add_execution_summary(self, agent_id: str, summary: str) -> None:
        """
        Adds or updates the summary for a specific execution record.
        """
        try:
            self.database.collection(self._collection_name).document(agent_id).update({"summary": summary})
        except Exception as e:
            raise e

    def get_execution_summary(self, agent_id: str) -> str:
        """
        Retrieves the summary for a specific execution record.
        """
        try:
            execution = self.database.collection(self._collection_name).document(agent_id).get()
            if not execution.exists:
                return None
            data = execution.to_dict()
            return data.get("summary", "")
        except Exception as e:
            raise e



