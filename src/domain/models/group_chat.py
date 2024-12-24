from datetime import datetime
from typing import Dict, Any, List, Optional

class GroupChat:
    def __init__(self, 
                 id: str,
                 name: str,
                 context: Dict[str, Any],
                 created_at: datetime,
                 updated_at: datetime,
                 agents: List[str] = None,  # List of agent IDs
                 messages: List[Dict] = None):
        self.id = id
        self.name = name
        self.context = context
        self.created_at = created_at
        self.updated_at = updated_at
        self.agents = agents or []
        self.messages = messages or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "context": self.context,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "agents": self.agents,
            "messages": self.messages
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'GroupChat':
        return GroupChat(
            id=data.get('id'),
            name=data.get('name'),
            context=data.get('context', {}),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
            agents=data.get('agents', []),
            messages=data.get('messages', [])
        )
