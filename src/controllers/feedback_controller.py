from usecases.feedback_usecase import UserFeedbackUseCase
from usecases.feedback_usecase import ImplicitFeedbackUsecase
from flask import  request, jsonify

class FeedbackController:
    def __init__(self, user_feedback_usecase: UserFeedbackUseCase, implicit_feedback_usecase: ImplicitFeedbackUsecase):
        self.user_feedback_usecase = user_feedback_usecase
        self.implicit_feedback_usecase = implicit_feedback_usecase
    
    def submit_feedback(self):
        feedback = request.json.get('feedback', None)
        agent_id = request.json.get('agent_id', None)
        
        if not feedback or not agent_id:
            return jsonify({
                'error': 'Feedback and agent_id are required.'
                }), 400
        
        try:
            self.user_feedback_usecase.add_feedback_to_agent(feedback=feedback, agent_id=agent_id)     
            self.user_feedback_usecase.update_nodes_based_on_feedback(feedback=feedback, agent_id=agent_id)
            return jsonify({
                'message': "agent nodes updated according to feedback"
                }), 200
        
        except Exception as e:
            return jsonify({
                'error': str(e)
                }), 500

    def implicit_feedback(self):
        agent_id = request.json.get('agent_id', None)
        if not agent_id:
            return jsonify({
                'error': 'agent_id is required.'
                }), 400
        
        try:
            print(agent_id + "recieved")
            self.implicit_feedback_usecase.implicitly_improve_agent(agent_id=agent_id)
            return jsonify({
                'message': "agent nodes updated according to feedback"
                }), 200
        
        except Exception as e:
            return jsonify({
                'error': str(e)
                }), 500
            
        
        
            