import uuid
from flask import Flask, request, jsonify, session
from domain.models.agent import Agent
from domain.models.goal import Goal
from domain.models.kpi import KPI
from domain.models.module import Module
from domain.models.workstream import Workstream
from infrastructure.llm.llm_service import LLMService
from infrastructure.performance_analyzer import PerformanceAnalyzer
from infrastructure.embedding_service import UserEmbeddingService
from infrastructure.repositories.agent_repository import AgentRepository
from infrastructure.repositories.goal_repository import GoalRepository
from infrastructure.repositories.sub_goal_repository import SubGoalRepository
from infrastructure.repositories.workstream_repository import WorkstreamRepository
from infrastructure.repositories.self_reflection_repository import SelfReflectionRepository
from domain.models.self_reflection import SelfReflection
from usecases.agent_usecase import AgentUsecase
from usecases.functionality_usecase import AgentFunctionalityUsecase
from usecases.performance_tracker import PerformanceTracker

user_embedding_service = UserEmbeddingService()

class AgentController:
    def __init__(self, agent_usecase: AgentUsecase,functionality_usecase: AgentFunctionalityUsecase, self_reflection_repository: SelfReflectionRepository = None):
        self.agent_usecase = agent_usecase
        self.functionality_usecase = functionality_usecase
        self.self_reflection_repository = self_reflection_repository

    def get_questions(self):
        data = request.json
        role = data.get('role', None)
        description = data.get('description', None)

        if role is None or description is None:
            return jsonify({
                'error': 'Role and description are required.'
                }), 400
        try:
            is_ethical, explanation = self.agent_usecase.validate_role_ethics(role, description)
            if not is_ethical:
                return jsonify({
                    'error': "Your input validates our standards: " f"{explanation}"
                }), 400

            
            is_api_mentioned = self.agent_usecase.check_api_availability_in_user_input(description)
            if is_api_mentioned:
                return jsonify({
                    'error': "To better assist you, could you kindly share a description without directly referencing any specific API? We'll handle the details from there."
                }), 400
        except Exception as e:
            return jsonify({
                'error': f"Error during role validation: {str(e)}"
            }), 500
        
        session['role'] = role
        session['description'] = description

        self_reflection_id = uuid.uuid4().hex
        user_id = uuid.uuid4().hex
        agent_id = uuid.uuid4().hex

        session['self_reflection_id'] = self_reflection_id
        session['user_id'] = user_id
        session['agent_id'] = agent_id

        self_reflection = SelfReflection(
            id=self_reflection_id,
            user_id=user_id,
            agent_id=agent_id,
            role=role,
            description=description,
            available_apis=[],
            interactions=[],
            workstreams=[],
            goals=[],
            subgoals=[]
        )

        self.self_reflection_repository.create_self_reflection(self_reflection)

        try:
            
            questions = self.agent_usecase.generate_questions(role, description)

            session['questions'] = questions
            session['answers'] = []

            return jsonify({
                'questions': questions
                }), 200
        except Exception as e:
            session.clear()
            return jsonify({
                'error': str(e)
                }), 500
        
    def get_additional_questions(self):
        data = request.json
        answers = data.get('answers', None)
        
        if answers is None:
            return jsonify({
                'error': 'Answers for previous questions are required.'
                }), 400
        

        try:
            role = session['role']
            is_ethical, description = self.agent_usecase.validate_user_input(role=role, input=answers)
            if not is_ethical:
                return jsonify({
                    'Your input validates the inital description: ': f"{description}"
                }), 400
        except Exception as e:
            return jsonify({
                'error': f"{str(e)}"
            }), 500
        
        try: 
            description = session['description']
            previous_questions_and_answers = list(zip(session['questions'], session['answers'] + answers))
            questions = self.agent_usecase.generate_additional_questions(role, description, previous_questions_and_answers)
            session['questions'].extend(questions)
            session['answers'].extend(answers)

            return jsonify({
                'questions': questions
                }), 200
        except Exception as e:
            return jsonify({
                'error': str(e)
                }), 500
        
    def get_report(self):
        data = request.json
        answers = data.get('answers', None)
        if answers is None:
            return jsonify({
                'error': 'Answers for previous questions are required.'
                }), 400

        session['answers'].extend(answers)
        
        try:
            role = session['role']
            is_ethical, description = self.agent_usecase.validate_user_input(role=role, input=answers)
            if not is_ethical:
                return jsonify({
                  'error':  f"Your input validates the inital role description: "f"{description}"
                }), 400
        except Exception as e:
            return jsonify({
                'error': f"{str(e)}"
            }), 500
        try:
            description = session['description']
            previous_questions_and_answers = list(zip(session['questions'], session['answers']))
            report = self.agent_usecase.generate_report(role, description, previous_questions_and_answers)
            session['report'] = report

            self_reflection_id = session.get('self_reflection_id')
            if self_reflection_id is None:
                return jsonify({'error': 'Session expired or invalid'}), 400
            self_reflection = self.self_reflection_repository.get_self_reflection(self_reflection_id)

            self_reflection.description = {
                'user_persona': report['user_persona'],
                'specific_needs': report['specific_needs']
            }

            self.self_reflection_repository.update_self_reflection(self_reflection)

            user_embedding_service.add_user_data(
                user_id=self_reflection.user_id,
                user_data=self_reflection.description
            )

            return jsonify({
                'report': report
                }), 200

        except Exception as e:
            return jsonify({
                'error': str(e)
                }), 500


    def update_report(self):
        data = request.json
        feedback = data.get('feedback', None)

        if feedback is None:
            return jsonify({
                'error': 'Feedback is required.'
                }), 400
        try:
            role = session['role']
            is_ethical, description = self.agent_usecase.validate_user_input(role=role, input=feedback)
            if not is_ethical:
                return jsonify({
                    'error':"Your input validates the inital role description: "f"{description}"
                }), 400
        except Exception as e:
            return jsonify({
                'error': "error" f"{str(e)}"
            }), 500
        try:
            description = session['description']
            previous_questions_and_answers = list(zip(session['questions'], session['answers']))
            report = session['report']
            updated_report = self.agent_usecase.update_report(role, description, previous_questions_and_answers, report, feedback)
            session['report'] = updated_report

            return jsonify({
                'report': updated_report
                }), 200
        except Exception as e:
            return jsonify({
                'error': str(e)
                }), 500
        
    def get_goals(self):
        try:
            role = session['role']
            report = session['report']
            self_reflection_id = session.get('self_reflection_id')
            if self_reflection_id is None:
                return jsonify({'error': 'Session expired or invalid'}), 400
            self_reflection = self.self_reflection_repository.get_self_reflection(self_reflection_id)
            goals = self.agent_usecase.generate_goals(role, report, self_reflection)

            return jsonify({
                'goals': goals
                }), 200
        except Exception as e:
            return jsonify({
                'error': str(e)
                }), 500
            
           
    def get_skills(self):
        try:
            #get skills from agent_usecase
            skills = self.agent_usecase.get_skills()
            return jsonify([skill.to_dict() for skill in skills]), 200

        except Exception as e:
            return jsonify({
                'error': str(e)
                }), 500
            
            

    def create_agent(self):
        data = request.json

        goals_dict = data.get('goals', None)
        if goals_dict is None:
            return jsonify({
                'error': 'Goals are required.'
                }), 400

        try:
            id = uuid.uuid4().hex
            user_id = uuid.uuid4().hex 
            role = session['role']
            report = session['report']
            description = {
                'user_persona': report['user_persona'],
                'specific_needs': report['specific_needs'],
            }
            agent_kpis = [KPI.from_dict(kpi_data) for kpi_data in report['kpis']]
            agent = Agent(id=id, user_id=user_id, role=role, description=description, kpis=agent_kpis)
            
            # # Generate skills

            goals = []
            for goal_dict in goals_dict:
                goal = Goal.from_dict(goal_dict)
                goal.id = uuid.uuid4().hex
                goal.agent_id = id
                goals.append(goal)

            # Get self_reflection from repository
            self_reflection_id = session.get('self_reflection_id')
            if self_reflection_id is None:
                return jsonify({'error': 'Session expired or invalid'}), 400
            self_reflection = self.self_reflection_repository.get_self_reflection(self_reflection_id)
            
            
            skills = self.agent_usecase.generate_skills(role, report['specific_needs'],self_reflection,id)
            print(len(skills), 'skills generated')
            
            # Generate relevant APIs
            relevant_apis = self.agent_usecase.generate_relevant_apis(role,description )
            agent.available_apis = relevant_apis

            # Update self_reflection.available_apis
            self_reflection.available_apis = relevant_apis
            self.self_reflection_repository.update_self_reflection(self_reflection)

            # Generate sub_goals and update SelfReflection
            sub_goals  = self.agent_usecase.generate_sub_goals(role, report, goals, self_reflection)
            print(len(sub_goals), 'sub goals generated')

            # Generate workstreams and update SelfReflection
            workstreams = self.agent_usecase.generate_workstreams(role, report, sub_goals,relevant_apis, self_reflection)
            print(len(workstreams), 'workstreams generated')

            

            # Create the agent with goals, sub_goals, workstreams, and skills
            self.agent_usecase.create_agent(agent, goals, sub_goals, workstreams, skills,id)

            # domain_name = 'https://' + request.host
            # print(domain_name)

            # self.agent_usecase.schedule_workstreams(workstreams, domain_name)
            print('workstreams scheduled')

            # self.agent_usecase.schedule_feedbacks(agent.id, domain_name, 'weekly')

            return jsonify({
                'message': 'Agent created successfully.',
                'workstreams': [workstream.to_dict() for workstream in workstreams]
                }), 202

        except Exception as e:
            print(e)
            return jsonify({
                'error': str(e)
                }), 500   
    
    def process_workstream(self):
        try:
            data = request.get_json()
            print("Got the data:", type(data))

            workstreams = data.get("workstreams")
            
            if not workstreams:
                return jsonify({"error": "workstream is required"}), 400

            print("Got the workstream:", type(workstreams))
            for workstream in workstreams:
                agent_id = workstream.get("agent_id")
                modules_data = workstream.get('modules')
            
                print("Got the modules:", type(modules_data))

                frequency = workstream.get('frequency')  
                if not modules_data:
                    return jsonify({"error": "No modules found in the workstream"}), 400

                modules = [] 

                for module_data in modules_data:
                    module_name = module_data.get('module')
                    kpis_data = module_data.get('kpis', [])
                    kpis = []

                    apis = module_data.get('apis', [])

                    for kpi_data in kpis_data:
                        kpi_instance = KPI(
                            kpi=kpi_data.get('kpi'),
                            expected_value=kpi_data.get('expected_value')
                        )
                        kpis.append(kpi_instance)

                    module_instance = Module(
                        module=module_name,
                        kpis=kpis,
                        frequency=frequency,  
                        apis= apis
                    )
                    modules.append(module_instance)

            modules_performance, error_occurred = self.functionality_usecase.Execute_modules(agent_id, modules)

            return (
                jsonify(
                    {
                        "message": (
                            "Something went wrong!"
                            if error_occurred
                            else "Steps processed successfully"
                        ),
                        "performance": modules_performance,
                    }
                ),
                500 if error_occurred else 200,
            )

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return jsonify({"error": "An error occurred while processing the workstream"}), 500

    def get_agents(self):
        try:
            agents = self.agent_usecase.get_agents()
            return jsonify([agent.to_dict() for agent in agents]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    
