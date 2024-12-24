from infrastructure.llm.open_ai_llm import OpenAiLLMService
import json
from typing import Dict, Optional
from datetime import datetime, timedelta
import uuid
from domain.models.group_chat import GroupChat


class GroupChatUsecase:
    def __init__(self, llm_service: OpenAiLLMService, agent_repository, group_chat_repository):    
        self.agent_repository = agent_repository
        self.llm_service = llm_service
        self.group_chat_repository = group_chat_repository
        self._cached_descriptions = None
        self._cache_timestamp = None
        self._cache_duration = timedelta(minutes=5)  # Cache for 5 minutes

    def _generate_context(self, user_input: str) -> Dict:
        """
        Generate a structured context from user's input using LLM.
        """
        try:
            system_instruction = '''
            You are an AI assistant that helps create structured context from user input.
            Analyze the user's input and extract/infer key information to create a comprehensive context.
            
            The context should be in JSON format with the following structure:
            {
                "topic": "Main topic or subject of discussion",
                "objective": "Primary goal or purpose",
                "key_points": ["List of important points mentioned or implied"],
                "domain": "Technical domain or field",
                "requirements": ["List of requirements if any"],
                "constraints": ["List of constraints or limitations if any"],
                "background_info": "Any relevant background information",
                "preferences": ["User preferences or specific requests"],
                "priority_level": "high/medium/low based on urgency/importance",
                "additional_notes": "Any other relevant information"
            }
            
            Make reasonable inferences where information isn't explicitly stated, but mark inferred information with "(inferred)" prefix.
            '''

            messages = [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": f"Generate a structured context from this input: {user_input}"}
            ]

            response = self.llm_service.client.chat.completions.create(
                model=self.llm_service.model_name,
                messages=messages,
                response_format={ "type": "json_object" },
                max_tokens=1000,
                temperature=0.7
            )

            context = json.loads(response.choices[0].message.content)
            
            # Add metadata
            context["generated_at"] = datetime.now().isoformat()
            context["source_input"] = user_input
            
            return context
        except Exception as e:
            raise Exception(f"Error generating context: {str(e)}")

    def create_group_chat(self, name: str, user_input: str) -> GroupChat:
        """
        Create a new group chat with context generated from user input
        """
        try:
            # Generate structured context from user input
            context = self._generate_context(user_input)
            
            group_chat = GroupChat(
                id=str(uuid.uuid4()),
                name=name,
                context=context,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            self.group_chat_repository.create_group_chat(group_chat)
            return group_chat
        except Exception as e:
            raise Exception(f"Error creating group chat: {str(e)}")

    def _get_agent_descriptions(self) -> str:
        """
        Get agent descriptions from cache or refresh if needed.
        Returns a formatted string of agent descriptions.
        """
        current_time = datetime.now()
        
        # Check if cache is valid
        if (self._cached_descriptions is None or 
            self._cache_timestamp is None or 
            current_time - self._cache_timestamp > self._cache_duration):
            
            # Refresh cache
            agents = self.agent_repository.get_all_agents()
            self._cached_descriptions = "\n".join(
                [f"ID: {agent.id}, Role: {agent.role}, Description: {agent.description}" 
                 for agent in agents]
            )
            self._cache_timestamp = current_time
        
        return self._cached_descriptions

    def select_agent(self, group_chat_id: str, user_input: str):
        """
        Select the most relevant agent based on user input, group chat context, and agent descriptions.
        """
        try:
            # Get group chat context
            group_chat = self.group_chat_repository.get_by_id(group_chat_id)
            
            system_instruction = '''
            You are an AI assistant. Analyze the user input and context to match with the most suitable agent.
            Consider the following when making your selection:
            1. The immediate user query
            2. The broader conversation context and objectives
            3. Domain expertise required
            4. Previous interactions in the chat
            5. Specific requirements and constraints
            
            Return the id, role, and a match score (0-100) indicating how well the agent matches the user's needs.
            
            Response must be in JSON format with this structure:
            {
                "id": "agent_id",
                "role": "agent_role",
                "score": 85,  # A number between 0-100 indicating match confidence
                "reason": "Detailed explanation of why this agent was selected, referencing specific aspects of the context and query"
            }
            '''

            # Get agent descriptions from cache
            agent_descriptions = self._get_agent_descriptions()

            # Format context for better prompt
            context = group_chat.context
            context_str = json.dumps(context, indent=2)
            
            messages = [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": f"""
                Group Chat Context:
                {context_str}

                Current User Input: {user_input}

                Available Agents:
                {agent_descriptions}

                Select the most suitable agent considering both the immediate query and the broader context.
                """}
            ]

            response = self.llm_service.client.chat.completions.create(
                model=self.llm_service.model_name,
                messages=messages,
                response_format={ "type": "json_object" },
                max_tokens=500,
                temperature=0.7
            )

            selected_agent = json.loads(response.choices[0].message.content)
            
            # Add agent to group chat if not already present
            if selected_agent['id'] not in group_chat.agents:
                group_chat.agents.append(selected_agent['id'])
                self.group_chat_repository.update_agents(group_chat_id, group_chat.agents)

            return selected_agent
        except Exception as e:
            raise Exception(f"Error in selecting agent: {str(e)}")

    def process_user_input(self, group_chat_id: str, agent_id: str, user_input: str):
        """
        Generate a response from the selected agent using OpenAI, considering the group chat context.
        """
        try:
            # Get agent and group chat details
            agent = self.agent_repository.get_by_id(agent_id)
            group_chat = self.group_chat_repository.get_by_id(group_chat_id)
            
            if not agent:
                raise Exception(f"Agent with ID {agent_id} not found")

            # Store user message first
            user_message = {
                'sender': 'User',
                'content': user_input,
                'timestamp': datetime.now().isoformat(),
                'message_type': 'user_message'
            }
            self.group_chat_repository.add_message(group_chat_id, user_message)

            # Get recent messages for context
            recent_messages = self.group_chat_repository.get_messages(group_chat_id)
            
            # Format conversation history
            conversation_history = "\n".join([
                f"{msg['sender']}: {msg['content']}" 
                for msg in recent_messages[-5:]  # Include last 5 messages
            ])

            system_instruction = f'''
            You are an AI agent with the following role: "{agent.role}".
            Description: {agent.description}

            Group Chat Context:
            {json.dumps(group_chat.context, indent=2)}

            Recent Conversation:
            {conversation_history}

            Consider the following when responding:
            1. The specific context and objectives of the group chat
            2. Any requirements or constraints mentioned
            3. The conversation history and flow
            4. Your specific role and expertise
            5. The priority level of the query

            Provide a response that is:
            - Relevant to both the immediate question and broader context
            - Consistent with previous interactions
            - Within your role's expertise
            - Actionable and specific
            '''
            
            messages = [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_input}
            ]

            response = self.llm_service.client.chat.completions.create(
                model=self.llm_service.model_name,
                messages=messages,
                max_tokens=1000
            )

            response_content = response.choices[0].message.content

            # Store the agent's message
            agent_message = {
                'sender': f"Agent:{agent.role}",
                'content': response_content,
                'timestamp': datetime.now().isoformat(),
                'agent_id': agent_id,
                'message_type': 'agent_response'
            }
            self.group_chat_repository.add_message(group_chat_id, agent_message)

            return {
                'content': response_content,
                'timestamp': agent_message['timestamp'],
                'previous_messages': recent_messages[-5:]  # Include recent conversation context
            }
        except Exception as e:
            raise Exception(f"Error in processing user input: {str(e)}")

    def refresh_cache(self):
        """
        Force refresh the agent descriptions cache.
        Call this when agents are updated.
        """
        self._cached_descriptions = None
        self._cache_timestamp = None

    def get_all_group_chats(self, limit: int = 50) -> list:
        """
        Get all group chats, ordered by last update
        Returns a list of group chats with their basic info and latest message
        """
        try:
            group_chats = self.group_chat_repository.get_all_group_chats(limit=limit)
            
            # Format the response to include only necessary information
            formatted_chats = []
            for chat in group_chats:
                # Get the latest message
                messages = self.group_chat_repository.get_messages(chat.id, limit=1)
                latest_message = messages[0] if messages else None
                
                formatted_chat = {
                    'id': chat.id,
                    'name': chat.name,
                    'created_at': chat.created_at.isoformat(),
                    'updated_at': chat.updated_at.isoformat(),
                    'topic': chat.context.get('topic', ''),
                    'objective': chat.context.get('objective', ''),
                    'latest_message': latest_message,
                    'agent_count': len(chat.agents)
                }
                formatted_chats.append(formatted_chat)
            
            return formatted_chats
        except Exception as e:
            raise Exception(f"Error getting group chats: {str(e)}")
