from typing import Any, Dict
import uuid
from datetime import datetime

class ModuleExecution:
    def __init__(
        self,
        execution_id: str,
        agent_id: str,  
        execution_time: datetime,
        result: str,
        summary: str = "",
    ) -> None:
        """
        Represents the execution of a module within a workstream, including agent information.

        :param execution_id: Unique ID for this execution.
        :param module_id: ID of the executed module.
        :param work_stream_id: ID of the workstream to which the module belongs.
        :param agent_id: ID of the agent associated with the execution.
        :param status: Status of the execution (e.g., "success", "failure").
        :param execution_time: Timestamp when the module was executed.
        :param result: Details or output of the execution result.
        :param summary: Summary of the execution.
        """
        self.agent_id = agent_id
        self.execution_time = execution_time
        self.result = result
        self.summary = summary

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the ModuleExecution object to a dictionary.
        """
        return {
            "agent_id": self.agent_id,  
            "execution_time": self.execution_time.isoformat(),
            "result": self.result,
            "summary": self.summary,
        }

    @staticmethod
    def from_dict(execution_data: Dict[str, Any]) -> "ModuleExecution":
        """
        Creates a ModuleExecution object from a dictionary.
        """
        return ModuleExecution(
            agent_id=execution_data["agent_id"],  
            execution_time=datetime.fromisoformat(execution_data["execution_time"]),
            result=execution_data["result"],
            summary=execution_data.get("summary", ""),
        )
