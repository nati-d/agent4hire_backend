import typing_extensions
import json
import uuid
import google.generativeai as genai
from infrastructure.repositories.agent_repository import AgentRepository
from infrastructure.repositories.goal_repository import GoalRepository
from infrastructure.repositories.sub_goal_repository import SubGoalRepository
from infrastructure.repositories.workstream_repository import WorkstreamRepository
from infrastructure.llm.llm_service import LLMService
from domain.models.goal import Goal
from domain.models.sub_goal import SubGoal
from domain.models.workstream import Workstream
from domain.models.module import Module
from domain.models.agent import Agent
import google.generativeai as genai


# Schema for RelevantNodes
relevant_nodes_schema = genai.protos.Schema(
    type=genai.protos.Type.OBJECT,
    properties={
        'nodes': genai.protos.Schema(
            type=genai.protos.Type.ARRAY,
            items=genai.protos.Schema(type=genai.protos.Type.STRING)
        )
    },
    required=['nodes']
)

# Schema for MetExpectation
met_expectation_schema = genai.protos.Schema(
    type=genai.protos.Type.OBJECT,
    properties={
        'met_expectation': genai.protos.Schema(type=genai.protos.Type.BOOLEAN)
    },
    required=['met_expectation']
)

# Schema for ImproveNode
improve_node_schema = genai.protos.Schema(
    type=genai.protos.Type.OBJECT,
    properties={
        'improved_node': genai.protos.Schema(type=genai.protos.Type.STRING)
    },
    required=['improved_node']
)

# Schema for KPISchema
kpi_schema = genai.protos.Schema(
    type=genai.protos.Type.OBJECT,
    properties={
        'kpi': genai.protos.Schema(type=genai.protos.Type.STRING),
        'expected_value': genai.protos.Schema(type=genai.protos.Type.STRING)
    },
    required=['kpi', 'expected_value']
)

# Schema for GoalSchema
goal_schema = genai.protos.Schema(
    type=genai.protos.Type.OBJECT,
    properties={
        'id': genai.protos.Schema(type=genai.protos.Type.STRING),
        'agent_id': genai.protos.Schema(type=genai.protos.Type.STRING),
        'goal': genai.protos.Schema(type=genai.protos.Type.STRING),
        'kpis': genai.protos.Schema(
            type=genai.protos.Type.ARRAY,
            items=kpi_schema
        )
    },
    required=['goal', 'kpis']
)

# Schema for SubGoalSchema
sub_goal_schema = genai.protos.Schema(
    type=genai.protos.Type.OBJECT,
    properties={
        'id': genai.protos.Schema(type=genai.protos.Type.STRING),
        'agent_id': genai.protos.Schema(type=genai.protos.Type.STRING),
        'goal_id': genai.protos.Schema(type=genai.protos.Type.STRING),
        'sub_goal': genai.protos.Schema(type=genai.protos.Type.STRING),
        'kpis': genai.protos.Schema(
            type=genai.protos.Type.ARRAY,
            items=kpi_schema
        ),
        
    },
    required=['sub_goal', 'kpis']
)

# Schema for ModuleSchema
module_schema = genai.protos.Schema(
    type=genai.protos.Type.OBJECT,
    properties={
        'module': genai.protos.Schema(type=genai.protos.Type.STRING),
        'kpis': genai.protos.Schema(
            type=genai.protos.Type.ARRAY,
            items=kpi_schema
        ),
        'frequency': genai.protos.Schema(type=genai.protos.Type.STRING),
        'apis': genai.protos.Schema(type=genai.protos.Type.ARRAY, items=genai.protos.Schema(type=genai.protos.Type.STRING))
    },
    required=['module', 'kpis', 'frequency', 'apis']
)

