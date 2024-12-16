import os
import random
from typing import Any, Dict, List, Tuple
from infrastructure.llm.llm_function_calling_service import LLM_function_calling_service
from infrastructure.llm.open_ai_llm import OpenAiLLMService
from infrastructure.api_imports import *
import inspect

class Fetch_Industry_Tree:
    @staticmethod
    def get_industry_tree() -> dict:
        """
        Generate and return the industry tree structure with mappings from industries to sub-industries and APIs.
        """
        try:
            tree = {
                    "Finance": {
                        "Cryptocurrency": {
                            "Alpha Vantage API": "alpha_vantage_api",
                            "Crypto Compare API": "crypto_compare_api",
                            "Binance API": "binance_api",
                            "Coinlore API": "coinlore_api"
                        },
                        "Forex": {
                            "Free Forex API": "free_forex_api",
                            "ECB Exchange Rates API": "ecb_exchange_rates_api"
                        },
                        "Accounting and Financial Management": {
                            "QuickBooks API": "quickbook_api",
                            "Slack API": "slack_api"
                        }
                    },
                    "Media and News": {
                        "General News": {
                            "News API": "news_api",
                            "GNews API": "gnews_api",
                            "Guardian Media API": "guardian_media_api",
                            "Hacker News API": "hacker_news_api"
                        }
                    },
                    "Social Media and Communication": {
                        "Communication": {
                            "Slack API": "slack_api"
                        },
                        "Social Platforms": {
                            "Twitter API": "twitter_api",
                            "Pinterest API": "pinterest_api",
                            "Reddit API": "reddit_api",
                            "HubSpot API": "hubspot_api"
                        }
                    },
                    "Business and Productivity Tools": {
                        "Project Management": {
                            "Trello API": "trello_api"
                        },
                        "Business Intelligence": {
                            "Crunchbase API": "crunchbase_api",
                            "Statista API": "statista_api_call"
                        },
                        "Development Tools": {
                            "GitHub API": "github_search_api_call",
                            "Google Console API": "google_services_api"
                        }
                    },
                    "Healthcare and Medical Information": {
                        "General Healthcare": {
                            "Health Care API": "health_care_api",
                            "CDC API": "cdc_api",
                            "Human API": "human_api",
                            "Open FDA API": "open_fda_api"
                        }
                    },
                    "Location and Mapping Services": {
                        "Mapping": {
                            "Here API": "here_api"
                        }
                    }
                }

            return tree
        except Exception as e:
            print(f"Error inside get_industry_tree: {e}")
            raise
        
        
