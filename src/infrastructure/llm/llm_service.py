import os
import google.generativeai as genai

class LLMService:
    def __init__(self, model_name: str):
        self.model_name = model_name

    def generate_content(self, system_instruction: str, query: str, response_type: str, response_schema = dict) -> str:
        
        model_config = genai.GenerationConfig(response_mime_type=response_type, response_schema=response_schema )
        model = genai.GenerativeModel(model_name=self.model_name, generation_config=model_config, system_instruction=system_instruction)

        response = model.generate_content(query)
        return response.candidates[0].content.parts[0].text
    
    def generate_content_with_tools(self, query: str, tools) -> str:
        
        model = genai.GenerativeModel(model_name=self.model_name, tools=tools)

        response = model.generate_content(query)
        return response
    
    def chat_bot(self, system_instruction: str, tools: list, history: list):
        model = genai.GenerativeModel(model_name=self.model_name,
                                      system_instruction=system_instruction,
                                      tools=tools)
        chat = model.start_chat(history=history)
        return chat
    
    def decide_next_branch(self, query: str, current_node: dict) -> (str, float):
        """
        Decides the next branch to take based on the provided query and the options in the current node.

        Args:
            query (str): The input query describing the functionality.
            current_node (dict): The current node in the tree, which contains the branches.

        Returns:
            (str, float): The name of the next branch and the confidence score for the choice.
        """
        print("INSIDE THE NEXT BRANCH CHOOOSING ACCEPTED THE QUERY AND THE CURRENT NODE IS", current_node)
        options = list(current_node.keys())
        print("OPTIONS,", options)
        formatted_options = "\n".join([f"- {option}" for option in options])
        print("FORMATEED OPTIONS", formatted_options)
        system_instruction = (
            "You are tasked with choosing the most relevant branch for the given query. "
            "Select one of the provided options and give a confidence score (0 to 1)."
        )
        
        query_with_options = (
            f"Query: {query}\n"
            f"Options:\n{formatted_options}\n"
            "Respond with the best choice and a confidence score."
        )
        
        response = self.generate_content(system_instruction, query_with_options, response_type="text/plain")
        
        response_parts = response.split(", Confidence: ")
        chosen_branch = response_parts[0].replace("Choice: ", "").strip()
        confidence_score = float(response_parts[1].strip())
        return chosen_branch, confidence_score
