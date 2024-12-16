from typing import List, Dict

class Report:
    def __init__(self, title: str, summary: Dict[str, int], actions: List[Dict[str, int]]):
        """
        Initialize the Report object.
        
        :param title: Title of the report.
        :param summary: Dictionary containing summary data (e.g., completed, pending, total tasks).
        :param actions: List of actions and their respective counts.
        """
        self.title = title
        self.summary = summary
        self.actions = actions

    def to_dict(self) -> Dict:
        """
        Convert the report object to a dictionary format.
        Useful for serialization (e.g., publishing to Pub/Sub).
        """
        return {
            "title": self.title,
            "content": {
                "summary": self.summary,
                "actions": self.actions,
            },
        }

    def __str__(self):
        """
        String representation of the report.
        """
        return f"Report(title={self.title}, summary={self.summary}, actions={self.actions})"
