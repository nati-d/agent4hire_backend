# from backend.src.infrastructure.apis.uk_police import UKPoliceClient
import json
import os
from venv import logger
from infrastructure.api_trees import API_Utils, Fetch_Industry_Tree
from infrastructure.llm.open_ai_llm import OpenAiLLMService
import google.generativeai as genai
from infrastructure.llm.llm_service import LLMService
from infrastructure.llm.openai_function_calling import OpenAIFunctionCallingService
from infrastructure.llm.llm_function_calling_service import LLM_function_calling_service
from infrastructure.openai_functions_schema import apis_schema, endpoints_schema
from typing import Any, Dict, List, Optional, Tuple
from infrastructure.api_imports import *

class API_calling_function:
    """
    This class handles calling the API endpoint using the traversal tree's results 
    and an LLM for executing function calls with dynamic parameters.
    """

    def __init__(self):
        self.utils_functionality = API_Utils()
        self.function_call_service = OpenAIFunctionCallingService()

    def endpoint_calling(self, selected_endpoint, confidence_score, user_parameters: Dict[str, Any] = {}, required_parameters: Dict[str, Any] = {}) -> Dict[str, Any]:
        """
        Handles the process of traversing the API tree, calling the endpoint, and managing 
        responses, including missing parameters and errors.

        :param query: The user's query describing the functionality needed.
        :param max_retries: The maximum number of retry attempts.
        :param user_parameters: Parameters provided by the user.
        :param required_parameters: Parameters required by the endpoint.
        :return: A JSON object containing the results of all attempts.
         """
        iteration_response = {
            "endpoint_name": None,
            "status": "",
            "details": "",
            "required_parameters": required_parameters,
            "confidence_score": 0.0
        }
        
        try:
            print("inside the endpoint calling")            
            print("here")
            print("needed paramertrs for it",required_parameters)
            print("the highest confidence score",confidence_score)
            iteration_response["endpoint_name"] = selected_endpoint.__name__
            iteration_response["required_parameters"] = required_parameters
            print(iteration_response["required_parameters"] )
            iteration_response["confidence_score"]= confidence_score
            
            print(f"Attempting to call {selected_endpoint.__name__}")

            if user_parameters == None:
                result = self.function_call_service.call_function(
                    function_call={"name": selected_endpoint.__name__, "arguments": json.dumps(required_parameters)},
                    functions={selected_endpoint.__name__: selected_endpoint}
                )


                if result.get("success") or result.get("data") or result.get("ok") is not True or result.get("error"):
                    error_message = result.get("error", "An unknown error occurred.")
                    iteration_response["status"] = "error"
                    iteration_response["details"] = {
                        "code": 400,
                        "error_type": "APIError",
                        "message": error_message,
                    }
                else:
                    iteration_response["status"] = "success"
                    if not isinstance(result, (dict, list, str, int, float, bool, type(None))):
                        try:
                            result = result.data if hasattr(result, "data") else str(result)
                        except Exception as e:
                            result = f"Non-serializable result: {type(result).__name__}, Error: {str(e)}"
                    result = self.serialize_result(result)  
                    iteration_response["details"] = result
            else :
                print("going to try to call using the generated arguments")
                result = self.function_call_service.call_function(
                    function_call={"name": selected_endpoint.__name__, "arguments": json.dumps(user_parameters)},
                    functions={selected_endpoint.__name__: selected_endpoint}
                )
                print("Result:", result)

                if isinstance(result, dict) and result.get("success") is not True:
                    error_message = result.get("error", "An unknown error occurred.")
                    iteration_response["status"] = "error"
                    iteration_response["details"] = {
                        "code": 400,
                        "error_type": "APIError",
                        "message": error_message,
                    }
                else:
                    iteration_response["status"] = "success"
                    result = self.serialize_result(result)  
                    iteration_response["details"] = result   
        except Exception as e:
            iteration_response["status"] = "error"
            iteration_response["details"] = {
                "code": 500,
                "error_type": type(e).__name__,
                "message": f"An unexpected error occurred while calling the function: {str(e)}"
            }
        return iteration_response
    
    def serialize_result(self,result):
        """Convert non-serializable result objects to a JSON-compatible format."""
        if hasattr(result, "data"):  
            return result.data
        if isinstance(result, (dict, list, str, int, float, bool, type(None))):
            return result
        try:
            return json.loads(json.dumps(result)) 
        except TypeError:
            return str(result) 
    
    