class API_Utils:
    @staticmethod
    def get_function_parameters(function: Any) -> List[str]:
        """
        Retrieves the parameters for a given function or endpoint.
        
        :param function: The function whose parameters need to be extracted.
        :return: A list of parameter names.
        """
        try:
            signature = inspect.signature(function)
            parameters = [param.name for param in signature.parameters.values() if param.name != 'self']
            print("here are the list of parameters required", parameters)
            return parameters
        except Exception as e:
            raise RuntimeError(f"Error retrieving parameters for the function: {str(e)}")
        
    def choose_industry_based_on_query(self, query: str, industry_map: Dict[str, Any]) -> Tuple[str, float]:
           """
           Uses the LLM to choose the most relevant industry based on the given query.
           
           :param query: The input query describing the functionality.
           :param industry_map: A dictionary of available industries.
           :return: The chosen industry.
           """
           api_key = os.getenv("OPENAI_API_KEY")
           llm_service = OpenAiLLMService(model_name="gpt-4o-2024-08-06", api_key=api_key)
           chosen_industry, confidence_score, endpoint_score = llm_service.decide_next_branch(query=query, options=industry_map)
           
           return chosen_industry, confidence_score


    def traverse_api_tree(self, query: str) -> Tuple[float, List[str], Any, List[str]]:
        """
        Traverses the industry tree to find the relevant path for an API call based on a query.
        Uses an LLM service to decide the next branch and attempts up to three times for regeneration
        if the confidence score is low.
        :param query: The input query describing the functionality.
        :param industry: The starting industry for the traversal.
        :return: A tuple containing the path taken, the final function (endpoint), and the parameters needed.
        """
        tree_fetch = Fetch_Industry_Tree()
        api_key = os.getenv("OPENAI_API_KEY")
        industry_tree = tree_fetch.get_industry_tree()
        llm_service = OpenAiLLMService(model_name="gpt-4o-2024-08-06", api_key=api_key)
        function_llm = LLM_function_calling_service()

        industry, confidence_score = self.choose_industry_based_on_query(query, industry_tree)
        current_node = industry_tree.get(industry, {})
        path_taken = [industry]

        while isinstance(current_node, dict):
            attempts = 0
            while attempts < 3 and confidence_score < 0.85:
                next_branch, confidence_score, endpoint_score = llm_service.decide_next_branch(query, current_node)
                attempts += 1

                if confidence_score >= 0.85:
                    break

            if next_branch in current_node:
                path_taken.append(next_branch)
                current_node = current_node[next_branch]
            else:
                raise KeyError(f"Branch '{next_branch}' not found in current industry path.")

        if not callable(current_node):
            function_map = function_llm.get_function_map(current_node)
            if function_map:
                final_method_name, confidence_score, endpoint_score = llm_service.decide_next_branch(query, function_map)
                if final_method_name in function_map:
                    final_method = function_map[final_method_name]
                    parameters = self.get_function_parameters(final_method)
                    return confidence_score, path_taken + [final_method_name], final_method, parameters
                else:
                    raise KeyError(f"Method '{final_method_name}' not found in API service.")
            else:
                raise ValueError("The last node is not a valid API service or does not have callable methods.")

        return confidence_score, path_taken, current_node, self.get_function_parameters(current_node)
    
    def multi_traverse_api_tree(self, query: str, threshold: float = 0.6) -> List[str]:
        """
        Traverses multiple paths in the API tree to find relevant APIs for a query.
        Each decision to branch is made based on a confidence score, and all paths with scores
        above the threshold are explored. If no APIs meet the threshold, the top 3 APIs by
        confidence are returned.

        :param query: The input query describing the functionality.
        :param threshold: The minimum confidence score required to continue exploring a path.
        :return: A list of valid API names (strings) that meet the threshold confidence, or
                the top 3 APIs if none meet the threshold.
        """
        tree_fetch = Fetch_Industry_Tree()
        industry_tree = tree_fetch.get_industry_tree()
        llm_service = OpenAiLLMService(model_name="gpt-4", api_key=os.getenv("OPENAI_API_KEY"))
        function_llm = LLM_function_calling_service()

        industry, initial_confidence = self.choose_industry_based_on_query(query, industry_tree)
        initial_node = industry_tree.get(industry, {})
        initial_path = [industry]
        active_paths = [(initial_confidence, initial_path, initial_node)]
        valid_api_names = []
        all_explored_apis = []

        visited_paths = set()

        while active_paths:
            current_confidence, current_path, current_node = active_paths.pop(0)

            path_tuple = tuple(current_path)

            if path_tuple in visited_paths:
                continue
            visited_paths.add(path_tuple)

            if isinstance(current_node, dict):
                for branch_name, branch_node in current_node.items():
                    next_branch, branch_confidence, score_reason = llm_service.decide_next_branch(query, {branch_name: branch_node})

                    if next_branch in current_node:
                        new_path = current_path + [next_branch]
                        new_node = current_node[next_branch]
                        active_paths.append((branch_confidence, new_path, new_node))

                        # Track all APIs explored with their confidence
                        if isinstance(new_node, str):
                            all_explored_apis.append((branch_confidence, new_node, score_reason))

            elif isinstance(current_node, str):
                if current_confidence >= threshold:
                    valid_api_names.append(current_node)
                all_explored_apis.append((current_confidence, current_node))

        # If no APIs meet the threshold, return the top 3 by confidence
        if not valid_api_names:
            all_explored_apis.sort(reverse=True, key=lambda x: x[0])  # Sort by confidence, descending
            valid_api_names = [api for confidence, api, *_ in all_explored_apis[:3]]

        return valid_api_names




    def select_highest_confidence_path(self, paths: List[Tuple[float, List[str], Any, List[str]]]) -> Tuple[List[str], Any, List[str], float]:
        """
        Selects the path with the highest confidence score from a list of paths.
        If there are ties in confidence score, randomly selects one of the tied paths.
    
        :param paths: A list of paths, each with a tuple containing:
                      (confidence_score, path_taken, final_method, parameters)
        :return: The selected path as a tuple containing:
                 (path_taken, final_method, parameters)
        """
        if not paths:
            raise ValueError("No paths provided to select from.")
        paths_sorted = sorted(paths, key=lambda x: x[0], reverse=True)
        highest_score = paths_sorted[0][0]
        top_paths = [path for path in paths_sorted if path[0] == highest_score]
    
        if len(top_paths) == 1:
            highest_score, path_taken, final_method, parameters = top_paths[0]
            return path_taken, final_method, parameters, highest_score
        chosen_path = random.choice(top_paths)
        highest_score, path_taken, final_method, parameters = chosen_path
        print(f"Randomly selected path among tied options with score {highest_score}")
        return path_taken, final_method, parameters, highest_score
    
    
    def select_endpoint(self, api_name: str, query: str) -> Tuple[str, List[str], float]:
        
        """
        Selects an endpoint for a given API name based on a query.
        Uses decide_next_branch to choose an endpoint from the function map.
        :param api_name: The name of the API as defined in the tree.
        :param query: A natural language query describing the desired functionality.
        :return: A tuple containing the selected endpoint and its parameters.
        """
        function_llm = LLM_function_calling_service()
        try:
            
            api_tree = get_flat_api_instance_tree()
            api_instance = api_tree.get(api_name)
            if not api_instance:
                raise KeyError(f"API '{api_name}' not found in the API tree.")

            function_map = function_llm.get_function_map(class_instance=api_instance)
            if not function_map:
                raise ValueError(f"No function map available for API '{api_name}'.")

            api_key = os.getenv("OPENAI_API_KEY")
            llm_service = OpenAiLLMService(model_name="gpt-4o-2024-08-06", api_key=api_key)
            selected_endpoint, confidence_score, endpoint_score = llm_service.decide_next_branch(query, function_map)
            print("here is the selected endpoint", selected_endpoint)
            
            if selected_endpoint in function_map:
                 final_method = function_map[selected_endpoint]
            else:
               raise KeyError(f"Selected endpoint '{selected_endpoint}' not found in the function map for API '{api_name}'.")
           
            parameters = self.get_function_parameters(final_method)

            return final_method, parameters , confidence_score, endpoint_score

        except Exception as e:
            print(f"Error in select_endpoint : {e}")
            raise