# Schema for WorkStreamSchema
workstream_schema = genai.protos.Schema(
    type=genai.protos.Type.OBJECT,
    properties={
        'id': genai.protos.Schema(type=genai.protos.Type.STRING),
        'agent_id': genai.protos.Schema(type=genai.protos.Type.STRING),
        'goal_id': genai.protos.Schema(type=genai.protos.Type.STRING),
        'sub_goal_id': genai.protos.Schema(type=genai.protos.Type.STRING),
        'workstream': genai.protos.Schema(type=genai.protos.Type.STRING),
        'frequency': genai.protos.Schema(type=genai.protos.Type.STRING),
        'kpis': genai.protos.Schema(
            type=genai.protos.Type.ARRAY,
            items=kpi_schema
        ),
        'modules': genai.protos.Schema(
            type=genai.protos.Type.ARRAY,
            items=module_schema
        ),   
    },
    required=['workstream', 'frequency', 'kpis', 'modules']
    
)

# schema for list of subgoals
sub_goals_schema = genai.protos.Schema(
    type=genai.protos.Type.ARRAY,
    items=sub_goal_schema
)

goals_schema = genai.protos.Schema(
    type=genai.protos.Type.ARRAY,
    items=goal_schema
)

workstreams_schema = genai.protos.Schema(
    type=genai.protos.Type.ARRAY,
    items=workstream_schema
)

teammate_feedback_schema = genai.protos.Schema(
    type=genai.protos.Type.OBJECT,
    properties={
        'teammate_id': genai.protos.Schema(type=genai.protos.Type.STRING),
        'feedback': genai.protos.Schema(type=genai.protos.Type.STRING)
    },
    required=['teammate_id', 'feedback']
)


def feedback_to_node_mapper(feedback: str, nodes: list, node_schema):
    llm = LLMService(model_name="gemini-1.5-flash")
    system_instruction = (
        "You are an intelligent agent that analyzes user feedback and selects relevant nodes based strictly on their relevance to the feedback. "
        "Only return nodes from the provided list, matching each node exactly as given, including all its properties."
    )

    # Explicitly listing out the nodes as JSON objects in the query
    nodes_listed = ", ".join([json.dumps(node.to_dict()) for node in nodes])

    query = (
        f"Given the feedback: '{feedback}', and the following list of nodes: [{nodes_listed}], "
        "return only the nodes from this list that are relevant as a JSON list. "
        "Each node in the response must match one from the provided list, with all properties exactly as they appear. "
        "Do not introduce any new nodes, properties, or modify any values. If no relevant nodes are found, return an empty list."
    )

    try:
        response = llm.generate_content(
            system_instruction=system_instruction,
            query=query,
            response_type="application/json",
            response_schema=node_schema
        )
        parsed_response = json.loads(response)

        return parsed_response

    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        print("Raw response that caused the error:", response)
        raise e

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise e


def is_expectation_met(metrics, progress):
    llm = LLMService(model_name="gemini-1.5-flash")
    system_instruction = "You are an intelligent agent that evaluates whether the performance metrics meet the user's expectations."
    query = f"""
    Based on the following metrics: {metrics}, and the progress of the agent: {progress}, determine if the expectation is met. 
    Respond with 'true' if met, otherwise 'false', using the JSON format.
    """

    try:
        response = llm.generate_content(system_instruction=system_instruction,
                                        query=query,
                                        response_type="application/json",
                                        response_schema=met_expectation_schema)
        parsed_response = json.loads(response)

        print(f"Response: {parsed_response}")

        return parsed_response.get('met_expectation')

    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        raise e

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise e


def generate_teammate_feedback(agent: dict, teammate: dict):
    llm = LLMService(model_name="gemini-1.5-flash")
    system_instruction = (
        "You are an intelligent agent that evaluates the performance of teammates based on their contributions "
        "to the agent's goals and expectations. Your task is to analyze the provided teammate's performance and "
        "generate constructive feedback to help them improve and better assist the agent in meeting its objectives."
    )
    query = (
        f"Analyze the performance of the teammate based on the agent's goals and expectations. "
        f"Agent details: {agent}. Teammate details: {teammate}. "
        f"Provide three feedback as a JSON object with a 'feedback' field containing the constructive suggestions."
    )

    try:
        response = llm.generate_content(
            system_instruction=system_instruction,
            query=query,
            response_type="application/json",
            response_schema=teammate_feedback_schema)
        parsed_response = json.loads(response)

        return parsed_response.get('feedback', "No feedback provided.")

    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        print("Raw response that caused the error:", response)
        raise e

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise e


