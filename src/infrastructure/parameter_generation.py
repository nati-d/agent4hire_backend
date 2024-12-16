
import json
import os
from typing import Any, Tuple

from fastapi import logger
from flask import session
from infrastructure.embedding_service import UserEmbeddingService
from infrastructure.repositories.self_reflection_repository import SelfReflectionRepository
from infrastructure.api_trees import API_Utils
from infrastructure.llm.open_ai_llm import OpenAiLLMService


api_key= os.getenv("OPENAI_API_KEY")
self_reflection_repository = SelfReflectionRepository()
llm = OpenAiLLMService(model_name="gpt-4o-2024-08-06", api_key=api_key)

class Parameter_Generation:

        
    def extract_user_persona(self):
        try:
            self_reflection_id = "1e0c4082896f4e81a0d5c2748d3edafd"
            # self_reflection_id = session.get('self_reflection_id')
            # if not self_reflection_id:
            #     raise ValueError("self_reflection_id not found in session")
            self_reflection = self_reflection_repository.get_self_reflection(self_reflection_id)
            user_id = self_reflection.user_id
            user_persona = self_reflection.description.get('user_persona', '')
            specific_needs = self_reflection.description.get('specific_needs', [])
            available_apis = self_reflection.available_apis
            goals = [goal.goal for goal in self_reflection.goals] 
            workstreams = [workstream.workstream for workstream in self_reflection.workstreams]  

            combined_info = (
            f"Specific Needs: {', '.join(specific_needs)}. "
            f"Available APIs: {', '.join(available_apis)}. "    
            f"Goals: {', '.join(goals)}. "
            f"Workstreams: {', '.join(workstreams)}."
        )
            return combined_info, user_id
        except Exception as e:
            print(e)
            return "none user description", ""
      
    def get_user_info(self,query, self_reflection_id):
        user_info= UserEmbeddingService()
        data = user_info.retrieve_user_info(query=query, user_id=self_reflection_id )    
        return data
               
    def generate_arguments(self, parameters: list , function: str) -> tuple[bool,dict]:
        user_info, user_id = self.extract_user_persona()
        query = f'Identify any relevant information that correspondece to the user preference, which is {user_info} to call the function {function}'
        user_data = self.get_user_info(query,user_id)
        function_schema= llm.generate_function_schema(function_name=function, parameter_names=parameters)
        arguments = llm.generate_parameters_for_function(function_schema=function_schema, user_persona=user_data)
        final_arguments = {}
        user_prompts = {}
        can_run_function = True
        print("finished argument generation here are the arguments",arguments)
        
        for parameter_name in parameters:
            if parameter_name in arguments:
                if not isinstance(arguments, dict):
                    arguments=json.loads(arguments)
                value = arguments[parameter_name]  
                is_valid, message = self.check_confidence_score(
                persona_context=user_data,
                parameter_name=parameter_name,
                generated_value=value,
                threshold=0.7
            ) 
                print(is_valid, message)
                if is_valid:
                    final_arguments[parameter_name] = value
                else:
                    print(f"Low confidence for parameter '{parameter_name}'. Prompting user for additional input.")
                    user_prompt_message = (
                        f"The parameter '{parameter_name}' requires additional input or credentials to proceed. "
                        f"Please provide the necessary details to continue. "
                    )
                    user_prompts[parameter_name] = user_prompt_message
                    can_run_function = False
            else:

                print(f"Parameter '{parameter_name}' was not generated. Prompting user for additional input.")
                user_prompt_message = (
                    f"The parameter '{parameter_name}' is missing from the generated results. "
                    "Please provide the necessary details to continue."
                )
                user_prompts[parameter_name] = user_prompt_message
                can_run_function = False
        if can_run_function:
            return True, final_arguments
        else:
            return False, user_prompts
    def check_confidence_score(
        self, 
        parameter_name: str, 
        generated_value: Any, 
        persona_context: str, 
        threshold: float = 0.7
    ) -> Tuple[bool, str]:
        """
        Evaluates the confidence score of a generated parameter based on its value, type, and relevance to the context.
        If it does not meet the threshold, provides actionable feedback.

        :param parameter_name: Name of the parameter being evaluated.
        :param generated_value: The generated value for the parameter.
        :param parameter_type: Expected type of the parameter for validation.
        :param persona_context: Context or description of the user persona for relevance evaluation.
        :param threshold: Minimum acceptable confidence score.
        :return: A tuple containing a boolean (True if score meets threshold) and a message.
        """
        prompt = (
            f"Evaluate the relevance, type compatibility, and confidence of the generated parameter accoring to the following information:\n\n"
            f"Parameter Name: {parameter_name}\n"
            f"Generated Value: {generated_value}\n"
            f"User Persona Context: {persona_context}\n\n"
            f"Provide a confidence score between 0 and 1, where 1 is highly relevant. "
            f"If the score is below the threshold of {threshold}, suggest improvements or prompt for additional input."
        )
        
        response_schema = {
                    "type": "json_schema",
                    "json_schema": {
                        "name": f"{parameter_name}_confidence_score",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "confidence_score": {
                                    "type": "number",
                                    "description": "The confidence score for the parameter, between 0 and 1."
                                },
                                "message": {
                                    "type": "string",
                                    "description": "A message explaining the confidence score or suggesting next steps."
                                }
                            },
                            "required": ["confidence_score", "message"],
                            "additionalProperties": False
                        }
                    }
                }
        
        system_instruction = (
            "You are an evaluator analyzing the relevance and accuracy of generated parameter values. "
            "Consider the parameter's name, type, value, and provided user context. "
            "Validate type compatibility and assess its relevance to the persona's needs. "
            "Provide a confidence score between 0 and 1, and if confidence is low, suggest actionable improvements with a generalized message that could be sent to the user."
        )

        try:
            response = llm.generate_content_with_json_format(
                system_instruction=system_instruction,
                query=prompt,
                response_schema=response_schema
            )

            response_data = json.loads(response)
            score = float(response_data["confidence_score"])
            message = response_data["message"]

            # Ensure score is clamped within [0, 1]
            score = max(0.0, min(1.0, score))

            if score < threshold:
                return False, f"Confidence score ({score}) is below threshold: {message}"
            else:
                return True, f"Confidence score ({score}) meets the threshold: {message}"

        except json.JSONDecodeError as e:
            print("Failed to parse JSON response from LLM:", e)
            return False, f"Error in evaluating confidence for '{parameter_name}': Invalid JSON response."
        except KeyError as e:
            print("Missing key in response from LLM:", e)
            return False, f"Error in evaluating confidence for '{parameter_name}': Missing expected keys."
        except Exception as e:
            print(f"Unexpected error during confidence evaluation: {e}")
            return False, f"Error in evaluating confidence for '{parameter_name}': {str(e)}"