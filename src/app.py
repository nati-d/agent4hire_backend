from infrastructure.repositories.alert_repository import AlertRepository
from infrastructure.llm.open_ai_llm import OpenAiLLMService
from infrastructure.repositories.chat_history_repository import ChatHistoryRepository
from controllers.chat_bot_controller import ChatbotController
from usecases.chat_bot_usecase import ChatbotUsecase
from flask import Flask, request, jsonify, session
from flask_session import Session
from flask_cors import CORS, cross_origin
from infrastructure.repositories.goal_repository import GoalRepository
from infrastructure.repositories.sub_goal_repository import SubGoalRepository
from infrastructure.repositories.workstream_repository import WorkstreamRepository
from infrastructure.repositories.self_reflection_repository import SelfReflectionRepository
from usecases.functionality_usecase import AgentFunctionalityUsecase
from controllers.agent_controller import AgentController
from infrastructure.llm.llm_service import LLMService
from infrastructure.repositories.agent_repository import AgentRepository
from infrastructure.repositories.api_repository import APIRepository
from infrastructure.scheduling_service import SchedulingService
from infrastructure.embedding_service import EmbeddingService
from infrastructure.api_descriptions import setup_embeddings
from infrastructure.performance_analyzer import PerformanceAnalyzer
from infrastructure.repositories.skill_repository import SkillRepository
from controllers.feedback_controller import FeedbackController
from usecases.agent_usecase import AgentUsecase
from usecases.feedback_usecase import UserFeedbackUseCase
from usecases.feedback_usecase import ImplicitFeedbackUsecase
from usecases.skill_usecase import SkillUsecase
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv() 

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

app = Flask(__name__)

# CORS Configuration
CORS(app, 
     origins=["*"],
     supports_credentials=True,
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     expose_headers=["Content-Type", "Authorization"],
     allow_headers=["Content-Type", "Authorization"])

app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

llm_service = LLMService(model_name="gemini-1.5-flash")
open_ai_service = OpenAiLLMService(model_name="gpt-4o-2024-08-06",
                                   api_key=os.getenv('OPENAI_API_KEY'))

# repositories
api_repo = APIRepository()
agent_repo = AgentRepository()
alert_repo = AlertRepository()
goal_repo = GoalRepository()
sub_goal_repo = SubGoalRepository()
workstream_repo = WorkstreamRepository()
chat_history_repo = ChatHistoryRepository()
self_reflection_repo = SelfReflectionRepository()
skill_repo = SkillRepository()

scheduling_service = SchedulingService('refined-analogy-435508-n3',
                                       'us-central1')
embedding_service = EmbeddingService()
agent_usecase = AgentUsecase(open_ai_service, api_repo, agent_repo, goal_repo,
                             sub_goal_repo, workstream_repo, scheduling_service,
                             embedding_service, self_reflection_repo, skill_repo)

performance_analyzer = PerformanceAnalyzer(LLMService("gemini-1.5-flash"))
functionality_usecase = AgentFunctionalityUsecase()
agent_controller = AgentController(agent_usecase,functionality_usecase, self_reflection_repo,)

user_feedback_usecase = UserFeedbackUseCase(agent_repo, goal_repo,
                                            sub_goal_repo, workstream_repo)
implicit_feedback_usecase = ImplicitFeedbackUsecase(agent_repo, goal_repo,
                                                    sub_goal_repo,
                                                    workstream_repo)

feedback_controller = FeedbackController(user_feedback_usecase,
                                         implicit_feedback_usecase)

# chatbot
chat_bot_usecase = ChatbotUsecase(agent_repo, chat_history_repo, alert_repo)
chat_bot_controller = ChatbotController(chat_bot_usecase)

step_limit = 5

# app.register_blueprint(skills_bp)

@app.route('/agents/create', methods=['POST'])
def create_agent_step1():
    try:
        # Only clear session if this is a new agent creation request
        if not request.json or 'answers' not in request.json:
            session.clear()
            session['step'] = 0
        
        step = session.get('step', 0)
        answers = request.json.get('answers', []) if request.json else []
        response = None
        print(f"Current step: {step}, Answers received: {len(answers)}")

        if step == 0:
            response = agent_controller.get_questions()
        elif step < step_limit:
            if not answers:
                return jsonify({"error": "No answers provided"}), 400
            # Store answers in session for final report
            session['answers'] = session.get('answers', []) + answers
            response = agent_controller.get_additional_questions()
        else:
            # Generate final report using all collected answers
            response = agent_controller.get_report()
            if isinstance(response, tuple):
                report = response[0].get_json()['report']
            else:
                report = response.get_json()['report']
                        
            return jsonify({
                "is_complete": True,
                "report": report
            }), 200

        if response and isinstance(response, tuple) and response[1] == 200:
            session['step'] = step + 1
            return response[0], 200
        
        return response

    except Exception as e:
        print(f"Error in create_agent_step1: {str(e)}")
        return jsonify({
            "error": "An error occurred while processing your request",
            "details": str(e)
        }), 500


@app.route('/agents/create/update-report', methods=['POST'])
@cross_origin()
def create_agent_step2():
    return agent_controller.update_report()


@app.route('/agents/create/goals', methods=['GET', 'POST'])
@cross_origin()
def create_agent_step3():
    if request.method == 'GET':
        return agent_controller.get_goals()

    response = agent_controller.create_agent()

    if response[1] == 202:
        session.clear()
        pass

    return response

@app.route('/agents/skills', methods=['POST', 'GET'])
@cross_origin()
def create_skill():
    if request.method == 'GET':
        return agent_controller.get_skills()
    
    response = agent_controller.create_skill()
    
    if response[1] == 202:
        session.clear()
        pass

    return response



@app.route('/agents/workstream/execute', methods=['POST'])
@cross_origin()
def process_duty():
    return agent_controller.process_workstream()


@app.route('/agents/feedbacks/submit', methods=['POST'])
@cross_origin()
def submit_feedback():
    return feedback_controller.submit_feedback()


@app.route("/agents/feedbacks/implicit", methods=["POST"])
@cross_origin()
def implicit_feedback():
    return feedback_controller.implicit_feedback()


@app.route('/agents/chat', methods=['POST'])
@cross_origin()
def chat_with_bot():
    return chat_bot_controller.chat_with_bot()

@app.route('/alert/chat', methods=['POST'])
@cross_origin()
def chat_with_alert():
    return chat_bot_controller.chat_with_alert()

#get all agents
@app.route('/agents', methods=['GET'])
@cross_origin()
def get_agents():
    return agent_controller.get_agents()
    

if __name__ == '__main__':
    app.run(debug=True)
