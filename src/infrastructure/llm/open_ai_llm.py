import json
import os
from typing import Any, Dict, Tuple
import openai
from infrastructure.llm.open_ai_schemas import api_tree_schema


class OpenAiLLMService:

    def __init__(self, model_name: str, api_key):
        self.model_name = model_name
        self.client = openai.OpenAI(api_key=api_key)

    def generate_content_with_Structured_schema(self,
                                     system_instruction: str,
                                     query: str,
                                      response_schema):
        messages = [{
            "role": "system",
            "content": system_instruction
        }, {
            "role": "user",
            "content": query
        }]

        completion = self.client.beta.chat.completions.parse(
            model=self.model_name,
            messages=messages,
            response_format=response_schema)

        return completion.choices[0].message.parsed

    def generate_content_with_json_format(self,
                         system_instruction: str,
                         query: str, response_schema: dict):
        messages = [{
            "role": "system",
            "content": system_instruction
        }, {
            "role": "user",
            "content": query
        }]
        completion = self.client.chat.completions.create(
            model="gpt-4o-2024-08-06", messages=messages, response_format=response_schema)

        return completion.choices[0].message.content
    
    
    def generate_content_with_tools(self, query, tools):
        try:
            
            system_instruction = ""
            messages = [{
                "role": "system",
                "content": system_instruction
            }, {
                "role": "user",
                "content": query
            }]
            
            completion = self.client.chat.completions.create(
                model="gpt-4o-2024-08-06", messages=messages, tools= tools)
            
            
            return completion.choices[0].message.tool_calls[0].function
        
        except Exception as e:
            return None
    
    def decide_next_branch(self, query: str, options: Dict[str, Any]) -> Tuple[str, float, str]:
        """
        Uses the LLM to decide the next branch or endpoint to follow based on the query.
        
        :param query: The user's query describing the functionality.
        :param options: A dictionary of options (e.g., available industries or API methods).
        :return: The selected option and a confidence score.
        """
        prompt = (
             f"Based on the query: '{query}', select the most appropriate option from the list below. "
             f"Consider each option carefully and choose the one that aligns best with the query's context: {list(options.keys())}")
 
        response_schema = api_tree_schema
        system_instruction =system_instruction=(
           "Choose the most appropriate next branch based on the given user input. Ensure the selection is from the "
           "provided list of options only. If the chosen branch is not available in the current industry path, "
           "regenerate and select an alternative step from the list. Never Return an empty reply."
           "Make sure to return the chosen endpoint with the reason for it being chosen and the reasonoing behind why it is assigned the given confidence score")

        try:
            response = self.generate_content_with_json_format(
                system_instruction=system_instruction,
                query=prompt,
                response_schema=response_schema
            )
            response_data = json.loads(response)
            return response_data["chosen_option"], response_data["confidence_score"], response_data["score_reason"]
 
        except json.JSONDecodeError as e:
            print("Failed to parse JSON response inside the next branch decision:", e)
            raise RuntimeError("Invalid JSON response received from LLM.")
        except KeyError as e:
            print("Missing key in response:", e)
            raise RuntimeError("Expected keys not found in the response inside the next branch decision.")

    def decide_endpoint_score(self, query: str, endpoint_name: str) -> bool:
        """
        Uses the LLM to determine the confidence score that the branch_name is relevant to the query.

        :param query: The user's query.
        :param branch_name: The name of the branch to evaluate.
        :return: A confidence score between 0 and 1.
        """
        prompt = (
            f"Evaluate the relevance of the query: '{query}' to the endpoint: '{endpoint_name}'. "
            f"Assign a confidence score between 0 and 1, where 1 indicates high relevance and 0 indicates no relevance."
        )

        response_schema = {
           "type": "json_schema",
           "json_schema": {
               "name" : "confidence_score",
               "schema": {
               "type": "object",
               "properties": {
                   "confidence_score": {
                       "type": "number",
                       "description": "The confidence score for the input."
                   }
               },
               "required": ["confidence_score"],
               "additionalProperties": False
           }
        }
       }
        system_instruction = (
            "Assess the relevance of the provided step to the user's query and return a confidence score between 0 and 1. "
            "The response must be in JSON format and include only the 'confidence_score' key."
        )
        
        print(f"Evaluating step '{query}' for relevance with endpoint {endpoint_name}.")
        try:
            response = self.generate_content_with_json_format(
                system_instruction=system_instruction,
                query=prompt,
                response_schema=response_schema
            )
            response_data = json.loads(response)
            score = float(response_data["confidence_score"])
            score = max(0.0, min(1.0, score))
            if score >= 0.85:
                return True
            else:
                return False
        except json.JSONDecodeError as e:
            print("Failed to parse JSON response:", e)
            raise RuntimeError("Invalid JSON response received from LLM inside the branch scoring.")
        except KeyError as e:
            print("Missing key in response:", e)
            raise RuntimeError("Expected keys not found in the response inside the branch scoring.")
        except ValueError:
            print("Invalid confidence score value.")
            raise RuntimeError("Confidence score is not a valid number inside the branch scoring.")
        
    def generate_parameter_details(self, parameter_name: str, function_name: str) -> dict:
        """
        Generates detailed information for a parameter based on the parameter name, function name, and function description.

        :param parameter_name: The name of the parameter.
        :param function_name: The name of the function the parameter belongs to.
        :param function_description: A description of the function's purpose and operations.
        :return: A dictionary with parameter details: name, type, description, and required status.
        """
        system_instruction = "You are an assistant generating details for a function parameter."
        query = (
            f"This is the inteded function '{function_name}'. "
            f"Please provide details for the parameter '{parameter_name}', including its type type limited to string, integer, boolean, a brief description, "
            "and whether it is required, based on its relevance to the function."
        )

        response_schema = {
            "type": "json_schema",
            "json_schema": {
                "name": f"{parameter_name}_details_schema",
                "schema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "The name of the parameter."},
                        "type": {"type": "string", "description": "Data type of the parameter, e.g., string, integer, boolean."},
                        "description": {"type": "string", "description": "Description of what this parameter represents."},
                        "required": {"type": "boolean", "description": "Indicates if the parameter is required."}
                    },
                    "required": ["name", "type", "description", "required"],
                    "additionalProperties": False
                }
            }
        }

        parameter_details = self.generate_content_with_json_format(system_instruction, query, response_schema)
        
        if isinstance(parameter_details, str):
            parameter_details = json.loads(parameter_details)

        if not isinstance(parameter_details, dict):
            raise ValueError(f"Expected dictionary but got {type(parameter_details).__name__}: {parameter_details}")

        return parameter_details



    def generate_function_schema(self, function_name: str, parameter_names: list):
        """
        Generates a JSON schema for a given function, including descriptions and types for each parameter.

        :param function_name: The name of the function.
        :param parameter_names: A list of parameter names (strings).
        :return: A JSON schema as a dictionary describing the function and its parameters.
        """
        system_instruction = "You are generating a JSON schema for a function."
        query = f"Create a JSON schema for the function '{function_name}' with the following parameters."

        response_schema = {
            "type": "object",
            "properties": {}
        }
        print(parameter_names)
        
        for param_name in parameter_names:
            print(param_name)
            print(type(param_name))
            param_details = self.generate_parameter_details(str(param_name), function_name)
            print("finish param description")
            response_schema["properties"][param_name] = {
                "type": param_details["type"],
                "description": param_details["description"]
            }

        return response_schema

    def validate_parameter_details(parameter_details: dict, parameter_name: str):
        """
        Validates that the parameter details contain the required keys: 'type' and 'description'.

        :param parameter_details: The dictionary containing details for a parameter.
        :param parameter_name: The name of the parameter for error reporting.
        :raises ValueError: If any required key is missing from parameter details.
        """
        required_keys = {"type", "description"}  # Hardcoded required keys
        missing_keys = required_keys - parameter_details.keys()
        if missing_keys:
            raise ValueError(f"Missing expected keys {missing_keys} in parameter details for '{parameter_name}'")

    
        
    def generate_parameters_for_function(self, function_schema: dict, user_persona: str):
        """
        Generates arguments for each parameter in the provided function schema based on the user persona description.

        :param function_schema: The JSON schema of the function with details about each parameter.
        :param user_persona: A description of the user persona to guide parameter generation.
        :return: A dictionary with parameter names as keys and generated argument values.
        """
        system_instruction = (
        "You are an intelligent assistant. Given a user persona and the function parameters schema, "
        "generate appropriate values for each parameter. Use contextual hints in the persona to infer "
        "values accurately, even if they are not explicitly stated."
           )
        
        query = (
            
            f"Based on the following user persona:\n'{user_persona}', "
            
            "please generate suitable values for each parameter in the function schema."
            
            "Provide values that match the type and purpose described for each parameter, using any relevant "
            
            "details from the persona to fill in or infer each parameter’s value."
         )  

        parameters = function_schema.get("properties", {})
        required_params = function_schema.get("required", [])

        response_schema = {
            "type": "json_schema",
            "json_schema": {
                "name": f"{function_schema.get('name', 'default_function')}_arguments_schema",
                "schema": {
                    "type": "object",
                    "properties": {
                        param_name: {
                            "type": param_details.get("type", "string"),
                            "description": param_details.get("description", "")
                        }
                        for param_name, param_details in parameters.items()
                    },
                    "required": required_params,
                    "additionalProperties": False
                }
            }
        }

        generated_arguments = self.generate_content_with_json_format(system_instruction, query, response_schema)

        return generated_arguments

