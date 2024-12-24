from datetime import timedelta
from infrastructure.repositories.alert_repository import AlertRepository
from infrastructure.llm.open_ai_llm import OpenAiLLMService
from infrastructure.repositories.chat_history_repository import ChatHistoryRepository
from controllers.chat_bot_controller import ChatbotController
from infrastructure.repositories.tags_repository import TagsRepository
from infrastructure.repositories.trait_repository import TraitsRepository
from infrastructure.repositories.category_repository import CategoryRepository
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
from controllers.group_chat_controller import GroupChatController
from infrastructure.repositories.agent_repository import AgentRepository
from infrastructure.repositories.group_chat_repository import GroupChatRepository
from usecases.agent_usecase import AgentUsecase
from usecases.group_chat_usecase import GroupChatUsecase
from infrastructure.llm.llm_service import LLMService
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
from usecases.category_usecase import CategoryUsecase
from controllers.category_controller import CategoryController
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



llm_service = LLMService(model_name="gemini-1.5-flash")
open_ai_service = OpenAiLLMService(model_name="gpt-4o-2024-08-06",
                                   api_key=os.getenv('OPENAI_API_KEY'))

# Session Configuration
app.config['SESSION_PERMANENT'] = True  
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'  
app.config['SESSION_COOKIE_SECURE'] = False  
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# CSRF Protection
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_TIME_LIMIT'] = 300  # 5 minutes (300 seconds)
app.config['WTF_CSRF_SSL_STRICT'] = False  # Set to True in production
app.config['WTF_CSRF_CHECK_DEFAULT'] = True

Session(app)

# repositories
api_repo = APIRepository()
agent_repo = AgentRepository()
group_chat_repo = GroupChatRepository()
alert_repo = AlertRepository()
goal_repo = GoalRepository()
sub_goal_repo = SubGoalRepository()
workstream_repo = WorkstreamRepository()
chat_history_repo = ChatHistoryRepository()
self_reflection_repo = SelfReflectionRepository()
skill_repo = SkillRepository()
tag_repo = TagsRepository()
trait_repo = TraitsRepository()
category_repo = CategoryRepository()

scheduling_service = SchedulingService('refined-analogy-435508-n3',
                                       'us-central1')
embedding_service = EmbeddingService()
agent_usecase = AgentUsecase(open_ai_service, api_repo, agent_repo, goal_repo,
                             sub_goal_repo, workstream_repo, scheduling_service,
                             embedding_service, self_reflection_repo, skill_repo,
                             tag_repo, trait_repo, category_repo)

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

category_usecase = CategoryUsecase(category_repo, open_ai_service)
category_controller = CategoryController(category_usecase)

group_chat_usecase = GroupChatUsecase(open_ai_service, agent_repo, group_chat_repo)
group_chat_controller = GroupChatController(group_chat_usecase)

step_limit = 2

# app.register_blueprint(skills_bp)

@app.route('/agents/create', methods=['POST'])
@cross_origin(supports_credentials=True)
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
@cross_origin(supports_credentials=True)
# @cross_origin()
def create_agent_step3():
    
    print('yyyyyyyyyyyyyyyyyyyy')
    if request.method == 'GET':
        return agent_controller.get_goals()

    response = agent_controller.create_agent()

    if response[1] == 202:
        # session.clear()
        pass

    return response



# @app.route('/agents/skills', methods=['POST', 'GET'])
# @cross_origin(supports_credentials=True)
# # @cross_origin()
# def create_skill():
#     if request.method == 'GET':
#         return agent_controller.get_skills()
    
#     response = agent_controller.create_skill()
    
#     if response[1] == 202:
#         session.clear()
#         pass

#     return response

@app.route('/agents/tags', methods=['GET'])
@cross_origin(supports_credentials=True)
# @cross_origin()
def get_tags():
    return agent_controller.get_tags()


@app.route('/agents/skills', methods=['GET'])
@cross_origin(supports_credentials=True)
# @cross_origin()
def get_skills():
    return agent_controller.get_skills()

@app.route('/agents/traits/<agent_id>', methods=['GET'])
@cross_origin(supports_credentials=True)
# @cross_origin()
def get_traits_by_agent_id(agent_id):
    return agent_controller.get_traits_by_agent_id(agent_id)

@app.route('/agents/tags/<agent_id>', methods=['GET'])
@cross_origin(supports_credentials=True)
# @cross_origin()
def get_tags_by_agent_id(agent_id):
    return agent_controller.get_tags_by_agent_id(agent_id)

@app.route('/agents/skills/<agent_id>', methods=['GET'])
@cross_origin(supports_credentials=True)
# @cross_origin()
def get_skills_by_agent_id(agent_id):
    return agent_controller.get_skills_by_agent_id(agent_id)

@app.route('/categories', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def handle_categories():
    if request.method == 'POST':
        return category_controller.create_category()
    return category_controller.get_categories()

@app.route('/categories/<category_id>', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_category(category_id):
    return category_controller.get_category(category_id)

@app.route('/categories/suggest-description', methods=['POST'])
@cross_origin(supports_credentials=True)
def suggest_category_description():
    return category_controller.suggest_description()

@app.route('/agents/workstream/execute', methods=['POST'])
@cross_origin(supports_credentials=True)
def process_duty():
    return agent_controller.process_workstream()


@app.route('/agents/feedbacks/submit', methods=['POST'])
@cross_origin(supports_credentials=True)
def submit_feedback():
    return feedback_controller.submit_feedback()


@app.route("/agents/feedbacks/implicit", methods=["POST"])
@cross_origin(supports_credentials=True)
def implicit_feedback():
    return feedback_controller.implicit_feedback()


@app.route('/agents/chat', methods=['POST'])
@cross_origin(supports_credentials=True)
def chat_with_bot():
    return chat_bot_controller.chat_with_bot()

@app.route('/alert/chat', methods=['POST'])
@cross_origin(supports_credentials=True)
def chat_with_alert():
    return chat_bot_controller.chat_with_alert()

#get all agents
@app.route('/agents', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_agents():
    return agent_controller.get_agents()

# Group Chat Endpoints
@app.route('/group-chats/', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def group_chats():
    """
    GET: List all group chats
    POST: Create a new group chat
    """
    if request.method == 'GET':
        return group_chat_controller.get_all_group_chats()
    else:  # POST
        return group_chat_controller.create_group_chat()

@app.route('/group-chats/chat', methods=['POST'])
@cross_origin(supports_credentials=True)
def handle_chat():
    """
    Send a message in a group chat
    """
    return group_chat_controller.handle_group_chat()

@app.route('/group-chats/<chat_id>/messages', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_chat_history(chat_id):
    """
    Get message history for a specific chat
    """
    return group_chat_controller.get_chat_history(chat_id)

@app.route('/group-chats/refresh-cache', methods=['POST'])
@cross_origin(supports_credentials=True)
def refresh_agent_cache():
    """
    Force refresh the agent descriptions cache
    """
    return group_chat_controller.refresh_agent_cache()

if __name__ == '__main__':
    app.run(debug=True)
