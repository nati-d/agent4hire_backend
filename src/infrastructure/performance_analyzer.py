import json
from domain.models.agent import Agent
from domain.models.goal import Goal
from domain.models.module import Module
from domain.models.sub_goal import SubGoal
from domain.models.workstream import Workstream
from infrastructure.llm.llm_service import LLMService

from typing_extensions import TypedDict

class PerformanceSchema(TypedDict):
    kpi: str
    value: str

class PerformanceAnalyzer:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    def analyze_module_performance(self, module: Module, module_execution_output: str) -> dict:
        system_instruction = """You are a data scientist at a large company. Your task is to analyze the performance of a module executed by an ai agent."""
        response_type = 'application/json'
        prompt = f"""The following module is executed by an AI Agent. Analyze the performance of the module based on the execution data and the metrics used to track its performance provided below.
                     Module: {module.module}
                    Execution Output: {module_execution_output}
                    Metrics: {[kpi.to_dict() for kpi in module.kpis]}
                    Return a json object according to the given schema.
                    """
        
        response_schema = list[PerformanceSchema]

        response = self.llm_service.generate_content(system_instruction, prompt, response_type, response_schema)
        performance_list = json.loads(response)
        result = {
            performance['kpi']: performance['value'] for performance in performance_list
        }
        return result

    
    def analyze_workstream_performance(self, workstream: Workstream, modules_performance: list[dict]) -> dict:
        system_instruction = """You are a data scientist at a large company. Your task is to analyze the performance of a workstream executed by an ai agent."""
        response_type = 'application/json'
        print('wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww')

        modules_data = "\n".join(
            [f"module -> {module.to_dict()}: performance -> {performance}" for module, performance in zip(workstream.modules, modules_performance)]
        )

        prompt = f"""The following workstream is executed by an AI Agent. Analyze the performance of the workstream based on the performance data of its modules and the metrics used to track its performance provided below.
                    Workstream: {workstream.workstream}
                    Modules Performance Data: {chr(10).join([f"module -> {module.to_dict()}: performance -> {performance}" for module, performance in zip(workstream.modules, modules_performance)])}
                    Workstream Metrics: {workstream.kpis}
                    Return a json object according to the given schema. The kpis should be the kpis of the workstream.
                    """

        response_schema = list[PerformanceSchema]

        response = self.llm_service.generate_content(system_instruction, prompt, response_type, response_schema)
        performance_list = json.loads(response)
        result = {
            performance['kpi']: performance['value'] for performance in performance_list
        }

        return result

    
    def analyze_sub_goal_performance(self, sub_goal: SubGoal, workstream: Workstream, workstream_performance: list[dict]) -> dict:
        system_instruction = """You are a data scientist at a large company. Your task is to analyze the achievement of a sub-goal using the performance data of the workstreams of the sub-goal that are executed by an ai agent."""
        response_type = 'application/json'
        prompt = f"""Analyze the achievement of the sub-goal based on the performance data of its workstream and the metrics used to track its performance provided below.
                    Sub-Goal: {sub_goal.sub_goal}
                    Workstream Performance Data: 
                        workstream: {workstream.to_dict()}
                        performance: {workstream_performance}
                    Sub-Goal Metrics: {sub_goal.kpis}
                    Return a json object according to the given schema. The kpis should be the kpis of the sub-goal.
                    """
        response_schema = list[PerformanceSchema]
        
        response = self.llm_service.generate_content(system_instruction, prompt, response_type, response_schema)
        performance_list = json.loads(response)
        result = {
            performance['kpi']: performance['value'] for performance in performance_list
        }
        return result
    
    def analyze_goal_performance(self, goal: Goal,sub_goal: SubGoal, sub_goal_performance: list[dict]) -> dict:
        system_instruction = """You are a data scientist at a large company. Your task is to analyze the achievement of a goal using the performance data of the sub-goals of the goal that are executed by an ai agent."""
        response_type = 'application/json'
        prompt = f"""Analyze the achievement of the goal based on the performance data of its sub-goals and the metrics used to track its performance provided below.
                    Goal: {goal.goal}
                    Sub-Goals Performance Data: 
                        sub-goal: {sub_goal}
                        performance; {sub_goal_performance}
                    Goal Metrics: {goal.kpis}
                    Return a json object according to the given schema. The kpis should be the kpis of the goal.
                    """
        response_schema = list[PerformanceSchema]
        
        response = self.llm_service.generate_content(system_instruction, prompt, response_type, response_schema)
        performance_list = json.loads(response)
        result = {
            performance['kpi']: performance['value'] for performance in performance_list
        }
        return result
    
    def analyze_agent_performance(self, agent: Agent, goal: Goal, goal_performance: list[dict]) -> dict:
        system_instruction = """You are a data scientist at a large company. Your task is to analyze the performance of an agent based on the performance data of the goals of the agent that are executed"""
        response_type = 'application/json'
        prompt = f"""Analyze the performance of the agent based on the performance data of its goal and the metrics used to track its performance provided below. 
                    Agent:
                        description: {agent.description}
                        kpis: {[kpi.to_dict() for kpi in agent.kpis]}
                    Goal Performance Data:
                        goal: {goal.goal}
                        performance: {goal_performance}
                    Return a json object according to the given schema. The kpis should be the kpis of the agent.   
                    """
        
        response_schema = list[PerformanceSchema]

        response = self.llm_service.generate_content(system_instruction, prompt, response_type, response_schema)
        performance_list = json.loads(response)
        result = {
            performance['kpi']: performance['value'] for performance in performance_list
        }
        return result
    
    def update_performance_data(self, prev_performance_data: dict, curr_performance_data: dict) -> dict:
        system_instruction = """You are a data scientist at a large company. Your task is to update the performance data on the previous and current performance data."""
        response_type = 'application/json'
        prompt = f"""Update the performance data based on the previous and current performance data provided below.
                    Previous Performance Data: {prev_performance_data}
                    Current Performance Data: {curr_performance_data}
                    Return a json object according to the given schema with the updated data.
                    """
        response_schema = list[PerformanceSchema]
        
        response = self.llm_service.generate_content(system_instruction, prompt, response_type, response_schema)

        performance_list = json.loads(response)
        result = {
            performance['kpi']: performance['value'] for performance in performance_list
        }
        return result