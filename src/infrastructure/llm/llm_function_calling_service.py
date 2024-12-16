import google.generativeai as genai

from infrastructure.llm.llm_service import LLMService
from infrastructure.repositories.self_reflection_repository import SelfReflectionRepository
from infrastructure.embedding_service import UserEmbeddingService

from flask import session

self_reflection_repository = SelfReflectionRepository()
user_embedding_service = UserEmbeddingService()

class LLM_function_calling_service:
    """
    A service class for mapping and invoking class methods based on LLM (Language Learning Model)
    function calls. It interacts with Google's Generative AI model to determine and execute 
    the correct method from a class instance based on the model's response.
    """
    
    def get_function_map(self, class_instance):
        """
        Retrieves all callable methods from the class instance, excluding special methods 
        (those starting with '__').
        
        :param class_instance: An instance of the class whose methods are being mapped.
        :return: A dictionary mapping method names to callable methods.
        """
        try:
            methods = {method_name: getattr(class_instance, method_name) 
                       for method_name in dir(class_instance) 
                       if callable(getattr(class_instance, method_name)) and not method_name.startswith("__") and not method_name.startswith("_")}
            return methods
        except Exception as e:
            raise RuntimeError(f"Error retrieving method map: {str(e)}")

    def call_function(self, function_call, functions):
        """
        Executes a function based on the function call object provided by the LLM response.
        
        :param function_call: The function call object from the model's response containing the name and arguments.
        :param functions: A dictionary of function names mapped to their corresponding callable methods.
        :return: The result of the executed function.
        """
        try:
            function_name = function_call.name
            function_args = function_call.args
            # print("function_name and function args", function_name, function_args)
            if function_name in functions:
                return functions[function_name](**function_args)
            else:
                raise ValueError(f"Function '{function_name}' not found in the available functions.")
        except KeyError as ke:
            raise KeyError(f"Error in function arguments: {str(ke)}")
        except TypeError as te:
            raise TypeError(f"Error during function call: {str(te)}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error during function execution: {str(e)}")

    def function_call_for_api(self, query: str, functions):
        """
        Generates a response using the Generative AI model based on the query and 
        executes the function if the model returns a function call.
        
        :param query: the action that needs to be performed.
        :param functions: The list of functions passed to the model for tool usage.
        :return: The result of the executed function if applicable.
        """
        try:
            # print("query:", query)
            # print("funcs:", list(functions.values()))
            # Retrieve self_reflection_id from the session
            self_reflection_id = session.get('self_reflection_id')
            if not self_reflection_id:
                raise ValueError("self_reflection_id not found in session")
            self_reflection = self_reflection_repository.get_self_reflection(self_reflection_id)

            query = f"""
            Give me what you think the user is asking for, and the overall needs of the user. Preferebly in one paragraph.
            """

            user_info = user_embedding_service.retrieve_user_info(query, self_reflection_id)

            print("USER INFO ", user_info)

            # Extract data from SelfReflection
            available_apis = self_reflection.available_apis
            goals = self_reflection.goals
            sub_goals = self_reflection.sub_goals
            workstreams = self_reflection.workstreams

            prompt = f"""
            You are an AI assistant designed to help users with specific tasks.

            User Description: {user_info}
            Available APIs: {', '.join(available_apis)}
            Goals: {', '.join(goals)}
            Sub-Goals: {', '.join(sub_goals)}
            Workstreams: {', '.join(workstreams)}
            
            The user has asked: "{query}"
            
            Based on the above information, please provide a JSON-formatted response that addresses the user's request.
            """

            llm_service = LLMService(model_name="gemini-1.5-flash")
            
            print("\n\n")
            print("here to function call query: ", query)
            print("tools for function call", list(functions.keys()))
            response = llm_service.generate_content_with_tools(query, list(functions.values()))

            # part = response.candidates[0].content.parts[0]

            # Generate content from the model based on the query
            # response = model.generate_content(query)
            # print("Model Response:", response)

            # Extract the first part of the response
            part = response.candidates[0].content.parts[0]
            # If the response contains a function call, execute the corresponding function
            print("\n\n")
            print("function choosed", part.function_call.name)
            if part.function_call:
                result = self.call_function(part.function_call, functions)
                # print("result", result)
                return result
            else:
                return part.text
        
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred: {str(e)}")

    
    def filter_function_map_by_apis(self, function_map: dict, relevant_apis: list) -> dict:
        """
        Filters the function map to only include functions that match the relevant API names.

        :param function_map: A dictionary mapping method names to callable methods.
        :param relevant_apis: A list of relevant API names to filter from the function map.
        :return: A dictionary with the filtered method names and their corresponding callables.
        """
        try:
            filtered_map = {method_name: method 
                            for method_name, method in function_map.items() 
                            if method_name in relevant_apis}
            return filtered_map
        except Exception as e:
            raise RuntimeError(f"Error filtering method map by APIs: {str(e)}")
    
    