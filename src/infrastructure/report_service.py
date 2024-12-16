import os
import json
from datetime import datetime
from typing import List, Dict
from infrastructure.pub_service import PubSubService
from domain.models.report import Report
from infrastructure.llm.open_ai_llm import OpenAiLLMService


class ReportGeneration:
    def __init__(self):
        self.pubsub_service = PubSubService(project_id="refined-analogy-435508-n3")
        self.llm = OpenAiLLMService(
            model_name="gpt-4o-2024-08-06", api_key=os.getenv("OPENAI_API_KEY")
        )

    def get_executions(self) -> List[Dict]:
        """
        Fetches execution results from a database or placeholder data for testing.
        """
        executions = [
            {
                "steps_execution": [
                    {"function": "Step 1", "iteration_response": {"status": "success"}},
                    {"function": "Step 2", "iteration_response": {"status": "input_required"}}
                ]
            },
            {
                "steps_execution": [
                    {"function": "Step 1", "iteration_response": {"status": "success"}}
                ]
            }
        ]
        print("Fetched executions from database:", executions)
        return executions

    def generate_report(self, executions: List[Dict]) -> Report:
        """
        Generates a report summarizing execution details.
        """
        if not executions:
            raise ValueError("Executions cannot be empty.")

        completed_tasks = len(
            [e for e in executions if all(step.get("iteration_response", {}).get("status") == "success"
                                          for step in e.get("steps_execution", []))]
        )
        pending_tasks = len(
            [e for e in executions if any(step.get("iteration_response", {}).get("status") == "input_required"
                                          for step in e.get("steps_execution", []))]
        )

        summary = {
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "total_tasks": len(executions),
        }

        actions = [
            {"action": "Slack messages", "count": completed_tasks},
            {"action": "Pending inputs required", "count": pending_tasks},
        ]

        report = Report(title="Daily Summary Report", summary=summary, actions=actions)
        print("Generated Report:", report.to_dict())
        return report

    def publish_report(self, report: Report) -> str:
        """
        Publishes the generated report to Pub/Sub.
        """
        topic = "daily-reports"
        response = self.pubsub_service.publish_message(topic, report.to_dict())
        print(f"Published report to Pub/Sub topic '{topic}' with response: {response}")
        return response

    def schedule_report(self):
        """
        Schedules daily report generation and publishing.
        """
        from apscheduler.schedulers.blocking import BlockingScheduler
        from apscheduler.triggers.cron import CronTrigger

        def task():
            try:
                print("Fetching executions...")
                executions = self.get_executions()
                report = self.generate_report(executions)
                self.publish_report(report)
                print("Report task completed successfully.")
            except Exception as e:
                print(f"Error during scheduled report task: {e}")

        scheduler = BlockingScheduler()
        scheduler.add_job(task, CronTrigger(hour=18, minute=0))
        print("Scheduled report generation daily at 6:00 PM.")
        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            print("Scheduler stopped.")
