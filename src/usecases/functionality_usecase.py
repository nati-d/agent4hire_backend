import os
import re
from typing import Any, Dict, List, Tuple
from venv import logger
from xml.dom import ValidationErr
from infrastructure.embedding_service import UserEmbeddingService
from domain.models.executions import ModuleExecution
from infrastructure.repositories.execution_repository import ModuleExecutionRepository
from infrastructure.report_service import ReportGeneration
from infrastructure.api_trees import API_Utils
from infrastructure.parameter_generation import Parameter_Generation
from infrastructure.llm.open_ai_llm import OpenAiLLMService
from infrastructure.llm.open_ai_schemas import ArraySchema, ModulesSchema, StringSchema, step_schema , summary_schema
from domain.models.workstream import Workstream
from infrastructure.llm import llm_step_generation_service as llmGen

from infrastructure import api_mapper
from infrastructure.llm.llm_function_calling_service import LLM_function_calling_service
from infrastructure.llm.llm_service import LLMService
import datetime
import json
from domain.models.module import Module
from typing_extensions import TypedDict

from infrastructure.performance_analyzer import PerformanceAnalyzer

class Steps(TypedDict):
    steps: list[str]

if not os.path.exists('logs'):
    os.makedirs('logs')

llm = OpenAiLLMService(model_name="gpt-4o-2024-08-06",
                       api_key=os.getenv('OPENAI_API_KEY'))

