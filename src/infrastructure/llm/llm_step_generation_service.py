import json
import os
from infrastructure.llm.llm_service import LLMService
from infrastructure.llm.open_ai_llm import OpenAiLLMService
from typing import List, Dict

llm = OpenAiLLMService("gpt-4o-2024-08-06", api_key=os.getenv('OPENAI_API_KEY'))
class LLM_step_generation_service:
    def Generate_steps(self, strategy: str, apis: List[str]) -> Dict[str, str]:
        """
        Generates high-level steps for a given strategy, with each step as a key and the associated API as its value.

        :param strategy: The central strategy or goal of the module.
        :param apis: A list of available APIs that can be used in the steps.
        :return: A dictionary where each key is a step (function description) and each value is the associated API.
        """
        prompt = f""" Task: {strategy}

        Objective: Break down the task into high-level, actionable steps that drive toward the module's main goal. Each step should align directly with the strategy's purpose, excluding authentication or initial setup steps.

        Requirements:
        1. Return a dictionary with each step as the key and only the associated API as the value.
        2. Exclude extra information such as explanations, numbering, or unrelated details.
        3. The output format should strictly match the following example:
           {{ "step_description": "chosen_api" }}

        Available APIs: {apis}

        Ensure clarity and conciseness in the response, with each step a necessary milestone toward fulfilling the module's objective.
        """
        
        system_instruction = (
            "You are a software engineer tasked with breaking down a module into high-level steps aligned with its central goal. "
            "Return each step as a dictionary entry where the key is a concise description of the step, and the value is the most appropriate API from the list provided. "
            "Strictly avoid adding explanations, numbering, or other information beyond the step and associated API."
        )
        
        steps_schema = {
            "type": "json_schema",
            "json_schema": {
                "name": "steps_schema",
                "schema": {
                    "type": "object",
                    "properties": {
                        "steps": {
                            "type": "object",
                            "additionalProperties": {
                                "type": "string"
                            }
                        }
                    },
                    "required": ["steps"],
                    "additionalProperties": False
                }
            }
        }

        try:
            print("Generating steps with associated API for strategy", strategy, "with available APIs:", apis)
            response = llm.generate_content_with_json_format(
                system_instruction=system_instruction,
                query=prompt,
                response_schema=steps_schema
            )
            
            if response:
                res = json.loads(response)
                steps_dict = res["steps"]
                print(steps_dict)
                return steps_dict
            
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
            print("Raw response that caused the error:", response.text)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        
        return {}  # Return empty dict if any error occurs

    def re_generate_step(self, step_name: str, selected_endpoint,score_reason):
        prompt = f"The function or step named '{step_name}' is being evaluated with the endpoint '{selected_endpoint}'. The confidence score for executing this step with the selected endpoint is {score_reason}. Please adjust the function description to align perfectly with the selected endpoint."
        system_instruction = (
            "Modify the function name to align with the purpose of the selected endpoint while preserving the original function names's high level structure, purpose and word limit."
        )        
        steps_schema = {
            "type": "json_schema",
            "json_schema": {
                "name": "step_schema",
                "schema": {
                    "type": "object",
                    "properties": {
                        "step": {
                            "type": "string",
                            "additionalProperties": {
                                "type": "string"
                            }
                        }
                    },
                    "required": ["step"],
                    "additionalProperties": False
                }
            }
        }
        try:
            response = llm.generate_content_with_json_format(
                system_instruction=system_instruction,
                query=prompt,
                response_schema=steps_schema
            )
            print("check", response)
            response=json.loads(response)
            print(response["step"])
            return response["step"]

        except Exception as e:
            print(f"An unexpected error occurred: {e}")



# from infrastructure.llm.llm_step_generation_service import *  
# llm = LLM_step_generation_service()
# llm.Generate_steps("Integration of Market and Competitor Data", ["crunchbase_api",  "statista_api_call"])