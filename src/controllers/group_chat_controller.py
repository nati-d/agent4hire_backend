from flask import request, jsonify
import json

class GroupChatController:
    def __init__(self, group_chat_usecase):
        self.group_chat_usecase = group_chat_usecase

    def _validate_json_request(self):
        """Helper method to validate JSON request"""
        if not request.is_json:
            raise ValueError("Request must be JSON")
        try:
            return request.get_json()
        except Exception as e:
            raise ValueError(f"Invalid JSON format: {str(e)}")

    def create_group_chat(self):
        """
        Create a new group chat with context generated from user input
        """
        try:
            data = self._validate_json_request()
            name = data.get('name')
            user_input = data.get('user_input')

            if not name:
                return jsonify({'error': 'Group chat name is required'}), 400
            if not user_input:
                return jsonify({'error': 'Initial context input is required'}), 400

            group_chat = self.group_chat_usecase.create_group_chat(name, user_input)
            
            return jsonify({
                'status': 'success',
                'data': {
                    'group_chat_id': group_chat.id,
                    'name': group_chat.name,
                    'context': group_chat.context,
                    'created_at': group_chat.created_at.isoformat()
                }
            })
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def handle_group_chat(self):
        """
        Handle messages in a group chat
        """
        try:
            data = self._validate_json_request()
            group_chat_id = data.get('group_chat_id')
            user_input = data.get('user_input')
            
            if not group_chat_id:
                return jsonify({'error': 'Group chat ID is required'}), 400
            if not user_input:
                return jsonify({'error': 'User input is required'}), 400

            # First select the appropriate agent
            selected_agent = self.group_chat_usecase.select_agent(group_chat_id, user_input)
            
            if not selected_agent or 'id' not in selected_agent:
                return jsonify({'error': 'No suitable agent found'}), 404

            # Process the user input with the selected agent
            response = self.group_chat_usecase.process_user_input(
                group_chat_id,
                selected_agent['id'], 
                user_input
            )

            return jsonify({
                'status': 'success',
                'data': {
                    'selected_agent': {
                        'id': selected_agent['id'],
                        'role': selected_agent['role'],
                        'match_score': selected_agent.get('score', 0),
                        'selection_reason': selected_agent.get('reason', '')
                    },
                    'response': response['content'],
                    'timestamp': response['timestamp'],
                    'conversation_context': response['previous_messages']
                }
            })

        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def get_all_group_chats(self):
        """
        Get all group chats with their basic information
        """
        try:
            # Get limit from query parameters, default to 50
            limit = request.args.get('limit', default=50, type=int)
            
            group_chats = self.group_chat_usecase.get_all_group_chats(limit=limit)
            
            return jsonify({
                'status': 'success',
                'data': {
                    'group_chats': group_chats,
                    'count': len(group_chats)
                }
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def refresh_agent_cache(self):
        """
        Force refresh the agent descriptions cache
        """
        try:
            self.group_chat_usecase.refresh_cache()
            return jsonify({
                'status': 'success',
                'message': 'Agent cache refreshed successfully'
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500

    def get_chat_history(self, chat_id):
        """
        Get the message history for a specific chat
        """
        try:
            # Get limit from query parameters, default to 50
            limit = request.args.get('limit', default=50, type=int)
            
            messages = self.group_chat_usecase.group_chat_repository.get_messages(chat_id, limit)
            
            if not messages:
                return jsonify({
                    'status': 'success',
                    'data': {
                        'messages': [],
                        'count': 0
                    }
                })

            return jsonify({
                'status': 'success',
                'data': {
                    'messages': messages,
                    'count': len(messages)
                }
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
