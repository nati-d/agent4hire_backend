from infrastructure.repositories.alert_repository import AlertRepository
from infrastructure.chat_bot import Chatbot
from infrastructure.repositories.agent_repository import AgentRepository
from infrastructure.repositories.chat_history_repository import ChatHistoryRepository


class ChatbotUsecase:

    def __init__(self, agent_repository: AgentRepository,
                 chat_history_repository: ChatHistoryRepository,
                 alert_repository: AlertRepository
                 ):
        self.chatbots = {}
        self.alert_chatbots = {}
        self.agent_repository = agent_repository
        self.chat_history_repository = chat_history_repository
        self.alert_repository = alert_repository

    def get_or_create_chatbot(self, agent_id):
        if agent_id not in self.chatbots:
            try:
                # Retrieve agent details
                agent = self.agent_repository.get_agent(agent_id)
                if agent:
                    # Create agent context dictionary
                    agent_context = {
                        'description': agent.description,
                        'kpis': [{'kpi': kpi.kpi, 'expected_value': kpi.expected_value} for kpi in agent.kpis],
                        'additional_info': {
                            'id': agent_id,
                            'created_at': str(agent.created_at) if hasattr(agent, 'created_at') else None,
                            'updated_at': str(agent.updated_at) if hasattr(agent, 'updated_at') else None
                        }
                    }

                    persona = agent.description.get("user_persona", "A helpful AI assistant")
                    print(f"Creating new chatbot for agent {agent_id} with persona: {persona}")

                    # Get chat history for the agent
                    chat_history = self.chat_history_repository.get_chat_history(
                        agent_id)

                    # Create new chatbot with full context
                    self.chatbots[agent_id] = Chatbot(
                        persona=persona,
                        agent_context=agent_context,
                        history=chat_history
                    )
            except Exception as e:
                raise e
        return self.chatbots[agent_id]

    def store_chat_history(self, agent_id):
        try:
            # Retrieve the chatbot's history
            chatbot = self.chatbots[
                agent_id] if agent_id in self.chatbots else None
            if chatbot:
                # Ensure each part in the chat history is properly formatted
                formatted_history = [{
                    "role": entry.role,
                    "message": entry.parts[0].text
                } for entry in chatbot.chat.history]

                # Create a data structure for the chat history with the expected structure
                chat_history_data = {
                    "agent_id": agent_id,
                    "history":
                    formatted_history  # List of dictionaries representing chat entries
                }
                print(chat_history_data)

                # Save the chat history to Firestore
                self.chat_history_repository.save_chat_history(
                    chat_history_data)
                print(f"Chat history for agent {agent_id} saved successfully.")
            else:
                print(
                    f"No chatbot found for agent {agent_id} to store history.")
        except Exception as e:
            raise e

    def get_or_create_alert_chatbot(self, alert_id):
        if alert_id not in self.chatbots:
            try:
                # Retrieve alert details
                alert = self.alert_repository.get_by_id(alert_id)
                if alert:
                    # Create alert context dictionary
                    alert_context = {
                        'description': alert.description,
                        'state': alert.state,
                        'suggested_actions': alert.suggested_actions,
                        'additional_info': {
                            'id': alert_id,
                            'created_at': str(alert.created_at) if hasattr(alert, 'created_at') else None,
                            'updated_at': str(alert.updated_at) if hasattr(alert, 'updated_at') else None
                        }
                    }

                    print(f"Creating new chatbot for alert {alert_id}")
                    chat_history = self.chat_history_repository.get_chat_history(alert_id)

                    # Create new chatbot with full context
                else:
                    print(f"No alert found for alert {alert_id}")

            except Exception as e:
                raise e
        return self.chatbots[alert_id]

    def store_alert_chat_history(self, alert_id):
        try:
            chatbot = self.alert_chatbots[alert_id] if alert_id in self.chatbots else None
            if chatbot:
                formatted_history = [{
                    "role": entry.role,
                    "message": entry.parts[0].text
                } for entry in chatbot.chat.history]

                chat_history_data = {"alert_id": alert_id, "history": formatted_history}

                self.chat_history_repository.save_chat_history(chat_history_data)
                print(f"Chat history for alert {alert_id} saved successfully.")
            else:
                print(
                    f"No chatbot found for alert {alert_id} to store history.")
        except Exception as e:
            raise e
