from infrastructure.api_mapper import API_to_endpoint_mapper
from infrastructure.llm.llm_function_calling_service import LLM_function_calling_service
from infrastructure.llm.llm_service import LLMService


class Chatbot:
    def __init__(self, persona, agent_context=None, history=None, apis=None):

        self.persona = persona
        self.agent_context = agent_context
        self.apis = apis if apis is not None else []
        self.conversation_history = history if isinstance(history, list) else []
        self.chat = self.create_chatbot()
        
    
    def create_chatbot(self):
        """
      Creates a chatbot with the given persona and agent context.
    
      Returns:
          A Chat object representing the chatbot.
      """
        system_instruction = f"You are an AI chatbot with the following persona: {self.persona}. "
        
        if self.agent_context:
            system_instruction += "\n\nAgent Context:"
            if 'description' in self.agent_context:
                system_instruction += f"\nDescription: {self.agent_context['description']}"
            if 'kpis' in self.agent_context:
                system_instruction += "\nKPIs:"
                for kpi in self.agent_context['kpis']:
                    system_instruction += f"\n- {kpi['kpi']}: Expected Value = {kpi['expected_value']}"
            if 'additional_info' in self.agent_context:
                system_instruction += f"\nAdditional Information: {self.agent_context['additional_info']}"
        
        system_instruction += "\nBe respectful, helpful, and professional in your interactions."
        try:
            llm = LLMService(model_name="gemini-1.5-flash")
            function_calling = LLM_function_calling_service()
            mapper = API_to_endpoint_mapper()
            function_map = function_calling.get_function_map(mapper)
            api_map = function_calling.filter_function_map_by_apis(function_map, self.apis)
            chat = llm.chat_bot(system_instruction, list(api_map.values()),
                                self.conversation_history)
            print("chat bot generated with apis:" , api_map)
            return chat
        except Exception as e:
            print(f"Error creating chatbot: {e}")
            return None
    
    def chat_with_bot(self):
        if not self.chat:
            print(
                "Chatbot initialization failed. Please check the configuration."
            )
            return
    
        print("Chatbot is ready. Type 'exit' to end the conversation.")
        while True:
            message = input("You: ")
            if message.lower() == 'exit':
                print("Ending conversation.")
                break
            try:
                response = self.chat.send_message(message)
                print(f"Agent: {response.text}")
            except Exception as e:
                print(f"Error during conversation: {e}")