def analyze_conversation_for_feedback(conversations: list[dict]) -> list[str]:
    llm = LLMService(model_name="gemini-1.5-flash")
    system_instruction = (
        "You are an intelligent assistant tasked with analyzing conversations between an agent and a user. "
        "Identify feedback for the agent based on their communication and the user's responses. "
        "Provide constructive feedback to help the agent improve their performance."
    )

    conversation_details = "\n".join(
        f"Agent: {conv['agent_message']} User: {conv['user_message']}"
        for conv in conversations)

    query = (
        f"Analyze the following conversation between an agent and a user:\n{conversation_details}\n"
        "Return feedback as a JSON list of strings, where each string is a feedback comment for the agent."
    )

    try:
        response = llm.generate_content(
            system_instruction=system_instruction,
            query=query,
            response_type="application/json",
            response_schema=genai.protos.Schema(
                type=genai.protos.Type.ARRAY,
                items=genai.protos.Schema(type=genai.protos.Type.STRING)))
        parsed_response = json.loads(response)

        return parsed_response

    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        print("Raw response that caused the error:", response)
        raise e

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise e


class GenerateNode:

    def generate_goal(self, agent: Agent, performance_data):
        llm = LLMService(model_name="gemini-1.5-flash")
        system_instruction = "You are an intelligent agent that generates a goal to help the agent meet its expectations."
        query = f"""
        Given the agent's description, generate a new goal that enables it to meet the expectations.
        agent role: {agent.role}
        agent description: {agent.description}
        agent kpi : {','.join([f"{kpi.kpi} with expected value {kpi.expected_value}" for kpi in agent.kpis])}
        agent progress: {performance_data}

        Return the generated goal as a JSON object.
        """

        try:
            response = llm.generate_content(
                system_instruction=system_instruction,
                query=query,
                response_type="application/json",
                response_schema=goal_schema)
            parsed_response = json.loads(response)

            return parsed_response

        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
            print("Raw response that caused the error:", response)
            raise e

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise e

    def generate_subgoals(self, goal: Goal, quantity, performance_data):
        llm = LLMService(model_name="gemini-1.5-flash")
        system_instruction = "You are an intelligent agent that generates a subgoal to help achieve the goal's expectations."
        query = f"""
        Given the goal's description, metrics, and expectations, generate {quantity} subgoals that enables it to meet the expectations.
        goal description: {goal.goal}
        goal kpis : {','.join([ f"{kpi.kpi} with expected value {kpi.expected_value}" for kpi in goal.kpis])}
        goal performance: {json.dumps(performance_data)}

        Return the generated subgoal as a JSON object.
        """

        try:
            response = llm.generate_content(
                system_instruction=system_instruction,
                query=query,
                response_type="application/json",
                response_schema=sub_goals_schema)
            parsed_response = json.loads(response)

            return parsed_response

        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
            print("Raw response that caused the error:", response)
            raise e

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise e

    def generate_workstreams(self, subgoal: SubGoal, quantity,
                             performance_data):
        llm = LLMService(model_name="gemini-1.5-flash")
        system_instruction = "You are an intelligent agent that generates a workstream to support the subgoal in meeting expectations."
        query = f"""
        Given the subgoal's description, metrics, and expectations, generate a new workstream that enables it to meet the expectations.
        subgoal description: {subgoal.sub_goal}
        goal kpis : {','.join([f"{kpi.kpi} with expected value {kpi.expected_value}" for kpi in subgoal.kpis])}
        subgoal progress: {performance_data}

        Return the generated workstream as a JSON object.
        """

        try:
            response = llm.generate_content(
                system_instruction=system_instruction,
                query=query,
                response_type="application/json",
                response_schema=workstreams_schema)
            parsed_response = json.loads(response)

            return parsed_response

        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
            print("Raw response that caused the error:", response)
            raise e

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise e