class Functionality_to_API_mapper:
    """
    This class is responsible for mapping the action to the respective API services.
    It selects the appropriate API  to execute based on the action described in the query using 
    function calling through the LLM.
    """
    @staticmethod
    def functionality_to_api_call(query: str):
        """
        Initializes the Generative AI model and handles the function mapping and execution 
        based on the provided query.
        
        :param query: The input query used to determine which API method to call.
        :return: The result of the executed API function.
        """
        try:
            # Initialize the LLM function calling service
            function_call_service = OpenAIFunctionCallingService()
            
            # Get all callable methods from the API_to_endpoint_mapper class (list of functions that initialize an api)
            functions_map = function_call_service.get_function_map(API_to_endpoint_mapper)
            
            # Use the query to execute the corresponding function via LLM
            response , function_name = function_call_service.function_call_for_api(query, apis_schema, functions_map)
            return response,function_name
        
        except AttributeError as ae:
            return function_name
        except KeyError as ke:
            return function_name
        except TypeError as te:
           return function_name
        except Exception as e:
            return function_name
        
    
    @staticmethod
    def endpoint_function_calling(step: str, api: str):
        """
        Initializes the Generative AI model and handles the function mapping and execution 
        based on the provided query.
        
        :param query: The input query used to determine which API method to call.
        :return: The result of the executed API function.
        """
        try:
            print("calling endpointssssssssssssssssssssssss")
            # Initialize the LLM function calling service
            function_call_service = OpenAIFunctionCallingService()
            
            # Get all callable methods from the API_to_endpoint_mapper class (list of functions that initialize an api)
            functions_map = function_call_service.get_function_map(API_to_endpoint_mapper)
            
            # Call the function with the same name as the api
            if api in functions_map:
                endpoint_function = functions_map[api] 
                print("here is the endpoint function", endpoint_function.__name__)
                response = functions_map[api](step)
                return response
            else:
                raise KeyError(f"No API function found for the given api name: {api}")
        
        except AttributeError as ae:
            # Handle cases where the Generative AI model or function mapping goes wrong
            raise AttributeError(f"Error accessing attributes during API call: {str(ae)}")
        except KeyError as ke:
            # Handle incorrect or missing keys for the function call
            return endpoint_function.__name__
        except TypeError as te:
            # Handle issues related to incorrect argument types passed to the function
            raise TypeError(f"Function execution error due to type mismatch: {str(te)}")
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred during the API call: {str(e)}")
        
    
class General_function_calling:
    def general_function_calling(self, service_object: object, query: str):
        """
        Executes a function call on the provided service object based on the input query.
        
        This method initializes the LLM function calling service, retrieves all callable methods 
        from the given service object, and executes the appropriate function based on the query.

        :param service_object: The API service object that contains the callable methods.
        :param query: The input query used to determine which API method to call.
        :return: The result of the executed API function.
        """
        try:
            function_call_service = LLM_function_calling_service()
            functions = function_call_service.get_function_map(service_object)
            response = function_call_service.function_call_for_api(query, functions)
            
            return response
        
        except AttributeError as ae:
            raise AttributeError(f"Error accessing attributes during API call: {str(ae)}")
        except KeyError as ke:
            raise KeyError(f"Function call argument issue: {str(ke)}")
        except TypeError as te:

            raise TypeError(f"Function execution error due to type mismatch: {str(te)}")
        except Exception as e:
            # Catch-all for any other unexpected errors
            raise RuntimeError(f"An unexpected error occurred during the Statista API call: {str(e)}")
    
    def google_services_api_call(query):
        """
        Handles Google Services API calls based on the provided query.
        """


