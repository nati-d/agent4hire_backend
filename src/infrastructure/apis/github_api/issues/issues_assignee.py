from typing import Any, Dict, List, Optional
from ..base import GitHubAPIBase


class IssueAssignees(GitHubAPIBase):
    def __init__(self, token: Optional[str] = None):
        super().__init__(token)

    def list_assignees(self, owner: str, repo: str, per_page: int = 30, page: int = 1) -> Dict[str, Any]:
        endpoint = f"repos/{owner}/{repo}/assignees"
        params = {
            "per_page": per_page,
            "page": page
        }
        return self.get(endpoint, params)

    def check_user_can_be_assigned(self, owner: str, repo: str, assignee: str) -> None:
        endpoint = f"repos/{owner}/{repo}/assignees/{assignee}"
        self.get(endpoint)

    def add_assignees_to_issue(self, owner: str, repo: str, issue_number: int, assignees: List[str]) -> Dict[str, Any]:
        endpoint = f"repos/{owner}/{repo}/issues/{issue_number}/assignees"
        data = {
            "assignees": assignees
        }
        return self.post(endpoint, data)

    def remove_assignees_from_issue(self, owner: str, repo: str, issue_number: int, assignees: List[str]) -> Dict[str, Any]:
        endpoint = f"repos/{owner}/{repo}/issues/{issue_number}/assignees"
        data = {
            "assignees": assignees
        }
        return self.delete(endpoint, data)

    def check_user_assigned_to_issue(self, owner: str, repo: str, issue_number: int, assignee: str) -> None:
        endpoint = f"repos/{owner}/{repo}/issues/{issue_number}/assignees/{assignee}"
        self.get(endpoint)