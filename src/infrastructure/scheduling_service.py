import re
import json
from google.cloud import scheduler_v1

class SchedulingService:
    def __init__(self, project_id: str, location: str):
        self.project_id = project_id
        self.location = location
        self.client = scheduler_v1.CloudSchedulerClient()

    def schedule_http_job(self, job_name: str, uri: str, http_method:str,  body: dict, frequency: str,description: str = 'No Description', time_zone: str = "America/Los_Angeles"):
        schedule = {
            "daily": "0 0 * * *",
            "weekly": "0 0 * * 0",
            "monthly": "0 0 1 * *",
            "quarterly": "0 0 1 */3 *",
            "yearly": "0 0 1 1 *",
        }

        job_name = sanitize_string(job_name)

        job = {
            'name': f'projects/{self.project_id}/locations/{self.location}/jobs/{job_name}',
            'description': description ,
            'schedule': schedule[frequency],  # Example: Run every day at midnight
            'time_zone': time_zone,
            'attempt_deadline': {'seconds': 60},  # Example: Timeout after 60 seconds
            'retry_config': {'retry_count': 3},  # Example: Retry up to 3 times
            'http_target': {
                'http_method': http_method,
                'uri': uri,
                'body': json.dumps(body).encode('utf-8'),
                'headers': {
                    'Content-Type': 'application/json',
                    # Add any other necessary headers
                },
            },
        }

        try:
            # 3. Create the Job
            response = self.client.create_job(parent=f'projects/{self.project_id}/locations/{self.location}', job=job)
            print(f'Created job: {response.name}')
        except Exception as e:
            print(f'An error occurred: {e}')



def sanitize_string(input_str):
    # Keep only allowed characters: letters, digits, underscores, and hyphens
    sanitized = re.sub(r'[^a-zA-Z\d_-]', '', input_str)
    
    # Trim the string to be at most 500 characters
    return sanitized[:500] if len(sanitized) > 500 else sanitized