class AgentFunctionalityUsecase:
    
    def log_metrics(self, step, status, error_message=None, execution_time=None):
        print("LOGGING HAS STARTED")
        metrics_entry = {
            "timestamp": str(datetime.datetime.now()),
            "step": step,
            "status": status,
            "error_message": error_message,
            "execution_time": execution_time
        }
        with open('logs/logs.txt', 'a') as log_file:
            log_file.write(json.dumps(metrics_entry, indent=2) + '\n')

    
    def Generate_steps(self, strategy: str, apis: list) -> Dict[str, str]:
        """
        Generate steps for a given strategy, ensuring alignment with available API endpoints.
        
        Args:
            strategy (str): High-level task description for which steps are generated.
            apis (list): List of available API functions to be mapped.
            
        Returns:
            Dict[str, str]: Generated steps mapped to available APIs.
        """
        function_call_service = LLM_function_calling_service()
        generator = llmGen.LLM_step_generation_service()

        functions = generator.Generate_steps(strategy=strategy, apis=apis)
        print("The list of functions has been generated and returned", type(functions), "with length of", len(functions))
        return functions
        

    def regenerate_step_with_context(self, steps: Dict[str, str], step_key: str, error_message: str) -> str:
        print("ENTERED REGENERATION SINCE THE EXECUTION FAILED")

        step_keys = list(steps.keys())
        current_index = step_keys.index(step_key)
        
        previous_steps = {k: steps[k] for k in step_keys[:current_index]}
        subsequent_steps = {k: steps[k] for k in step_keys[current_index + 1:]}

        prompt = (
            "Regenerate a function step based on the following context:\n"
            f"Previous steps: {previous_steps}\n"
            f"Subsequent steps: {subsequent_steps}\n"
            f"Current failing step: {steps[step_key]}\n"
            f"Error encountered: {error_message}\n"
            "Make sure the regenerated step is clear, high-level, and aligns smoothly with the surrounding steps, "
            "focusing on overall objective advancement. Avoid overly detailed technical descriptions but address common issues "
            "such as missing dependencies, type mismatches, and handling of NoneType objects. Ensure compatibility with the "
            "next step and logical consistency with prior steps."
        )

        system_instruction = (
            "You are a software engineer tasked with regenerating a step in a high-level task breakdown. Consider the provided "
            "context, including previous and following steps, and address the error encountered. Ensure that the regenerated step "
            "maintains high-level clarity, logically fits with surrounding steps, and advances the module's central objective. "
            "Address common issues like missing dependencies, type mismatches, and NoneType handling as needed."
        )
        
        try:
            # Assuming step_schema is defined elsewhere in your code as the response format schema
            response_format = step_schema
            response = llm.generate_content_with_json_format(
                system_instruction=system_instruction,
                query=prompt,
                response_schema=response_format
            )
            print("LLM response:", repr(response))  
        
            if isinstance(response, str) and response.strip():
                return response.strip()
            else:
                print("Regenerated response is not a valid string.")
                return steps[step_key]

        except Exception as e:
            print(f"An error occurred during step regeneration: {e}")
            return steps[step_key]


    def Execute_steps(self, steps: Dict[str, str]) -> dict:
        """
        Executes a sequence of steps by calling respective API functions, generates parameters for missing ones, and handles retries for errors.
        It retries the same function with generated parameters first and then regenerates the function up to three times.
        
        :param steps: A dictionary where the keys are step names and values are API names.
        :return: A dictionary containing execution results for all steps.
        """
        logger.info("Execution of the functions has started")
        argument_generator = Parameter_Generation()
        api_calling = api_mapper.API_calling_function()
        utils_functionality = API_Utils()
        generator = llmGen.LLM_step_generation_service()
        steps_execution = []
        user_prompt_data = {}
        max_retries = 3

        for step_name, api_name in steps.items():
            print(f"Executing step: {step_name}")
            retry = 0
            iteration_response = None
            user_arguments = {}
            while retry <= max_retries:
                try:
                    if not isinstance(api_name, str):
                        self.log_metrics(step_name, "failure", f"Invalid type for API in step '{step_name}'")
                        iteration_response = {
                            "endpoint_name": None,
                            "status": "error",
                            "details": {
                                "code": 400,
                                "error_type": "InvalidAPIType",
                                "message": f"Invalid type for API in step '{step_name}': expected str, got {type(api_name)}",
                                "confidence": 1.0
                            },
                            "required_parameters": {}
                        }
                        steps_execution.append({
                            "function": step_name,
                            "iteration_response": iteration_response
                        })
                        break

                    selected_endpoint, required_parameters, confidence_score, score_reason = utils_functionality.select_endpoint(api_name=api_name, query=step_name)              
                    if confidence_score < 0.85:
                        for regen_attempt in range(max_retries):
                            new_step = generator.re_generate_step(
                                step_name=step_name,
                                selected_endpoint=selected_endpoint.__name__,
                                score_reason=score_reason
                            )
                            print(f"Regenerated step {regen_attempt + 1}: {new_step}")
                            check = llm.decide_endpoint_score(query=new_step, endpoint_name=selected_endpoint.__name__)
                            if check:
                                step_name = new_step
                                confidence_score = 0.85  
                                break
                        else:
                            print(f"Failed to achieve sufficient confidence score after {max_retries} attempts for step '{step_name}'.")
                            self.log_metrics(step_name, "failure", "Low confidence score after retries.")
                            iteration_response = {
                                "endpoint_name": selected_endpoint.__name__,
                                "status": "error",
                                "details": {
                                    "code": 400,
                                    "error_type": "LowConfidenceScore",
                                    "message": f"Failed to execute attempts for step '{step_name}' since the confidence is low to our .",
                                    "confidence": confidence_score
                                },
                                "required_parameters": {}
                            }
                            steps_execution.append({
                                "function": step_name,
                                "iteration_response": iteration_response
                            })
                            break
                    if required_parameters:
                        missing_parameters = [p for p in required_parameters if p not in user_arguments]
                    else:
                        missing_parameters = []

                    if missing_parameters:
                        can_run, generated_arguments = argument_generator.generate_arguments(function=selected_endpoint, parameters=missing_parameters)
                        if not can_run:
                            print(f"Parameter generation failed for API '{api_name}'. Requesting user input.")
                            user_prompt_data[api_name] = generated_arguments
                            self.log_metrics(step_name, "failure", f"Missing user input for API '{api_name}'.")
                            iteration_response = {
                                "endpoint_name": selected_endpoint.__name__,
                                "status": "input_required",
                                "details": "Waiting for user input",
                                "required_parameters": missing_parameters,
                                "confidence_score": confidence_score
                            }
                            steps_execution.append({
                                "function": step_name,
                                "iteration_response": iteration_response
                            })
                            break

                        if isinstance(generated_arguments, str):
                            generated_arguments = json.loads(generated_arguments)

                        user_arguments.update(generated_arguments)

                    iteration_response = api_calling.endpoint_calling(
                        selected_endpoint=selected_endpoint,
                        user_parameters=user_arguments,
                        confidence_score=confidence_score,
                    )

                    if iteration_response["status"] == "success":
                        self.log_metrics(step_name, "success")
                        steps_execution.append({
                            "function": step_name,
                            "iteration_response": iteration_response
                        })
                        break

                    if iteration_response["status"] == "error":
                        print(f"The function '{step_name}' failed. Attempting to regenerate function.")
                        regenerated_success = False
                        for regen_attempt in range(max_retries):
                            regenerated_step = self.regenerate_step_with_context(steps, step_name, iteration_response["details"])
                            print(f"Regenerated step {regen_attempt + 1}: {regenerated_step}")

                            iteration_response = api_calling.endpoint_calling(
                                selected_endpoint=selected_endpoint,
                                required_parameters=required_parameters,
                                confidence_score=confidence_score
                            )

                            if iteration_response["status"] == "success":
                                self.log_metrics(step_name, "success")
                                steps_execution.append({
                                    "function": step_name,
                                    "iteration_response": iteration_response
                                })
                                regenerated_success = True
                                break
                            
                        if regenerated_success:
                            break

                except Exception as e:
                    self.log_metrics(step_name, "failure", str(e))
                    print(f"Error during '{step_name}': {e}")
                    iteration_response = {
                        "endpoint_name": None,
                        "status": "error",
                        "details": {
                            "code": 500,
                            "error_type": type(e).__name__,
                            "message": f"An unexpected error occurred during step execution: {str(e)}",
                            "confidence": 0.0
                        },
                        "required_parameters": {}
                    }
                    steps_execution.append({
                        "function": step_name,
                        "iteration_response": iteration_response
                    })
                    break

                retry += 1

            logger.info(f"Execution completed for step '{step_name}' with status: {iteration_response['status']}")

        logger.info("Execution of all functions completed.")
        return {
            "steps_execution": steps_execution,
            "user_prompts": user_prompt_data
        }
    def Execute_modules(self, agent_id, modules: List[Module]) -> List[dict]:
        performance_analyzer = PerformanceAnalyzer(LLMService(model_name="gemini-1.5-flash"))
        repository = ModuleExecutionRepository()
        modules_performance = []
        results = []
        print("This is the amount of modules", len(modules))
        print("These are the modules:", modules)

        error_occurred = False
        for idx, module in enumerate(modules):
            print(f"Processing module {idx + 1}/{len(modules)}: {module.module}")
            try:
                steps = self.Generate_steps(module.module, module.apis)
                print(f"Generated steps for module {idx + 1}: {steps}")
            except Exception as e:
                print(f"Step generation failed for module {idx + 1}: {str(e)}")
                modules_performance.append({"module": module.module, "error": f"Step generation failed: {str(e)}"})
                error_occurred = True
                continue

            try:
                result = self.Execute_steps(steps)

                # check if some steps failed to execute
                if any(iteration["iteration_response"]["status"] == "error" for iteration in result["steps_execution"]):
                    error_occurred = True

                print('Module execution result', result)

                module_performance = performance_analyzer.analyze_module_performance(module, result)
                print('kkkkkkkkkkkkkkkkk')
                print(f"Analyzed performance for module {idx + 1}: {module_performance}")
                expectations = [{"expected_value": kpi.expected_value} for kpi in module.kpis]
                metrics = [{"kpi": kpi.kpi} for kpi in module.kpis]
                execution_summary= self.generate_execution_summary(module=module.module,expectations=expectations,metrics=metrics,module_executions=result)
                print("here is the summary of the execution", execution_summary)
                
                execution = ModuleExecution(
                    agent_id=agent_id,
                    execution_time=datetime.utcnow(),
                    result=json.dumps(result),  
                    summary=execution_summary,
                )
                repository.create_execution(execution)
                print("stored on repository")
                modules_performance.append(module_performance)
                results.append({
                    "module": module.module,
                    "steps_execution": result,
                    "performance": module_performance,
                    "execution_summary": execution_summary,
                })
                
            except Exception as e:
                print(f"Step execution failed for module {idx + 1}: {str(e)}")
                error_occurred = True
                modules_performance.append({"module": module.module, "error": f"Step execution failed: {str(e)}"})
                results.append({
                    "module": module.module,
                    "steps_execution": f"Step execution failed: {str(e)}",
                    "performance": "Error on updating the performance.",
                    "execution_summary": execution_summary
                })
                continue

        return {
            "results": results,
        }
    def generate_execution_summary(
        self,
        module: str,
        module_executions: Dict,
        expectations: List[Dict[str,any]],
        metrics: List[Dict[str, any]]
    ) -> str:
        """
        Generate a paragraph-like summary for module executions.
        
        :param module_executions: List of execution details for the modules.
        :param user_requirement: Description of the user's requirements.
        :param expectations: Description of the user's expectations.
        :param metrics: Performance metrics for the executions.
        
        :return: A paragraph-like summary generated by the LLM.
        """
        argument_generator = Parameter_Generation()
        
        try:
            
            query = f"Fetch all relevant information you can get about the user in correspondence to the {module}"
            user_requirement = argument_generator.get_user_info(query=query)
            
            if not expectations:
                expectations = [{"expected_value": "No expectations provided."}]
            if not metrics:
                metrics = [{"kpi": "No metrics provided."}]
            if not module_executions:
                module_executions = [{"module": module, "steps_execution": "No steps executed.", "performance": "No performance data available."}]
                
            formatted_executions = ''.join([
                f"Module: {execution.get('module', 'Unknown')}, "
                f"Steps: {execution.get('steps_execution', 'Not available')}, "
                f"Performance: {execution.get('performance', 'Not available')}\n"
                for execution in module_executions
            ])

            prompt = (
                f"Generate a concise summary based on the following information:\n\n"
                f"User Requirement:\n{user_requirement}\n\n"
                f"Expectations:\n{expectations}\n\n"
                f"Module Executions:\n{formatted_executions}\n\n"
                f"Performance Metrics:\n{json.dumps(metrics, indent=2)}\n\n"
                f"Write a cohesive and professional summary paragraph incorporating all the details provided."
               )
            
            system_instruction = (
            "You are an expert technical writer. Generate a summary that is well-structured, "
            "professional, and concise. Ensure that the summary highlights the key results of "
            "the module executions, aligns with the user's requirements and expectations, "
            "and provides an evaluation of the performance metrics. The tone should be formal "
            "and the information should be organized logically in paragraph format."
            )
            
            response_schema = summary_schema

            summary = llm.generate_content_with_json_format(query=prompt, system_instruction=system_instruction,response_schema=response_schema)
            
            if isinstance(summary, str) and summary.strip():
                return summary.strip()
            return summary

        except Exception as e:
            print(f"Error generating summary: {str(e)}")
            return "An error occurred while generating the summary."
            