class ImproveNode:
    #is not returning the expected response schema more specifically it doesnt response the right schema for
    def improve_node(self, node, feedback, response_schema):

        llm = LLMService(model_name="gemini-1.5-flash")
        system_instruction = "You are an intelligent agent that improves nodes based on user feedback. Analyze and provide updates to enhance the node's attributes."
        query = f"""
        Based on the user feedback: '{feedback}', improvise the node's description, and KPIs. 
        The node details are: {json.dumps(node.to_dict())}. Return the improved node as a JSON object.
        """

        try:
            response = llm.generate_content(
                system_instruction=system_instruction,
                query=query,
                response_type="application/json",
                response_schema=response_schema)
            parsed_response = json.loads(response)
            return parsed_response

        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
            print("Raw response that caused the error:", response)
            raise e

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise e


class UserFeedbackUseCase:

    def __init__(self, agent_repository: AgentRepository,
                 goal_repository: GoalRepository,
                 subgoal_repository: SubGoalRepository,
                 workstream_repository: WorkstreamRepository):
        self.agent_repository = agent_repository
        self.goal_repository = goal_repository
        self.subgoal_repository = subgoal_repository
        self.workstream_repository = workstream_repository

    def add_feedback_to_agent(self, feedback: str, agent_id: str) -> None:
        try:
            agent = self.agent_repository.get_agent(agent_id)
            # append feedback to agent feedback list
            agent.feedbacks.append(feedback)
            self.agent_repository.update_agent(agent)
        except Exception as e:
            raise RuntimeError(
                f"Error adding feedback to agent {agent_id}: {str(e)}")

    def update_nodes_based_on_feedback(self, feedback: str,
                                       agent_id: str) -> None:
        # When we update the nodes we traverse each layer of the tree and
        # update the nodes that are relevant to the feedback
        improve_node = ImproveNode()
        try:
            agent = self.agent_repository.get_agent(agent_id)
            goals = self.goal_repository.get_goals_by_agent_id(agent_id)
            # Get the relevant goals related to the feedback
       
            relevant_goals = [
                Goal.from_dict(goal) for goal in feedback_to_node_mapper(
                    feedback, goals, goals_schema)
            ]

            for goal in relevant_goals:
                # print("relevant goal",goal.id)
                subgoals = self.subgoal_repository.get_sub_goals_by_goal_id(
                    goal.id)
                # print("fetched subgoals")
                print([f": {subgoal.sub_goal}" for subgoal in subgoals])
                relevant_subgoals = [
                    SubGoal.from_dict(subgoal)
                    for subgoal in feedback_to_node_mapper(
                        feedback, subgoals, sub_goals_schema)
                ]
                

                for subgoal in relevant_subgoals:
                    workstreams = self.workstream_repository.get_workstreams_by_sub_goal_id(
                        subgoal.id)
                    relevant_workstreams = [
                        Workstream.from_dict(workstream)
                        for workstream in feedback_to_node_mapper(
                            feedback, workstreams, workstreams_schema)
                    ]
                    print("relevant workstreams", relevant_workstreams)
                    for workstream in relevant_workstreams:
                        # Update workstreams based on the feedback
                        print("starting updating workstream")
                        improved_workstream = improve_node.improve_node(
                            workstream, feedback, workstream_schema)
                        print("improved workstream: ",improved_workstream)
                        # improved_workstream["agent_id"] = agent_id
                        # improved_workstream["goal_id"] = goal.id
                        # improved_workstream["sub_goal_id"] = subgoal.id
                        # improved_workstream["id"] = workstream.id
                        # improved_workstream["modules"] = workstream.modules
                        # improved_workstream["kpis"] = workstream.kpis
                        # improved_workstream["frequency"] = workstream.frequency
                        print("about to updateeeeee...................")
                        self.workstream_repository.update_workstream(
                            Workstream.from_dict(improved_workstream))
                    # Improve the subgoal based on the feedback
                    improved_subgoal = improve_node.improve_node(
                        subgoal, feedback, sub_goal_schema)
                    improved_subgoal["agent_id"] = agent_id
                    improved_subgoal["goal_id"] = goal.id
                    improved_subgoal["id"] = subgoal.id
                    self.subgoal_repository.update_sub_goal(
                        SubGoal.from_dict(improved_subgoal))
              

                # Update the relevant goals by improving them
                improved_goal = improve_node.improve_node(
                    goal, feedback, goal_schema)
                improved_goal["agent_id"] = agent_id
                improved_goal["id"] = goal.id
                self.goal_repository.update_goal(Goal.from_dict(improved_goal))
                

        except Exception as e:
            print(f"Error updating nodes based on feedback: {str(e)}")
            raise RuntimeError(
                f"Error updating nodes for agent {agent_id} based on feedback: {str(e)}"
            )

    


