import json
import os
import uuid

from proto.message import re
from infrastructure.llm.open_ai_llm import OpenAiLLMService
from infrastructure.llm.open_ai_schemas import BooleanSchema, StringSchema, ArraySchema, AnswersScehma, KpiSchema, ReportSchema, ModuleSchema, GoalSchema, SubGoalSchema, WorkstreamSchema, subgoals_schema, workstreams_schema, goals_schema, report_schema, modules_schema
from domain.models.agent import Agent
from domain.models.goal import Goal
from domain.models.kpi import KPI
from domain.models.module import Frequency, Module
from domain.models.sub_goal import SubGoal
from domain.models.workstream import Workstream
from domain.models.self_reflection import SelfReflection
from domain.models.skill import Skill
from domain.models.tag import Tags
from domain.models.trait import Traits
from domain.models.category import Category, AGENT_CATEGORIES
from infrastructure.llm.llm_service import LLMService
from infrastructure.repositories.agent_repository import AgentRepository
from infrastructure.repositories.api_repository import APIRepository
from infrastructure.repositories.goal_repository import GoalRepository
from infrastructure.repositories.sub_goal_repository import SubGoalRepository
from infrastructure.repositories.workstream_repository import WorkstreamRepository
from infrastructure.repositories.self_reflection_repository import SelfReflectionRepository
from infrastructure.repositories.tags_repository import TagsRepository
from infrastructure.repositories.trait_repository import TraitsRepository
from infrastructure.repositories.skill_repository import SkillRepository
from infrastructure.repositories.category_repository import CategoryRepository
from infrastructure.scheduling_service import SchedulingService
from infrastructure.embedding_service import EmbeddingService
from google.cloud import run_v2
import google.generativeai as genai
from infrastructure.api_trees import API_Utils

import typing_extensions as typing
import time
from typing import List, Dict, Tuple


def retry(max_retries: int, delay: int):

    def decorator(func):

        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < max_retries - 1:
                        time.sleep(delay)
                    else:
                        raise e

        return wrapper

    return decorator


# kpi_schema = genai.protos.Schema(
#     type=genai.protos.Type.OBJECT,
#     properties={
#         'kpi': genai.protos.Schema(type=genai.protos.Type.STRING),
#         'expected_value': genai.protos.Schema(type=genai.protos.Type.STRING),
#     })

# kpis_schema = genai.protos.Schema(type=genai.protos.Type.ARRAY,
#                                   items=kpi_schema)

# report_schema = genai.protos.Schema(
#     type=genai.protos.Type.OBJECT,
#     properties={
#         'user_persona':
#         genai.protos.Schema(type=genai.protos.Type.STRING),
#         'specific_needs':
#         genai.protos.Schema(
#             type=genai.protos.Type.ARRAY,
#             items=genai.protos.Schema(type=genai.protos.Type.STRING)),
#         'kpis':
#         kpis_schema
#     })

# module_schema = genai.protos.Schema(
#     type=genai.protos.Type.OBJECT,
#     properties={
#         'module': genai.protos.Schema(type=genai.protos.Type.STRING),
#         # 'kpis': genai.protos.Schema(type=genai.protos.Type.ARRAY, items=kpi_schema),
#         'frequency': genai.protos.Schema(type=genai.protos.Type.STRING, enum=[freq.value for freq in Frequency]),
#     }
# )

# # modules_schema = genai.protos.Schema(
# #     type=genai.protos.Type.ARRAY,
# #     items=module_schema
# # )

# goal_schema = genai.protos.Schema(
#     type=genai.protos.Type.STRING,
#     properties={
#         'goal':
#         genai.protos.Schema(type=genai.protos.Type.STRING),
#         'kpis':
#         genai.protos.Schema(type=genai.protos.Type.ARRAY, items=kpi_schema),
#     })

# sub_goal_schema = genai.protos.Schema(
#     type=genai.protos.Type.OBJECT,
#     properties={
#         'sub_goal':
#         genai.protos.Schema(type=genai.protos.Type.STRING),
#         'kpis':
#         genai.protos.Schema(type=genai.protos.Type.ARRAY, items=kpi_schema),
#     })

# workstream_schema = genai.protos.Schema(
#     type=genai.protos.Type.OBJECT,
#     properties={
#         'workstream':
#         genai.protos.Schema(type=genai.protos.Type.STRING),
#         'frequency':
#         genai.protos.Schema(type=genai.protos.Type.STRING),
#         'kpis':
#         genai.protos.Schema(type=genai.protos.Type.ARRAY, items=kpi_schema),
#     })

# apis = [
#     "Zoominfo ", "Slack", "News API", "ECB API", "Guardian News API",
#     "Hunter.io", "Github", "Free Forex API", "Open FDA", "Here API",
#     "CoinLore", "CDCAPI", "BinanceAPI", "HealthCareAPI", "HubSpotAPI",
#     "Alpha Vantage", "GNews API", "Quickbooks", "Confluence"
# ]


