import time
from typing import Any, Dict, List


# enum of alert states
class AlertState:
    DISMISSED = "dismissed" # dismissed by the user
    ACTIVE = "active"    # active alert
    RESOLVED = "resolved"  # resolved alert


class Alert:
    def __init__(
        self,
        id: str,
        user_id: str,
        agent_id: str,
        description: str,
        suggested_actions: List[str],
        state: AlertState,
    ) -> None:
        self.id = id
        self.user_id = user_id
        self.agent_id = agent_id
        self.description = description
        self.suggested_actions = suggested_actions
        self.state = state
        self.created_at = time.time()
        self.updated_at = time.time()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "agent_id": self.agent_id,
            "reason_for_alert": self.description,
            "suggested_actions": self.suggested_actions,
            "state": self.state.__str__(),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @staticmethod
    def from_dict(alert: Dict[str, Any]) -> "Alert":
        return Alert(
            id=alert["id"],
            user_id=alert["user_id"],
            agent_id=alert["agent_id"],
            description=alert["reason_for_alert"],
            suggested_actions=alert["suggested_actions"],
            state=alert["state"],
        )