class API_to_endpoint_mapper:
    """
    This class is responsible for mapping the API calls to the respective API services.
    It selects the appropriate API endpoint to execute based on the api description query using 
    function calling through the LLM.
    """


    @staticmethod
    def statista_api_call( query: str):
        """
        Executes a single api call to statista api based on the provided query. The query is expected to be a string and verobsely describe the action to be performed.
        
        :param query: A descriptive string representing the specific request or action to perform 
                      with the Statista API. This query should contain the necessary information 
                      to determine which Statista API method to call and any relevant parameters 
                      (e.g., dataset ID, report type, date range). The function uses this query 
                      to map and execute the appropriate API call dynamically.
        :return: The result of the executed API function.
        """
        try:
            statista = StatistaAPI("aapi_keyyy")
            llm_func_service = OpenAIFunctionCallingService()
            functions_map = llm_func_service.get_function_map(statista)
            response = llm_func_service.function_call_for_api(query, endpoints_schema["statista_api_call"], functions_map)
            return response
        except Exception as e:
            raise e
        
    @staticmethod
    def github_search_api_call( query: str):
        """
        Initializes the GitHub API search and handles the function mapping and execution 
        based on the provided query. The query is expected to be a string that describes 
        the search criteria, such as keywords, repositories, or users.
        
        :param query: A string representing the search criteria for the GitHub API.
        :return: The result of the executed API function.
        """
        try:
            github_api = GitHubAPIIntializer()
            llm_func_service = LLM_function_calling_service()
            functions = llm_func_service.get_function_map(github_api)
            response = llm_func_service.function_call_for_api(query, functions)
            return response
        except Exception as e:
            raise e

    @staticmethod
    def news_api(query: str):
        """Fetches the top headlines from the News API.

        Args:
            query (str): The string search query to filter the headlines.

        Returns:
            dict: A dictionary containing the response or error information.
        """
        try:
            print("inside the news api")
            news = NewsAPIInitializer()
            llm_func_service = OpenAIFunctionCallingService()
            functions_map = llm_func_service.get_function_map(news)
            response = llm_func_service.function_call_for_api(query, endpoints_schema["news_api"], functions_map)
            return {
                "status": "success",
                "response": response
            }
        except Exception as e:
            return {
                "status": "error",
                "error_type": type(e).__name__,
                "message": str(e)
            }


    @staticmethod
    def hunter_email_api(query: str):
        """
        Provides a unified interface to search for email addresses by domain or
        find an email address given a domain and a person's name based on the query string.
        

        :param query: A query string in the format of "domain=<domain>" to search for email addresses
                      associated with a domain, or "domain=<domain>&first_name=<first_name>&last_name=<last_name>"
                      to find a specific email address.
        """
        try:
            hunter = HunterAPI()
            llm_func_service = OpenAIFunctionCallingService()
            functions_map = llm_func_service.get_function_map(hunter)
            response = llm_func_service.function_call_for_api(query, endpoints_schema["hunter_api"], functions_map)
            return response
        except Exception as e:
            raise e
    
    @staticmethod
    def hubspot_api(query: str):
        """Interacts with HubSpot's CRM API to perform operations based on the provided query.

        This method is a part of the HubSpotAPI class, which is designed to facilitate interactions
        with HubSpot's CRM API, enabling the management of contacts and companies.

        Args:
            query (str): A string representing the query to execute against the HubSpot API.
                        This could be a request for contact information, company details, 
                        or any other operation supported by the HubSpot API.
        """
        try:
            hubspot_api = HubSpotAPI()
            llm_func_service = OpenAIFunctionCallingService()
            functions_map = llm_func_service.get_function_map(hubspot_api)
            response = llm_func_service.function_call_for_api(query, endpoints_schema["hubspot_api"], functions_map)
            return response
        except Exception as e:
            raise e
    
    @staticmethod
    def quickbook_api(query: str):
        """
        Interacts with the QuickBooks API to perform operations based on the provided query.

        :param query: A string representing the query to execute against the QuickBooks API.
        :return: The result of the executed API function.
        """
        try:
            quickbook_api = QuickBooksAPI()
            llm_func_service = OpenAIFunctionCallingService()
            functions_map = llm_func_service.get_function_map(quickbook_api)
            response = llm_func_service.function_call_for_api(query, endpoints_schema["quickbook_api"], functions_map)
            return response
        except Exception as e:
            raise e
        
    @staticmethod
    def slack_api(query: str):
        """
        Interacts with the Slack API to perform operations based on the provided query.

        This method is designed to facilitate interactions with the Slack API, enabling
        the sending of messages, retrieving channel information, or performing other
        operations supported by the Slack API.

        Args:
            query (str): A string representing the query to execute against the Slack API.
                         This could include commands for sending messages, fetching user
                         details, or any other operation supported by the Slack API.

        Returns:
            The result of the executed API function, which may vary based on the specific
            operation performed.
        """
        try:
            slack_service = SlackService()
            llm_func_service = OpenAIFunctionCallingService()
            functions_map = llm_func_service.get_function_map(slack_service)
            response = llm_func_service.function_call_for_api(query, endpoints_schema["slack_api"], functions_map)
            return response
        except Exception as e:
            raise e
        
    @staticmethod
    def uk_police_api(query: str):
        "Interacts with the uk polic API to fetch relevant informations as needed"
        
        try:
            uk_police_api = UKPoliceClient()
            return General_function_calling.general_function_calling(uk_police_api, query)
        except Exception as e:
            raise e

    @staticmethod
    def ecb_exchange_rates_api(query: str):
        """
        Interacts with the European Central Bank (ECB) Exchange Rates API to perform operations based on the provided query.

        Args:
            query (str): A string representing the query to execute against the ECB Exchange Rates API.
        """
        try:
            ecb_exchange_rates = ECBExchangeRatesAPI()
            llm_func_service = OpenAIFunctionCallingService()
            functions_map = llm_func_service.get_function_map(ecb_exchange_rates)
            response = llm_func_service.function_call_for_api(query, endpoints_schema["ecb_exchange_rates_api"], functions_map)
            return response
        except Exception as e:
            raise e
        
    @staticmethod
    def guardian_media_api(query: str):
        """
        Interacts with the Guardian Media API to perform operations based on the provided query.

        Args:
            query (str): A string representing the query to execute against the Guardian Media API. This query
                         may include search terms, filters, or other parameters to retrieve specific content. 
        """
        try:
            guardian_media = GuardianNewsAPI()
            llm_func_service = OpenAIFunctionCallingService()
            functions_map = llm_func_service.get_function_map(guardian_media)
            response = llm_func_service.function_call_for_api(query, endpoints_schema["guardian_media_api"], functions_map)
            return response
        except Exception as e:
            raise e
        
    @staticmethod
    def binance_api(query: str):
        """
        Interacts with the Binance API to perform operations based on the provided query.

        Args:
            query (str): A string representing the query to execute against the Binance API.
        """
        try:
            binance = BinanceAPI()
            llm_func_service = OpenAIFunctionCallingService()
            functions_map = llm_func_service.get_function_map(binance)
            response = llm_func_service.function_call_for_api(query, endpoints_schema["binance_api"], functions_map)
            return response
        except Exception as e:
            raise e
        
    @staticmethod
    def cdc_api(query: str):
        """
        Interacts with the Centers for Disease Control and Prevention (CDC) API to perform operations based on the provided query.

        Args:
            query (str): A string representing the query to execute against the CDC API.
        """
        try:
            cdc = CDCAPI()
            llm_func_service = OpenAIFunctionCallingService()
            functions_map = llm_func_service.get_function_map(cdc)
            response = llm_func_service.function_call_for_api(query, endpoints_schema["cdc_api"], functions_map)
            return response
        except Exception as e:
            raise e
        
    @staticmethod
    def free_forex_api(query: str):
        """
        Interacts with the Free Forex API to perform operations based on the provided query.

        Args:
            query (str): A string representing the query to execute against the Free Forex API.
        """
        try:
            free_forex = FreeForexAPI()
            llm_func_service = OpenAIFunctionCallingService()
            functions_map = llm_func_service.get_function_map(free_forex)
            response = llm_func_service.function_call_for_api(query, endpoints_schema["free_forex_api"], functions_map)
            return response
        except Exception as e:
            raise e
        
    @staticmethod
    def health_care_api(query: str):
        """
        Interacts with the HealthCare.gov API to perform operations based on the provided query.

        Args:
            query (str): A string representing the query to execute against the HealthCare.gov API.
        """
        try:
            health_care = HealthCareAPI()
            llm_func_service = OpenAIFunctionCallingService()
            functions_map = llm_func_service.get_function_map(health_care)
            response = llm_func_service.function_call_for_api(query, endpoints_schema["health_care_api"], functions_map)
            return response
        except Exception as e:
            raise e
        
    @staticmethod
    def human_api(query: str):
        """
        Interacts with the Human API to perform operations based on the provided query.

        Args:
            query (str): A string representing the query to execute against the Human API.
        """
        try:
            human = HumanAPI()
            llm_func_service = OpenAIFunctionCallingService()
            functions_map = llm_func_service.get_function_map(human)
            response = llm_func_service.function_call_for_api(query, endpoints_schema["human_api"], functions_map)
            return response
        except Exception as e:
            raise e
        
    @staticmethod
    def open_fda_api(query: str):
        """
        Interacts with the OpenFDA API to perform operations based on the provided query.

        Args:
            query (str): A string representing the query to execute against the OpenFDA API.
        """
        try:
            open_fda = OpenFDAAPI()
            llm_func_service = OpenAIFunctionCallingService()
            functions_map = llm_func_service.get_function_map(open_fda)
            response = llm_func_service.function_call_for_api(query, endpoints_schema["open_fda_api"], functions_map)
            return response
        except Exception as e:
            raise e
        
    # @staticmethod
    # def crunchbase_api(query: str):
    #     """
    #     Interacts with the Crunchbase API to perform operations based on the provided query.

    #     Args:
    #         query (str): A string representing the query to execute against the Crunchbase API.
    #     """
    #     try:
    #         crunchbase_api = CrunchbaseAPI()
    #         llm_func_service = OpenAIFunctionCallingService()
    #         functions_map = llm_func_service.get_function_map(crunchbase_api)
    #         response = llm_func_service.function_call_for_api(query,endpoints_schema["crunchbase_api"], functions_map)
    #         return response
    #     except Exception as e:
    #         raise e
        
    @staticmethod
    def trello_api(query: str):
        """
        Interacts with the Trello API to perform operations based on the provided query.

        This method is designed to facilitate interactions with the Trello API, enabling
        board, list, and card operations.

        Args:
            query (str): A string representing the query to execute against the Trello API.
                        This could include commands for managing boards, lists, and cards.

        Returns:
            The result of the executed API function, which may vary based on the specific
            operation performed.
        """
        try:
            trello_api = TrelloAPI()
            llm_func_service = OpenAIFunctionCallingService()
            functions_map = llm_func_service.get_function_map(trello_api)
            response = llm_func_service.function_call_for_api(query, endpoints_schema["trello_api"], functions_map)
            return response
        except Exception as e:
            raise e

    @staticmethod
    def hackernews_api(query: str):
        """
        Interacts with the Hacker News API to perform operations based on the provided query.

        This method is designed to facilitate interactions with the Hacker News API, enabling
        the fetching of stories, comments, jobs, polls, or user profiles.

        Args:
            query (str): A string representing the query to execute against the Hacker News API.
                        This could include commands for fetching stories, comments, jobs, or user profiles.

        Returns:
            The result of the executed API function, which may vary based on the specific operation performed.
        """
        try:
            hackernews = HackerNewsAPI()
            llm_func_service = OpenAIFunctionCallingService()
            functions_map = llm_func_service.get_function_map(hackernews)
            response = llm_func_service.function_call_for_api(query, endpoints_schema["hackernews_api"], functions_map)
            return response
        
        except Exception as e:
            raise RuntimeError(f"An error occurred while executing the Hacker News API call: {str(e)}")

    @staticmethod
    def crypto_compare_api(query: str) -> Dict[str, Any]:
        """
        Interacts with the CryptoCompare API to perform operations based on the provided query.

        This method is designed to facilitate interactions with the CryptoCompare API, enabling
        the retrieval of cryptocurrency prices, historical data, and other operations supported
        by the CryptoCompare API.

        Args:
            query (str): A string representing the query to execute against the CryptoCompare API.
                        This could include commands for fetching prices, historical data, or
                        any other operation supported by the CryptoCompare API.

        Returns:
            The result of the executed API function, which may vary based on the specific
            operation performed.
        """
        try:
            crypto_compare_api = CryptoCompareAPI()
            llm_func_service = OpenAIFunctionCallingService()
            functions_map = llm_func_service.get_function_map(crypto_compare_api)
            response = llm_func_service.function_call_for_api(query, endpoints_schema["crypto_compare_api"], functions_map)
            return response
        except Exception as e:
            raise e
        

    @staticmethod
    def coinlore_api(query: str) -> Dict[str, Any]:
        """
        Interacts with the Coinlore API to perform operations based on the provided query.

        Args:
            query (str): A string representing the query to execute against the Coinlore API.

        Returns:
            The result of the executed API function, which may vary based on the specific
            operation performed.
        """
        try:
            coinlore = CoinloreAPI()
            llm_func_service = OpenAIFunctionCallingService()
            functions_map = llm_func_service.get_function_map(coinlore)
            response = llm_func_service.function_call_for_api(query, endpoints_schema["coinlore_api"], functions_map)
            return response
        except Exception as e:
            raise e
    
    @staticmethod
    def alpha_vantage_api(query: str) -> Dict[str, Any]:
        """
        Interacts with the Alpha vantage API to perform operations based on the provided query.

        Args:
            query (str): A string representing the query to execute against the Alpha vantage API.

        Returns:
            The result of the executed API function, which may vary based on the specific
            operation performed.
        """
        try:
            alpha_api = AlphaVantageClient()
            llm_func_service = OpenAIFunctionCallingService()
            functions_map = llm_func_service.get_function_map(alpha_api)
            response = llm_func_service.function_call_for_api(query, endpoints_schema["alpha_vantage_api"], functions_map)
            return response
        except Exception as e:
            raise e

    @staticmethod
    def here_api(query: str) -> Dict[str, Any]:
        """
        Interacts with the HERE API to perform operations based on the provided query.

        Args:
            query (str): A string representing the query to execute against the HERE API.

        Returns:
            The result of the executed API function, which may vary based on the specific
            operation performed.
        """
        try:
            here_api = HereAPI()
            llm_func_service = OpenAIFunctionCallingService()
            functions_map = llm_func_service.get_function_map(here_api)
            response = llm_func_service.function_call_for_api(query, endpoints_schema["here_api"], functions_map)
            return response
        except Exception as e:
            raise e

    @staticmethod
    def twitter_api(query: str) -> Dict[str, Any]:
        """
        Interacts with the Twitter API to perform operations based on the provided query.

        Args:
            query (str): A string representing the query to execute against the Twitter API.
        
        Returns:

        """
        try:
            twitter_api = TwitterClient()
            llm_func_service = OpenAIFunctionCallingService()
            functions_map = llm_func_service.get_function_map(twitter_api)
            response = llm_func_service.function_call_for_api(query, endpoints_schema["twitter_api"], functions_map)
            return response
        except Exception as e:
            raise e

    @staticmethod
    def pinterest_api(query: str) -> Dict[str, Any]:
        """
        Interacts with the Pinterest API to perform operations based on the provided query.

        Args:
            query (str): A string representing the query to execute against the Pinterest API.
        """
        try:
            pinterest_api = PinterestClient()
            llm_func_service = OpenAIFunctionCallingService()
            functions_map = llm_func_service.get_function_map(pinterest_api)
            response = llm_func_service.function_call_for_api(query, endpoints_schema["pinterest_api"], functions_map)
            return response
        except Exception as e:
            raise e

    @staticmethod
    def reddit_api(query: str) -> Dict[str, Any]:
        """
        Interacts with the Reddit API to perform operations based on the provided query.

        Args:
            query (str): A string representing the query to execute against the Reddit API.
        """
        try:
            reddit_api = RedditClient()
            llm_func_service = OpenAIFunctionCallingService()
            functions_map = llm_func_service.get_function_map(reddit_api)
            response = llm_func_service.function_call_for_api(query, endpoints_schema["reddit_api"], functions_map)
            return response
        except Exception as e:
            raise e
    
    @staticmethod
    def gnews_api(query: str) -> Dict[str, Any]:
        """
        Interacts with the Google News API to perform operations based on the provided query.

        Args:
            query (str): A string representing the query to execute against the Google News API.
        """
        try:
            gnews_api = GNewsClient()
            llm_func_service = OpenAIFunctionCallingService()
            functions_map = llm_func_service.get_function_map(gnews_api)
            response = llm_func_service.function_call_for_api(query, endpoints_schema["gnews_api"], functions_map)
            return response
        except Exception as e:
            raise e
        
        
# from infrastructure import api_mapper
# step_name,api_name = "retrive news headlines", "news_api"
# iteration_response = api_mapper.Functionality_to_API_mapper().endpoint_function_calling(step_name, api_name)
# print(iteration_response)