class ErrorHandler:
    def __init__(self, llm_service: OpenAiLLMService):
        self.llm_service = llm_service

    def identify_error_type(self, error_message: str) -> str:
        
        error_patterns = {
            "TypeError": r"TypeError",
            "ValueError": r"ValueError",
            "SyntaxError": r"SyntaxError",
            "NoneType": r"NoneType",
            "KeyError": r"KeyError",
            "IndexError": r"IndexError"
        }

        for error_type, pattern in error_patterns.items():
            if re.search(pattern, error_message):
                return error_type
        return "UnknownError"

    def generate_solution(self, steps: List[str], i: int, error_message: str) -> List[str]:
        error_type = self.identify_error_type(error_message)
        print(f"Identified error type: {error_type}")
        prompt = (
            f"Regenerate a solution for the following error:\n"
            f"Error Type: {error_type}\n"
            f"Error Details: {error_message}\n"
            f"Prior Steps: {steps[:i]}\n"
            f"Following Steps: {steps[i + 1:]}\n"
            "Ensure the solution handles dependencies, type safety, and logical flow."
        )

        system_instruction = (
            "You are a software engineer tasked with generating a solution for an identified error. "
            "Use the provided error type and context to create a revised function that resolves the issue."
        )

        try:
            response = self.llm_service.generate_content_with_Structured_schema(
                system_instruction=system_instruction,
                query=prompt,
                response_schema=ArraySchema
            )
            print("Generated response from LLM:", type(response))
            return response.array

        except Exception as e:
            print(f"An error occurred while generating a solution: {e}")
            return []
