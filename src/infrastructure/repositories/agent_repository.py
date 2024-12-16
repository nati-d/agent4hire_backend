import json
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

from domain.models.agent import Agent

class AgentRepository:
    def __init__(self):
        self.database = firestore.Client(database='agent-square')
        self._collection_name = "agents"

    def create_agent(self, agent_data: Agent) -> None:
        try:
            self.database.collection(self._collection_name).document(agent_data.id).set(agent_data.to_dict())
        except Exception as e:
            raise e
        
    def get_agent(self, agent_id: str) -> Agent:
        try:
            print("databaseeeeee")
            agent = self.database.collection(self._collection_name).document(agent_id).get()
            return Agent.from_dict(agent.to_dict())
        except Exception as e:
            raise e
    
    def get_all_agents(self) -> list:
        try:
            agents = self.database.collection(self._collection_name).stream()
            return [Agent.from_dict(agent.to_dict()) for agent in agents]
        except Exception as e:
            raise e
        
    
    def update_agent(self, agent_data: Agent) -> None:
        try:
            self.database.collection(self._collection_name).document(agent_data.id).update(agent_data.to_dict())
        except Exception as e:
            raise e
    
    def add_performance_data(self, agent_id: str, performance_data: dict) -> None:
        try:
            self.database.collection('agent_performance').document(agent_id).set(performance_data)
        except Exception as e:
            raise e
        
    def get_performance_data(self, agent_id: str) -> list:
        try:
            agent_performance = self.database.collection('agent_performance').document(agent_id).get()
            if agent_performance.exists == False:
                return {}
            return agent_performance.to_dict()
        except Exception as e:
            raise e