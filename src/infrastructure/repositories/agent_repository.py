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
        
    def get_by_id(self, agent_id: str) -> Agent:
        """
        Retrieve an agent by its ID.
        
        Args:
            agent_id (str): The ID of the agent to retrieve
            
        Returns:
            Agent: The agent object if found
            
        Raises:
            Exception: If the agent is not found or if there's a database error
        """
        try:
            agent_doc = self.database.collection(self._collection_name).document(agent_id).get()
            if not agent_doc.exists:
                raise Exception(f"Agent with ID {agent_id} not found")
            return Agent.from_dict(agent_doc.to_dict())
        except Exception as e:
            raise Exception(f"Error retrieving agent: {str(e)}")
    
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
    