class ImplicitFeedbackUsecase:

    def __init__(self, agent_repository: AgentRepository,
                 goal_repository: GoalRepository,
                 subgoal_repository: SubGoalRepository,
                 workstream_repository: WorkstreamRepository):
        self.agent_repository = agent_repository
        self.goal_repository = goal_repository
        self.subgoal_repository = subgoal_repository
        self.workstream_repository = workstream_repository

    def implicitly_improve_agent(self, agent_id):
        generate_node = GenerateNode()
        try:
            agent = self.agent_repository.get_agent(agent_id)
            goals = self.goal_repository.get_goals_by_agent_id(agent_id)
            agent_performance = self.agent_repository.get_performance_data(agent_id)
            unmet_goals = []
            for goal in goals:
                goal_performance = self.goal_repository.get_performance_data(
                    goal.id)
                if not is_expectation_met(goal.kpis, goal_performance):
                    unmet_goals.append(goal)
            unmet_goals = []
            if not unmet_goals:
                new_node = generate_node.generate_goal(agent,
                                                       agent_performance)
                goal = Goal.from_dict(new_node)
                goal.id = uuid.uuid4().hex
                goal.agent_id = agent_id
                self.goal_repository.create_goal(goal)

                #we will generate subgoals for the new goal
                new_nodes = generate_node.generate_subgoals(
                    goal, 2, agent_performance)
                new_subgoals = [SubGoal.from_dict(node) for node in new_nodes]
                for subgoal in new_subgoals:
                    subgoal.agent_id = agent_id
                    subgoal.goal_id = goal.id
                    subgoal.id = uuid.uuid4().hex
                    self.subgoal_repository.create_sub_goal(subgoal)

                    #we will generate workstreams for the new subgoals
                    new_nodes = generate_node.generate_workstreams(
                        subgoal, 2, agent_performance)
                    new_workstreams = [
                        Workstream.from_dict(node) for node in new_nodes
                    ]
                    for workstream in new_workstreams:
                        workstream.agent_id = agent_id
                        workstream.goal_id = goal.id
                        workstream.sub_goal_id = subgoal.id
                        workstream.id = uuid.uuid4().hex
                        self.workstream_repository.create_workstream(
                            workstream)

            else:
                for goal in unmet_goals:
                    self.implicitly_improve_goal(goal.id)

        except Exception as e:
            print(f"An error occurred while implicitly improving agent: {e}")
            raise e

    def implicitly_improve_goal(self, goal_id):
        generate_node = GenerateNode()
        try:
            goal = self.goal_repository.get_goal(goal_id)
            subgoals = self.subgoal_repository.get_sub_goals_by_goal_id(
                goal_id)
            unmet_subgoals = []

            for subgoal in subgoals:
                subgoal_performance = self.subgoal_repository.get_performance_data(
                    subgoal.id)
                if not is_expectation_met(subgoal.kpis, subgoal_performance):
                    unmet_subgoals.append(subgoal)
            unmet_subgoals = []
            if not unmet_subgoals:
                # we will generate a new subgoal
                performance_data = self.goal_repository.get_performance_data(goal.id)
                new_node = generate_node.generate_subgoals(
                    goal, 1, performance_data)  #this will return list of one
                print("new node", new_node)
                new_subgoal = SubGoal.from_dict(new_node[0])
                new_subgoal.agent_id = goal.agent_id
                new_subgoal.goal_id = goal.id
                new_subgoal.id = uuid.uuid4().hex

                self.subgoal_repository.create_sub_goal(new_subgoal)

                #we will generate workstreams for the new subgoals
                new_nodes = generate_node.generate_workstreams(
                    new_subgoal, 2, performance_data)
                new_workstreams = [
                    Workstream.from_dict(node) for node in new_nodes
                ]
                for workstream in new_workstreams:
                    workstream.agent_id = goal.agent_id
                    workstream.goal_id = goal.id
                    workstream.sub_goal_id = new_subgoal.id
                    workstream.id = uuid.uuid4().hex
                    self.workstream_repository.create_workstream(workstream)

            else:
                for subgoal in unmet_subgoals:
                    self.implicitly_improve_subgoal(subgoal.id)

        except Exception as e:
            print(f"An error occurred while implicitly improving goal: {e}")
            raise e

    def implicitly_improve_subgoal(self, subgoal_id):
        generate_node = GenerateNode()
        try:
            performance_data = self.subgoal_repository.get_performance_data(
                subgoal_id)
            subgoal = self.subgoal_repository.get_sub_goal(subgoal_id)
            workstreams = self.workstream_repository.get_workstreams_by_sub_goal_id(
                subgoal_id)
            unmet_workstreams = []
            for workstream in workstreams:
                workstream_performance = self.workstream_repository.get_performance_data(
                    workstream.id)
                if not is_expectation_met(workstream.kpis,workstream_performance):
                    unmet_workstreams.append(workstream)

            if not unmet_workstreams:
                new_nodes = generate_node.generate_workstreams(
                    subgoal, 2, performance_data)
                new_workstreams = [Workstream.from_dict(new_node) for new_node in new_nodes]
                for new_workstream in new_workstreams:
                    new_workstream.agent_id = subgoal.agent_id
                    new_workstream.goal_id = subgoal.goal_id
                    new_workstream.sub_goal_id = subgoal.id
                    new_workstream.id = uuid.uuid4().hex
                    self.workstream_repository.create_workstream(new_workstream)
            else:
                for workstream in unmet_workstreams:
                    self.implicitly_improve_workstream(workstream.id)

        except Exception as e:
            print(f"An error occurred while implicitly improving subgoal: {e}")
            raise e

    def implicitly_improve_workstream(self, workstream_id):
        improve_node = ImproveNode()
        try:
            workstream = self.workstream_repository.get_workstream(
                workstream_id)
            performance_data = self.workstream_repository.get_performance_data(
                workstream_id)
            feedback = "The workstream is not meeting the expectations"

            new_node = improve_node.improve_node(workstream, feedback,
                                                 workstream_schema)
            improved_workstream = Workstream.from_dict(new_node)
            improved_workstream.agent_id = workstream.agent_id
            improved_workstream.goal_id = workstream.goal_id
            improved_workstream.sub_goal_id = workstream.sub_goal_id
            improved_workstream.id = workstream.id
            print("previous:" )
            print(workstream.to_dict())
            print("improved:")
            print(improved_workstream.to_dict())
            self.workstream_repository.update_workstream(improved_workstream)

        except Exception as e:
            print(
                f"An error occurred while implicitly improving workstream: {e}"
            )
            raise e

class TeammateFeedbackUsecase:

    def __init__(self, agent_repository: AgentRepository,
                 goal_repository: GoalRepository,
                 subgoal_repository: SubGoalRepository,
                 workstream_repository: WorkstreamRepository):
        self.agent_repository = agent_repository
        self.goal_repository = goal_repository
        self.subgoal_repository = subgoal_repository
        self.workstream_repository = workstream_repository

    def analyze_teammate_performance(self, agent_id, team_mate_id):
        agent = self.agent_repository.get_agent(agent_id)
        team_mate = self.agent_repository.get_agent(team_mate_id)

        analyzed_feedback = generate_teammate_feedback(agent, team_mate)

        user_feedback_usecase = UserFeedbackUseCase(self.agent_repository,
                                                    self.goal_repository,
                                                    self.subgoal_repository,
                                                    self.workstream_repository)
        user_feedback_usecase.add_feedback_to_agent(analyzed_feedback,
                                                    agent_id)
        user_feedback_usecase.update_nodes_based_on_feedback(
            analyzed_feedback, agent_id)