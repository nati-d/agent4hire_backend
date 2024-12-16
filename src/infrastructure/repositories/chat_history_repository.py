import json
from google.cloud import firestore

class ChatHistoryRepository:
  def __init__(self):
    self.database = firestore.Client(database='agent-square')
    self._collection_name = "chat_histories"
    
  def save_chat_history(self, chat_history_data):
    try:
      self.database.collection(self._collection_name).document(chat_history_data["agent_id"]).set({"history": chat_history_data})
    except Exception as e:
      raise e

  def get_chat_history(self, agent_id):
    try:
      chat_history = self.database.collection(self._collection_name).document(agent_id).get()
      if not chat_history.exists:
        return {}
      return chat_history.to_dict()
    except Exception as e:
      raise e
  
  def update_chat_history(self, chat_history_data):
    try:
      self.database.collection(self._collection_name).document(chat_history_data.id).update(chat_history_data.to_dict())
    except Exception as e:
      raise e