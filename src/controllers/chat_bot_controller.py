from infrastructure.repositories.agent_repository import AgentRepository
from usecases.chat_bot_usecase import ChatbotUsecase
from flask import Flask, request, jsonify


class ChatbotController:
  def __init__(self, chat_bot_usecase: ChatbotUsecase):
    self.chat_bot_usecase = chat_bot_usecase
    

  def chat_with_bot(self):
    data = request.json
    agent_id = data.get('agent_id')
    user_message = data.get('message')
    
    if not agent_id or not user_message:
      return jsonify({"error": "Agent ID and message are required"}), 400
    
    chatbot_instance = self.chat_bot_usecase.get_or_create_chatbot(agent_id=agent_id)
    
    if chatbot_instance:
      # Interact with the chatbot and get the response
        try:
            response = chatbot_instance.chat.send_message(user_message)
            self.chat_bot_usecase.store_chat_history(agent_id=agent_id)
            return jsonify({"response": response.text})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "chatbot not found"}), 404


  def chat_with_alert(self):
    data = request.json
    alert_id = data.get('agent_id')
    user_message = data.get('message')

    if not alert_id or not user_message:
      return jsonify({"error": "Alert ID and message are required"}), 400
    
    chatbot_instance = self.chat_bot_usecase.get_or_create_alert_chatbot(alert_id=alert_id)
    if chatbot_instance:
        try:
            response = chatbot_instance.chat.send_message(user_message)

            # Here we determine if the alert should start optimizing the agent

            self.chat_bot_usecase.store_alert_chat_history(alert_id=alert_id)
            return jsonify({"response": response.text})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "chatbot not found"}), 404
