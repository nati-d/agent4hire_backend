# import json
# from typing import List
# from infrastructure.report_service import ReportGeneration
# from domain.models.module import Module
# from functionality_usecase import AgentFunctionalityUsecase
# from infrastructure.pub_service import PubSubService


# class UserQueryFunctionality:
#     def __init__(self):
#         self.functionality = AgentFunctionalityUsecase()
#         self.pubsub_service = PubSubService(project_id="refined-analogy-435508-n3")
#         self.report_generator = ReportGeneration()

#     def user_query(self, result: dict) -> dict:
#         """
#         Processes user query results to extract execution details.
#         """
#         json_payload = {}
#         for module_result in result.get("performance", {}).get("results", []):
#             module_name = module_result.get("module")
#             steps_execution = module_result.get("steps_execution", {}).get("steps_execution", [])
#             user_prompts = module_result.get("steps_execution", {}).get("user_prompts", {})

#             for step in steps_execution:
#                 function_name = step.get("function")
#                 iteration_response = step.get("iteration_response", {})
#                 if iteration_response.get("status") == "input_required":
#                     endpoint_name = iteration_response.get("endpoint_name")
#                     required_parameters = iteration_response.get("required_parameters", [])
#                     api_name = None
#                     for api, params in user_prompts.items():
#                         if any(param in params for param in required_parameters):
#                             api_name = api
#                             break

#                     json_payload = {
#                         "module": module_name,
#                         "function": function_name,
#                         "api_name": api_name,
#                         "endpoint": endpoint_name,
#                         "required_parameters": required_parameters,
#                     }
#             return json_payload

#     def execute_and_store(self, agent_id: str, modules: List[Module]) -> dict:
#         """
#         Executes modules and stores the results.
#         """
#         print("Executing modules:", [module.module for module in modules])
#         execution_result = self.functionality.Execute_modules(agent_id, modules=modules)

#         # Generate and publish report
#         try:
#             report = self.report_generator.generate_report(execution_result)
#             self.report_generator.publish_report(report)
#         except Exception as e:
#             print(f"Error generating or publishing report: {e}")

#         return execution_result
