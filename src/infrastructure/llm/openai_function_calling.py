from infrastructure.llm.open_ai_llm import OpenAiLLMService
import json
import os
class OpenAIFunctionCallingService:
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
        :return: The result of the executed function or an error status and message if the function is not found.
        """
        function_name = function_call.name
        function_args = function_call.arguments
        
        if function_name in functions:
            try:
                # Execute the function and return its response
                response = functions[function_name](**json.loads(function_args))
                return {
                    "status": "success",
                    "response": response
                }
            except Exception as e:
                # Handle any exceptions raised during function execution
                return {
                    "status": "error",
                    "message": f"An error occurred while executing the function: {str(e)}"
                }
        else:
            # Return error if the function is not found in the map
            return {
                "status": "error",
                "message": f"Function '{function_name}' not found in the function map."
            }


    def function_call_for_api(self, query: str, functions_schema, functions_map):
        """
        Generates a response using the Generative AI model based on the query and 
        executes the function if the model returns a function call.

        :param query: The action that needs to be performed.
        :param functions_schema: The schema of functions available to the LLM for tool usage.
        :param functions_map: The dictionary mapping function names to their callable endpoints.
        :return: The result of the executed function if applicable.
        """
        api_key = os.getenv('OPENAI_API_KEY')
        llm_service = OpenAiLLMService(model_name="gpt-4o-2024-08-06", api_key=api_key)
        response = llm_service.generate_content_with_tools(query, functions_schema)
        if response:
            
            result = self.call_function(function_call=response, functions=functions_map)
            return result,response
        else:
            return {
                "error": "No function call returned from the LLM model."
            }