class AgentUsecase:

    def __init__(self, llm_service: OpenAiLLMService,
                 api_repository: APIRepository,
                 agent_repository: AgentRepository,
                 goal_repository: GoalRepository,
                 sub_goal_repository: SubGoalRepository,
                 workstream_repository: WorkstreamRepository,
                 scheduling_service: SchedulingService,
                 embedding_service: EmbeddingService,
                 self_reflection_repository: SelfReflectionRepository,
                 skill_repository: SkillRepository,
                 tags_repository: TagsRepository,
                 traits_repository: TraitsRepository,
                 category_repository: CategoryRepository):

        self.llm_service = llm_service
        self.api_repository = api_repository
        self.agent_repository = agent_repository
        self.goal_repository = goal_repository
        self.sub_goal_repository = sub_goal_repository
        self.workstream_repository = workstream_repository
        self.scheduling_service = scheduling_service
        self.embedding_service = embedding_service
        self.self_reflection_repository = self_reflection_repository
        self.skill_repository = skill_repository
        self.tags_repository = tags_repository
        self.traits_repository = traits_repository
        self.category_repository = category_repository  

    def _get_relevant_entities(self, query: str, entity_type: str) -> List[Dict]:
        """Retrieve relevant entities from the vector database based on a query and entity type."""
        return self.embedding_service.search_relevant_entities(query, entity_type)

    def generate_questions(self, role: str, description: str) -> List[str]:
        system_instruction = """You are an AI assistant designed to help users create personalized agents. Your task is to ask thoughtful, insightful questions that will gather all the necessary details about the type of agent the user wants to create. Focus on understanding the agent’s purpose, functionalities, target audience, role, and specific tasks it needs to perform. Make sure the questions are clear, concise, and cover all aspects required to define the agent effectively."""
        query = f"""
        Return all of the APIs we have available.
        """
        relevant_apis = self._get_relevant_entities(query=query, entity_type="api")
        
        apis_context = "\n".join([f"{api['name']}: {api['description']}" for api in relevant_apis])
        
        query = f"""
        Generate 5 specific and relevant questions to ask the user based on the role and the description provided about the agent that is going to be created.
        Given the role: {role}
        And description: {description}
        
        Considering these available APIs:
        {apis_context}
        """
        
        response_schema = ArraySchema
        response = self.llm_service.generate_content_with_Structured_schema(
            system_instruction=system_instruction,
            query=query,
            response_schema=response_schema)
        return response.array

    def generate_additional_questions(
            self, role: str, description: str,
            previous_questions_and_answers: zip) -> list[str]:
        user_preference = ""
        all_answers = ""
        for question, answer in previous_questions_and_answers:
            user_preference += f"{question}: {answer}\n"
            all_answers += f"{answer}\n"

        system_instruction = """You are an AI assistant designed to help users create personalized agents. Your task is to ask thoughtful, insightful questions that will gather all the necessary details about the type of agent the user wants to create. Focus on understanding the agent’s purpose, functionalities, target audience, role, and specific tasks it needs to perform. Make sure the questions are clear, concise, and cover all aspects required to define the agent effectively."""

        query = f"""
        Return all of the APIs we have available.
        """
        
        combined_context = f"{query} {all_answers}"
        
        if len(previous_questions_and_answers) % 5 == 0:
            relevant_apis = self._get_relevant_entities(query=combined_context, entity_type="api")
            apis_context = "\n".join([f"{api['name']}: {api['description']}" for api in relevant_apis])
        
            query = f"""
            Generate 5 additional specific and relevant questions to ask the user based on the role and description of the agent, and the answers to the previous questions about the agent that is going to be created.
            Given the role: {role}
            And description: {description}
            
            Previous Q&A:
            {user_preference}
            
            Considering these available APIs:
            {apis_context}
            """

        response_schema = ArraySchema

        response = self.llm_service.generate_content_with_Structured_schema(
            system_instruction=system_instruction,
            query=query,
            response_schema=response_schema)

        return response.array

    def generate_report(self, role: str, description: str,
                        previous_questions_and_answers: zip) -> str:
        # Generate a detailed report based on the user's answers to the questions and the agent's role and description
        user_preference = ""
        for question, answer in previous_questions_and_answers:
            user_preference += f"{question}: {answer}\n"

        system_instruction = """You are an AI assistant designed to help users create personalized agents. """
        query = f"""Generate an agent persona for this AI {role} based on the description and previous questions and answers given below. Make it extensive. Also generate the specific needs of the user for this AI. Additionally generate the KPIs and their expected value for the agent based on the user persona and specific needs.
                    description : {description}
                    previous questions and answers : \n{user_preference}
                    """

        response_schema = report_schema

        response = self.llm_service.generate_content_with_json_format(
            system_instruction=system_instruction,
            query=query,
            response_schema=response_schema)
        report = json.loads(response)

        return report

    def update_report(self, role: str, description: str,
                      previous_questions_and_answers: zip, report: dict,
                      feedback: str) -> str:
        user_preference = ""
        for question, answer in previous_questions_and_answers:
            user_preference += f"{question}: {answer}\n"

        system_instruction = """You are an AI assistant designed to help users create personalized agents."""
        query = f"""Update the user persona and specific needs based on the user's feedback. Incorporate the feedback provided by the user to make it align to the user needs. Also update the KPIs and their expected value based on the feedback provided by the user.
                    role : {role}
                    description : {description}
                    previous questions and answers : \n{user_preference}
                    user persona : {report['user_persona']}
                    specific needs : {report['specific_needs']}
                    kpis : {','.join([f"{kpi['kpi']} with expected value {kpi['expected_value']}" for kpi in report['kpis']])}
                    feedback : {feedback}
                    """

        response_schema = report_schema

        response = self.llm_service.generate_content_with_json_format(
            system_instruction=system_instruction,
            query=query,
            response_schema=response_schema)

        return json.loads(response)

    def generate_goals(self, role: str, report: dict, self_reflection: SelfReflection) -> list:
        specific_needs = ','.join(report['specific_needs'])
        kpis = ','.join([
            f"{kpi['kpi']} with expected value {kpi['expected_value']}"
            for kpi in report['kpis']
        ])
        system_instruction = """You are an AI assistant designed to help users generate goals for an AI agent."""

        query = f"""
        Return all of the APIs we have available.
        """
        
        relevant_apis = self._get_relevant_entities(query=query, entity_type="api")
        apis_context = "\n".join([f"{api['name']}: {api['description']}" for api in relevant_apis])

        query = f"""
        Generate two goals for the AI {role} agent based on the description and user-provided answers to previous questions. Ensure the goals are broad, measurable, and achievable, aligning with the available API functionalities.
        
        user persona : {report['user_persona']}
        specific needs : {specific_needs}
        agent kpis: {kpis}
        Given role: {role}

        Available APIs:
        {apis_context}

        Return your response as a JSON list of goal strings according to the response schema provided.
        """

        response_schema = ArraySchema
        goals_string = ""
        max_retries = 5
        for attempt in range(max_retries):
            response = self.llm_service.generate_content_with_Structured_schema(
                system_instruction=system_instruction,
                query=query,
                response_schema=response_schema)
            print(response.array)
            try:
                goals_string = response.array
                if isinstance(goals_string, list) and all(
                        isinstance(goal, str) for goal in goals_string):
                    break
            except json.JSONDecodeError:
                pass

            if attempt < max_retries - 1:
                time.sleep(2**attempt)  # Exponential backoff
        else:
            raise RuntimeError(
                "Failed to generate goals after multiple attempts")

        goals = []
        for goal in goals_string:
            print(goal)
            system_instruction = """You are an AI assistant designed to generate kpis for goals of an AI agent."""
            query = f"""generate a list of at least 2 kpis that you think this goal should be measured against. These KPIs need to be measurable.  make sure to make it short and one sentence
                user persona : {report['user_persona']} 
                specific needs : {specific_needs}
                agent kpis: {kpis}
                goal : {goal}

                Return your response as a JSON list of strings according to the response schema provided.
                """
            response_schema = ArraySchema

            for attempt in range(max_retries):
                response = self.llm_service.generate_content_with_Structured_schema(
                    system_instruction=system_instruction,
                    query=query,
                    response_schema=response_schema)
                print(response)
                try:
                    kpis_list = response.array
                    if isinstance(kpis_list, list) and all(
                            isinstance(kpi, str) for kpi in kpis_list):
                        break
                except json.JSONDecodeError:
                    pass

            if attempt < max_retries - 1:
                time.sleep(2**attempt)  # Exponential backoff
            else:
                raise RuntimeError(
                    f"Failed to generate KPIs for goal '{goal}' after multiple attempts"
                )

            print(kpis_list)

            kpis = []
            for kpi in kpis_list:
                system_instruction = """You are an AI assistant designed to help users create personalized agents."""
                query = f"""Generate an expected value for the KPI provided below according to the user persona, specific needs, agent KPIs, and goal. make sure to make it short and one sentence
                    user persona: {report['user_persona']}
                    specific needs: {specific_needs}
                    agent KPIs: {kpis}
                    goal: {goal}
                    KPI: {kpi}
                    """

                response_schema = StringSchema

                for attempt in range(max_retries):
                    response = self.llm_service.generate_content_with_Structured_schema(
                        system_instruction=system_instruction,
                        query=query,
                        response_schema=response_schema)
                    try:
                        expected_value = response.string
                        if isinstance(expected_value, str):
                            break
                    except json.JSONDecodeError:
                        pass

                    if attempt < max_retries - 1:
                        time.sleep(2**attempt)  # Exponential backoff
                else:
                    raise RuntimeError(
                        f"Failed to generate expected value for KPI '{kpi}' after multiple attempts"
                    )

                kpi_obj = {'kpi': kpi, 'expected_value': expected_value}
                kpis.append(kpi_obj)

            goal_data = [{
                "name": goal,
                "description": f"Goal for role {role}: {goal}",
                "type": "goal"
            }]
            self.embedding_service.add_entities(goal_data, "goal")


            goal_obj = {'goal': goal, 'kpis': kpis}
            goals.append(goal_obj)
        
        self_reflection.goals = goals
        self.self_reflection_repository.update_self_reflection(self_reflection)

        return goals

    @retry(max_retries=5, delay=2)
    def generate_sub_goals(self, role: str, report: dict,
                           goals: list[Goal], self_reflection: SelfReflection) -> list[SubGoal]:
        try:
            specific_needs = ','.join(report['specific_needs'])
            agent_kpis = ','.join([
                f"{kpi['kpi']} with expected value {kpi['expected_value']}"
                for kpi in report['kpis']
            ])
            sub_goals = []
            for goal in goals:
                goal_kpis = ','.join([
                    f"{kpi.kpi} with expected value {kpi.expected_value}"
                    for kpi in goal.kpis
                ])

                query = f"""
                Return all of the APIs we have available.
                """                

                relevant_apis = self._get_relevant_entities(query=query, entity_type="api")
                apis_context = "\n".join([f"{api['name']}: {api['description']}" for api in relevant_apis])

                goal_descriptions = self._get_relevant_entities(query=query, entity_type="goal")

                system_instruction = """You are an AI assistant designed to help users create personalized agents."""
                query = f"""Generate 2 sub goals to break down the goal provided below that you think this AI {role} with the specified user persona and specific needs should have. These sub goals should be a way to divide and conquer the problem of the major goal. Make sure to write the API's you are considering to use don't mention the reason though.
                            user persona : {report['user_persona']}
                            specific needs : {specific_needs}
                            agent kpis: {agent_kpis}
                            goal : {goal.goal}
                            goal kpis : {goal_kpis}
                            User-provided goals:
                            {goal_descriptions}

                            Available APIs:
                            {apis_context}
                            """

                response_schema = ArraySchema

                response = self.llm_service.generate_content_with_Structured_schema(
                    system_instruction=system_instruction,
                    query=query,
                    response_schema=response_schema)
                sub_goals_list = response.array
                if not isinstance(sub_goals_list, list):
                    raise ValueError("Response is not as expected")
                print("generated subgoals: ", sub_goals_list)
                for sub_goal_string in sub_goals_list:
                    system_instruction = """You are an AI assistant designed to generate KPIs for sub-goals of an AI agent. 
                           Return your response as a JSON list of kpis.
                           """

                    query = f"""Generate at least two KPIs that you think this sub-goal should be measured against. make sure to make it short and one sentence
                            These KPIs need to be quantified and measurable.
                            user persona: {report['user_persona']}
                            specific needs: {specific_needs}
                            agent KPIs: {agent_kpis}
                            Goal: {goal.goal}
                            Goal KPIs: {goal_kpis}
                            Sub-goal: {sub_goal_string}
                            """

                    response_schema = ArraySchema
                    response = self.llm_service.generate_content_with_Structured_schema(
                        system_instruction=system_instruction,
                        query=query,
                        response_schema=response_schema)
                    kpis_list = response.array
                    if not isinstance(kpis_list, list):
                        raise ValueError("Response is not as expected")
                    kpis = []
                    for kpi in kpis_list:
                        system_instruction = """You are an AI assistant designed to help users create personalized agents."""
                        query = f"""Generate an expected value for the KPI provided below according to the user persona, specific needs, agent KPIs, goal, and sub-goal. make sure to make it short and one sentence
                                user persona: {report['user_persona']}
                                specific needs: {specific_needs}
                                agent KPIs: {agent_kpis}
                                goal: {goal.goal}
                                goal KPIs: {goal_kpis}  
                                sub-goal: {sub_goal_string} 
                                KPI: {kpi}  
                                """

                        response_schema = StringSchema
                        response = self.llm_service.generate_content_with_Structured_schema(
                            system_instruction=system_instruction,
                            query=query,
                            response_schema=response_schema)
                        if not isinstance(response.string, str):
                            raise ValueError("Response is not as expected")
                        kpi_obj = KPI(kpi=kpi, expected_value=response.string)
                        kpis.append(kpi_obj)

                    sub_goal_obj = SubGoal(sub_goal_id=uuid.uuid4().hex,
                                           goal_id=goal.id,
                                           agent_id=goal.agent_id,
                                           sub_goal=sub_goal_string,
                                           kpis=kpis)

                    
                    sub_goal_data = [{
                        "name": sub_goal_string,
                        "description": f"Sub-goal for role {role} with goal '{goal.goal}': {sub_goal_string}",
                        "type": "sub_goal"
                    }]
                    self.embedding_service.add_entities(sub_goal_data, "sub_goal")

                    sub_goals.append(sub_goal_obj)

            self_reflection.subgoals = sub_goals
            self.self_reflection_repository.update_self_reflection(self_reflection)

            return sub_goals

        except Exception as e:
            raise RuntimeError(f"Error generating sub-goals: {str(e)}")

    @retry(max_retries=5, delay=2)
    def generate_workstreams(self, role: str, report: dict,
                             sub_goals: list[SubGoal],
                             available_apis: list, self_reflection: SelfReflection) -> list[Workstream]:
        try:
            specific_needs = ','.join(report['specific_needs'])
            agent_kpis = ','.join([
                f"{kpi['kpi']} with expected value {kpi['expected_value']}"
                for kpi in report['kpis']
            ])
            workstreams = []

            for sub_goal in sub_goals:
                sub_goal_kpis = ','.join([
                    f"{kpi.kpi} with expected value {kpi.expected_value}"
                    for kpi in sub_goal.kpis
                ])

                max_attempts = 3  # Limit the number of attempts for verification
                attempts = 0
                workstreams_dict = None

                while attempts < max_attempts:  # Attempt verification only a limited number of times
                    query = f"""
                    Return all of the APIs we have available.
                    """    
                    relevant_apis = self._get_relevant_entities(query=query, entity_type="api")
                    apis_context = "\n".join([f"{api['name']}: {api['description']}" for api in relevant_apis[:5]])
                    
                    sub_goal_descriptions = self._get_relevant_entities(query=query, entity_type="sub_goal")

                    system_instruction = """You are an AI assistant designed to help users create personalized agents."""
                    query = f"""
                    Generate 2 workstreams to achieve the sub-goal provided below for the AI {role} with the specified user persona specific needs. The workstreams should be doable by the available apis. The frequency should be one of the following: daily, weekly, monthly, quarterly, yearly. Make sure to add relevant KPIs with the expected value to each workstream.
                    user persona : {report['user_persona']}
                    specific needs : {specific_needs}
                    agent kpis: {agent_kpis}
                    sub-goal : {sub_goal.sub_goal}
                    sub-goal kpis : {sub_goal_kpis}
                    available apis : {','.join(available_apis)}
                    Sub-goals:
                    {sub_goal_descriptions}

                    Available APIs:
                    {apis_context}
                    """

                    response_schema = workstreams_schema
                    response = self.llm_service.generate_content_with_json_format(
                        system_instruction=system_instruction,
                        query=query,
                        response_schema=response_schema)

                    res = json.loads(response)
                    workstreams_dict = res["workstreams"]
                    if not isinstance(workstreams_dict, list):
                        raise ValueError("Response is not a list as expected")

                    #Verify the generated workstreams
                    verified = all(
                        self.verify_node(
                            workstream['workstream'],
                            self.generate_nodes_apis(workstream['workstream'],
                                                     available_apis))
                        for workstream in workstreams_dict)
                    print("verification of workstreams: ", verified)
                    verified = True

                    if verified:
                        print("Workstreams verified")
                        break  # Break if verification succeeds
                    else:
                        print(
                            f"Verification failed, retrying... (Attempt {attempts + 1})"
                        )
                        attempts += 1  # Increment attempt count

                if not workstreams_dict or not verified:
                    raise RuntimeError(
                        "Failed to generate valid workstreams after multiple attempts"
                    )

                for workstream_dict in workstreams_dict:
                    max_task_attempts = 3  # Limit task generation retries
                    task_attempts = 0
                    module_list = None

                    while task_attempts < max_task_attempts:  # Retry for tasks verification
                        system_instruction = """You are an AI assistant designed to help users create personalized agents."""
                        query = f"""Generate 2 tasks that break down the specific workstream into smaller, manageable components. Each task should represent a distinct task or process necessary to achieve the overall goal of the workstream. also make sure that the tasks are doable by the available apis. Since the generated tasks are going to be verified make sure to improve and change the task if it is not doable by the available apis.
                                    user persona : {report['user_persona']}
                                    specific needs : {specific_needs}
                                    agent kpis: {agent_kpis}
                                    sub-goal : {sub_goal.sub_goal}
                                    sub-goal kpis : {sub_goal_kpis}
                                    workstream : {workstream_dict['workstream']}
                                    available apis : {','.join(available_apis)}
                                    """
                        response_schema = modules_schema

                        response = self.llm_service.generate_content_with_json_format(
                            system_instruction=system_instruction,
                            query=query,
                            response_schema=response_schema)

                        module_list = json.loads(response)["modules"]
                        if not isinstance(module_list, list):
                            raise ValueError(
                                "Response is not a list as expected")

                        #Verify the tasks
                        verified = all(
                            self.verify_node(
                                module,
                                self.generate_nodes_apis(
                                    module, available_apis))
                            for module in module_list)
                        verified = True

                        if verified:
                            print("modules verified")
                            break
                        else:
                            print(
                                f"Task verification failed, retrying... (Attempt {task_attempts + 1})"
                            )
                            task_attempts += 1

                    if not module_list or not verified:
                        raise RuntimeError(
                            "Failed to generate valid tasks after multiple attempts"
                        )

                    modules = []
                    for module_dict in module_list:
                        module = module_dict["module"]
                        freq_module = module_dict["frequency"]
                        system_instruction = """You are an AI assistant designed to help users create personalized agents."""
                        query = f"""Generate at least 2 kpis for the task provided below according to the user persona, specific needs, agent KPIs, sub-goal, workstream, and task. make sure to make it short and one sentence
                                user persona: {report['user_persona']}
                                specific needs: {specific_needs}
                                sub-goal: {sub_goal.sub_goal}
                                workstream: {workstream_dict['workstream']}
                                workstream kpis: {','.join([f"{kpi['kpi']} with expected value {kpi['expected_value']}" for kpi in workstream_dict['kpis']])}
                                task: {module}
                                """

                        response_schema = ArraySchema
                        response = self.llm_service.generate_content_with_Structured_schema(
                            system_instruction=system_instruction,
                            query=query,
                            response_schema=response_schema)
                        module_kpis = response.array
                        print("module_kpis123", module_kpis)
                        if not isinstance(module_kpis, list):
                            raise ValueError(
                                "Module KPIs Response is not as expected")
                        kpis = []
                        for kpi in module_kpis:
                            system_instruction = """You are an AI assistant designed to help users create personalized agents."""
                            query = f"""Generate an expected value for the KPI provided below according to the user persona, specific needs, agent KPIs, sub-goal, workstream, task, and kpi. make sure to make it short and one sentence
                                    user persona: {report['user_persona']}
                                    specific needs: {specific_needs}
                                    agent KPIs: {agent_kpis}
                                    sub-goal: {sub_goal.sub_goal}
                                    sub-goal KPIs: {sub_goal_kpis}
                                    workstream: {workstream_dict['workstream']}
                                    workstream kpis: {','.join([f"{kpi['kpi']} with expected value {kpi['expected_value']}" for kpi in workstream_dict['kpis']])}
                                    task: {module}
                                    KPI: {kpi}
                                    """

                            response_schema = StringSchema
                            response = self.llm_service.generate_content_with_Structured_schema(
                                system_instruction=system_instruction,
                                query=query,
                                response_schema=response_schema)
                            print("detail kpi module", response)
                            if not isinstance(response.string, str):
                                raise ValueError(
                                    "Module KPI Details Response is not as expected"
                                )
                            kpi_obj = {
                                'kpi': kpi,
                                'expected_value': response.string
                            }
                            kpis.append(kpi_obj)

                        print(f"module_object-{freq_module}-")
                        
                        #get the apis for the module by multi-traversing the tree
                        modules_apis = API_Utils().multi_traverse_api_tree(module)
                        module_obj = {
                            'module': module,
                            'kpis': kpis,
                            'frequency': freq_module,
                            'apis': modules_apis
                        }

                        modules.append(module_obj)
                        print("added module", module_obj)

                    workstream_dict['modules'] = modules
                    workstream = Workstream.from_dict(workstream_dict)
                    workstream.id = uuid.uuid4().hex
                    workstream.sub_goal_id = sub_goal.id
                    workstream.goal_id = sub_goal.goal_id
                    workstream.agent_id = sub_goal.agent_id

                    workstream_data = [{
                        "name": workstream_dict["workstream"],
                        "description": f"Workstream for sub-goal '{sub_goal.sub_goal}' with role '{role}': {workstream_dict['workstream']}",
                        "type": "workstream"
                    }]
                    self.embedding_service.add_entities(workstream_data, "workstream")

                    workstreams.append(workstream)
                    print("appenddeddddddddddddddddddddddddd")
            print('Workstreams generated')
            self_reflection.workstreams = workstreams
            self.self_reflection_repository.update_self_reflection(self_reflection)

            return workstreams

        except Exception as e:
            print(e)
            raise RuntimeError(f"Error generating workstreams: {str(e)}")
    

    def generate_skills(self, role, specific_needs, self_reflection,agent_id) -> list:
        specific_needs = ','.join(specific_needs)
        system_instruction = """You are an AI assistant designed to help users generate skills for an AI agent."""
        query = f"""generate a list of skills that you think this AI {role} should have. These skills should be relevant to the role and help achieve the specified goals.
        specific needs : {specific_needs}
        self reflection : {self_reflection}
        Return your response as a JSON list of skill strings according to the response schema provided and makesure its length is not morethan 6.
        """

        response_schema = ArraySchema
        skills_string = []
        max_retries = 5
                
        response = self.llm_service.generate_content_with_Structured_schema(
            system_instruction=system_instruction,
            query=query,
            response_schema=response_schema
        )
            
        print("response", response.array) 
            

        # for skill in response.array:
        #     self.skill_repository.create_skill(Skill(id=uuid.uuid4().hex, agent_id=agent_id, name=skill))
        
        return response.array

    def generate_traits(self, role, specific_needs, self_reflection):
        specific_needs = ','.join(specific_needs)
        system_instruction = """You are an AI assistant designed to help users generate traits for an AI agent."""
        query = f"""generate a list of traits that you think this AI {role} should have. These traits should be relevant to the role and help achieve the specified goals.
        specific needs : {specific_needs}
        self reflection : {self_reflection} 
        Return your response as a JSON list of trait strings according to the response schema provided and makesure its length is not morethan 4.
        """

        response_schema = ArraySchema
        traits_string = []
        max_retries = 5
                
        response = self.llm_service.generate_content_with_Structured_schema(
            system_instruction=system_instruction,
            query=query,
            response_schema=response_schema
        )
            
        print("response", response.array)
        
        return response.array
    
    
    def generate_tags(self, role, specific_needs, self_reflection):
        specific_needs = ','.join(specific_needs)
        system_instruction = """You are an AI assistant designed to help users generate tags for an AI agent."""
        query = f"""generate a list of tags that you think this AI {role} should have. These tags should be relevant to the role and help achieve the specified goals.
        specific needs : {specific_needs}
        self reflection : {self_reflection} 
        Return your response as a JSON list of tag strings according to the response schema provided and makesure its length is not morethan 5.
        """

        response_schema = ArraySchema
        tags_string = []
        max_retries = 5
                
        response = self.llm_service.generate_content_with_Structured_schema(
            system_instruction=system_instruction,
            query=query,
            response_schema=response_schema
        )
            
        print("response", response.array)
        
        return response.array
            

    def generate_category(self, role: str, traits: List[str], skills: List[str]) -> str:
        """Generate the most suitable category for the agent based on its role, traits, and skills."""
        system_instruction = """You are an AI assistant designed to categorize AI agents into predefined categories."""
        
        # Get categories from database
        categories = self.category_repository.get_all_categories()
        categories_str = "\n".join([f"- {cat.name}: {cat.description}" for cat in categories])
        
        query = f"""Based on the following agent characteristics, select the most suitable category from the list below.
        
        Agent Role: {role}
        Traits: {', '.join(traits)}
        Skills: {', '.join(skills)}
        
        Available Categories:
        {categories_str}
        
        Return only the category name that best matches this agent's characteristics."""
        
        response_schema = StringSchema

        response = self.llm_service.generate_content_with_Structured_schema(
            system_instruction=system_instruction,
            query=query,
            response_schema=response_schema
        )
        
        print('Categories: ', categories)
        print('Response: ', response )
        
        
        # Get the string value from the response and clean it up
        selected_category_name = response.string.strip()
        
        print('Selected Category Name: ', selected_category_name)
        
        # Find the matching category from database
        for category in categories:
            if category.name.lower() == selected_category_name.lower():
                return category.id  # Return category ID instead of name
        
        # If no exact match, return the first category's ID as default
        return categories[0].name if categories else None

    def create_agent(self, agent: Agent, goals: list[Goal],
                     sub_goals: list[SubGoal],
                     workstreams: list[Workstream], skills, agent_id: str, traits, tags) -> None:
        try:
            for workstream in workstreams:
                self.workstream_repository.create_workstream(workstream)
            print('workstreams stored in db')

            for sub_goal in sub_goals:
                self.sub_goal_repository.create_sub_goal(sub_goal)
            print('sub goals stored in db')

            for goal in goals:
                self.goal_repository.create_goal(goal)
            print('goals stored in db')
            
            self.skill_repository.create_skill(Skill(id=uuid.uuid4().hex, agent_id=agent_id, skill=skills))
            print('Skills stored in db')
            
            self.traits_repository.create_trait(Traits(id=uuid.uuid4().hex, agent_id=agent_id, traits=traits))
            print('Traits stored in db')
            
            self.tags_repository.create_tag(Tags(id=uuid.uuid4().hex, agent_id=agent_id, tags=tags))
            print('Tags stored in db')
            
            # Set the category_id in the agent model
            category_id = self.generate_category(agent.role, traits, skills)
            agent.category_id = category_id
            print('Category ID set in agent model')

            self.agent_repository.create_agent(agent)
            print('agent stored in db')
        except Exception as e:
            raise RuntimeError(f"Error creating agent: {str(e)}")

    def schedule_workstreams(self, workstreams: list[Workstream],
                             domain_name: str) -> None:
        # Schedule the workstreams for the newly created agent
        try:
            for i, workstream in enumerate(workstreams):
                job_name = f"Execute-Workstream-{i}-With-ID-{workstream.id}-for-AI_Agent-With-ID-{workstream.agent_id}"
                uri = f"{domain_name}/agents/workstream/execute"
                http_method = "POST"
                body = {"workstream": workstream}
                frequency = workstream.frequency
                description = f"Job to execute workstream with ID: {workstream.id}"

                self.scheduling_service.schedule_http_job(
                    job_name, uri, http_method, body, frequency, description)

        except Exception as e:
            raise RuntimeError(f"Error scheduling workstreams: {str(e)}")

    def schedule_feedbacks(self, agent_id: str, domain_name: str,
                           frequency: str) -> None:
        try:
            job_name = f"Implicit Feedback Analysis-for-AI_Agent-With-ID-{agent_id}"
            uri = f"{domain_name}/agents/feedbacks/implicit"
            http_method = "POST"
            body = {"agent_id": agent_id}
            frequency = frequency
            description = f"Agent with ID: {agent_id} is scheduled for implicit feedback analysis."

            self.scheduling_service.schedule_http_job(job_name, uri,
                                                      http_method, body,
                                                      frequency, description)

        except Exception as e:
            raise RuntimeError(
                f"Error analyzing performance of agent: {str(e)}")

    def generate_relevant_apis(self, role: str, description: dict) -> list:
        apis = [
            'binance_api', 'cdc_api', 'crunchbase_api',
            'ecb_exchange_rates_api', 'free_forex_api',
            'github_search_api_call', 'guardian_media_api', 'health_care_api',
            'human_api', 'hunter_email_api', 'news_api',
            'open_fda_api', 'quickbook_api', 'slack_api', 'statista_api_call'
        ]

        try:
            system_instruction = """You are an AI assistant designed to help users create personalized agents."""
            query = f"""
            You are given a role: {role}, a description: "{description}", and a list of APIs: {apis}. 
            You should return a list of relevant API names from the provided list that would help accomplish the tasks associated with the role and description.
            Return the result as a JSON array of API names.
            """

            response_schema = ArraySchema
            response = self.llm_service.generate_content_with_Structured_schema(
                system_instruction=system_instruction,
                query=query,
                response_schema=response_schema)
            print(response)
            parsed_response = response.array

            return parsed_response
        except Exception as e:
            raise RuntimeError(
                f"Error creating relevant apis for the agent: {str(e)}")

    def verify_node(self, description: str, apis: list) -> bool:
        try:
            system_instruction = """
            You are an AI assistant tasked with evaluating whether a specified action can be executed using the provided APIs. 
            Assess the feasibility of achieving the described action using the available functionality of these APIs.
            """
            query = f"""
            You are given an action description: "{description}", and a list of APIs: {apis}.
            Determine if the action can be performed using the provided APIs.
            Return a boolean value indicating whether the action is achievable using these APIs.
            """

            response_schema = BooleanSchema
            response = self.llm_service.generate_content_with_Structured_schema(
                system_instruction=system_instruction,
                query=query,
                response_schema=response_schema)
            print(response)
            parsed_response = response.boolean

            return parsed_response
        except Exception as e:
            raise RuntimeError(
                f"Error verifying node feasibility with APIs: {str(e)}")

    def generate_nodes_apis(self, node, apis: list) -> list:
        try:
            system_instruction = """
            You are an AI assistant tasked with generating a list of APIs that can be used to perform a specific action.
            Assess the feasibility of achieving the described action using the available functionality of these APIs.
            """
            query = f"""
            You are given a node: {node}, and a list of APIs: {apis}.
            Generate a list of APIs that can be used to perform the action associated with the node.
            Return the result as a JSON array of API names.
            """

            response_schema = ArraySchema
            response = self.llm_service.generate_content_with_Structured_schema(
                system_instruction=system_instruction,
                query=query,
                response_schema=response_schema)
            print(response)
            parsed_response = response.array

            return parsed_response
        except Exception as e:
            raise RuntimeError(
                f"Error generating nodes APIs for the agent: {str(e)}")
    def validate_role_ethics(self,role, description):

        try:
            openai_llm = OpenAiLLMService(model_name="gpt-4o-2024-08-06", api_key=os.getenv('OPENAI_API_KEY'))
            system_instruction = (
                "You are an ethics compliance evaluator for company. Validate if a role and its description align with basic ethical guidelines "
                "and do not cause harm. Respond in the structured schema format provided."
            )
            query = f"Role: {role}\nDescription: {description}"
            response_schema = {
                "type": "json_schema",
                "json_schema": {
                "name": "validate_role",
                "schema": {
                    "type": "object",
                "properties": {
                    "is_ethical": {
                        "type": "boolean",
                        "description": "Indicates whether the role is ethical."
                    },
                    "explanation": {
                        "type": "string",
                        "description": "Provides a brief explanation for the ethical evaluation."
                    }
                },
                "required": ["is_ethical", "explanation"]
            }
            }
            }
            result = openai_llm.generate_content_with_json_format(
                system_instruction=system_instruction,
                query=query,
                response_schema=response_schema
            )
            result=json.loads(result)
            print(type(result))
            is_ethical = result["is_ethical"]
            explanation = result["explanation"]
            return is_ethical, explanation
        except Exception as e:
            return False, f"Error during role validation: {str(e)}"
        
        
    def validate_user_input(self, role, input):
        try:
            openai_llm = OpenAiLLMService(model_name="gpt-4o-2024-08-06", api_key=os.getenv('OPENAI_API_KEY'))
            system_instruction = (
                "You are an ethics compliance evaluator for our company. Validate if a role and its description align with basic ethical guidelines "
                "and do not cause harm. Respond in the structured schema format provided."
            )
            if isinstance(input, list):
                input = " ".join(input)
            query = f"Role: {role}\nDescription: {input}"
            response_schema = {
                "type": "json_schema",
                "json_schema": {
                "name": "validate_role",
                "schema": {
                    "type": "object",
                "properties": {
                    "is_ethical": {
                        "type": "boolean",
                        "description": "Indicates whether the role is ethical."
                    },
                    "explanation": {
                        "type": "string",
                        "description": "Provides a brief explanation for the ethical evaluation."
                    }
                },
                "required": ["is_ethical", "explanation"]
            }
            }
            }
            result = openai_llm.generate_content_with_json_format(
                system_instruction=system_instruction,
                query=query,
                response_schema=response_schema
            )
            result=json.loads(result)
            is_ethical = result["is_ethical"]
            explanation = result["explanation"]
            return is_ethical, explanation
        except Exception as e:
            return False, f"Error during role validation: {str(e)}"

    
    def check_api_availability_in_user_input(self,input):
        try:
            system_instruction=('''
            You are a user input analyzer for our application. Analyze the provided input to determine if it explicitly mentions any API.
             Consider any phrasing or context that refers to APIs, such as API names, endpoints, or API-related terms. Return a boolean value (True or False)
              indicating whether an API is mentioned in the input. 
            ''')

            query = f"user input: {input}"
            response_schema = {
                "type": "json_schema",
                "json_schema": {
                    "name": "check_api_availability",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "api_mentioned": {
                                "type": "boolean",
                                "description": "Indicates whether an API is mentioned in the user input."
                            }
                        },
                        "required": ["api_mentioned"]
                    }
                }
            }

            response_schema = BooleanSchema
            response = self.llm_service.generate_content_with_Structured_schema(
                system_instruction=system_instruction,
                query=query,
                response_schema=response_schema)
            parsed_response = response.boolean
            print(parsed_response)
            return parsed_response

        except Exception as e:
            return False, f"Error during user input check: {str(e)}"

    def get_agents(self) -> List[Agent]:
        """Fetch all agents from the repository."""
        try:
            agents = self.agent_repository.get_all_agents()
            return agents
        except Exception as e:
            raise RuntimeError(f"Error fetching agents: {str(e)}")
    
    def get_skills(self) -> List[Skill]:
        """Fetch all skills from the repository."""
        try:
            skills = self.skill_repository.get_all_skills()
            print(skills, "skills")
            return skills
        except Exception as e:
            raise RuntimeError(f"Error fetching skills: {str(e)}")
    
    def get_skills_by_agent_id(self, agent_id: str) -> List[Skill]:
        try:
            skills = self.skill_repository.get_skills_by_agent_id(agent_id)
            return skills
        except Exception as e:
            raise RuntimeError(f"Error fetching skills: {str(e)}")
        
        

    def get_traits(self) -> List[Traits]:
        """Fetch all traits from the repository."""
        try:
            traits = self.traits_repository.get_all_traits()
            return traits
        except Exception as e:
            raise RuntimeError(f"Error fetching traits: {str(e)}")
    
    def get_traits_by_agent_id(self, agent_id: str) -> List[Traits]:
        try:
            traits = self.traits_repository.get_traits_by_agent_id(agent_id)
            return traits
        except Exception as e:
            raise RuntimeError(f"Error fetching traits: {str(e)}")

    def get_tags(self) -> List[Tags]:
        """Fetch all tags from the repository."""
        try:
            tags = self.tags_repository.get_all_tags()
            return tags
        except Exception as e:
            raise RuntimeError(f"Error fetching tags: {str(e)}")
    
    def get_tags_by_agent_id(self, agent_id: str) -> List[Tags]:
        try:
            tags = self.tags_repository.get_tags_by_agent_id(agent_id)
            return tags
        except Exception as e:
            raise RuntimeError(f"Error fetching tags: {str(e)}")