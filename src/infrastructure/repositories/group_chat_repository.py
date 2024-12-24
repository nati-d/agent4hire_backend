from google.cloud import firestore
from domain.models.group_chat import GroupChat
from datetime import datetime

class GroupChatRepository:
    def __init__(self):
        self.database = firestore.Client(database='agent-square')
        self._collection_name = "group_chats"

    def create_group_chat(self, group_chat: GroupChat) -> None:
        """Create a new group chat"""
        try:
            self.database.collection(self._collection_name).document(group_chat.id).set(group_chat.to_dict())
        except Exception as e:
            raise Exception(f"Error creating group chat: {str(e)}")

    def get_by_id(self, group_chat_id: str) -> GroupChat:
        """Get a group chat by ID"""
        try:
            doc = self.database.collection(self._collection_name).document(group_chat_id).get()
            if not doc.exists:
                raise Exception(f"Group chat with ID {group_chat_id} not found")
            return GroupChat.from_dict(doc.to_dict())
        except Exception as e:
            raise Exception(f"Error retrieving group chat: {str(e)}")

    def add_message(self, group_chat_id: str, message: dict) -> None:
        """Add a message to the group chat"""
        try:
            group_chat_ref = self.database.collection(self._collection_name).document(group_chat_id)
            group_chat_ref.update({
                'messages': firestore.ArrayUnion([message]),
                'updated_at': datetime.now()
            })
        except Exception as e:
            raise Exception(f"Error adding message: {str(e)}")

    def update_agents(self, group_chat_id: str, agent_ids: list) -> None:
        """Update the list of agents in the group chat"""
        try:
            self.database.collection(self._collection_name).document(group_chat_id).update({
                'agents': agent_ids,
                'updated_at': datetime.now()
            })
        except Exception as e:
            raise Exception(f"Error updating agents: {str(e)}")

    def get_messages(self, group_chat_id: str, limit: int = 50) -> list:
        """Get the most recent messages from a group chat"""
        try:
            doc = self.database.collection(self._collection_name).document(group_chat_id).get()
            if not doc.exists:
                raise Exception(f"Group chat with ID {group_chat_id} not found")
            
            chat_data = doc.to_dict()
            messages = chat_data.get('messages', [])
            return messages[-limit:] if messages else []
        except Exception as e:
            raise Exception(f"Error retrieving messages: {str(e)}")

    def get_all_group_chats(self, limit: int = 50, order_by: str = 'updated_at', descending: bool = True) -> list:
        """
        Get all group chats, ordered by specified field
        """
        try:
            query = self.database.collection(self._collection_name)
            
            # Add ordering
            direction = firestore.Query.DESCENDING if descending else firestore.Query.ASCENDING
            query = query.order_by(order_by, direction=direction).limit(limit)
            
            docs = query.stream()
            return [GroupChat.from_dict(doc.to_dict()) for doc in docs]
        except Exception as e:
            raise Exception(f"Error retrieving group chats: {str(e)}")
