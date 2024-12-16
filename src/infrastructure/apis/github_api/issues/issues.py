from typing import Any, Dict, List, Optional
from ..base import GitHubAPIBase
from ..enums_github import IssueState, LockReason, SortDirection, SortOrder, StateReasonEnum


class Issues(GitHubAPIBase):
    def list_issues(
        self,
        owner: str,
        repo: str,
        milestone: Optional[str] = None,
        state: IssueState = IssueState.OPEN,
        assignee: Optional[str] = None,
        creator: Optional[str] = None,
        mentioned: Optional[str] = None,
        labels: Optional[List[str]] = None,
        sort: SortOrder = SortOrder.CREATED,
        direction: SortDirection = SortDirection.DESC,
        since: Optional[str] = None,
        per_page: int = 30,
        page: int = 1
    ) -> List[Dict[str, Any]]:
        endpoint = f"repos/{owner}/{repo}/issues"
        params = {
            "milestone": milestone,
            "state": state.value,  # Use enum value
            "assignee": assignee,
            "creator": creator,
            "mentioned": mentioned,
            "labels": labels,
            "sort": sort.value,  # Use enum value
            "direction": direction,
            "since": since,
            "per_page": per_page,
            "page": page
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.get(endpoint, params)

    def create_issue(
        self,
        owner: str,
        repo: str,
        title: str,
        body: Optional[str] = None,
        assignees: Optional[List[str]] = None,
        milestone: Optional[int] = None,
        labels: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        endpoint = f"repos/{owner}/{repo}/issues"
        data = {
            "title": title,
            "body": body,
            "assignees": assignees,
            "milestone": milestone,
            "labels": labels
        }
        data = {k: v for k, v in data.items() if v is not None}
        return self.post(endpoint, data)

    def get_issue(self, owner: str, repo: str, issue_number: int) -> Dict[str, Any]:
        endpoint = f"repos/{owner}/{repo}/issues/{issue_number}"
        return self.get(endpoint)

    def update_issue(
        self,
        owner: str,
        repo: str,
        issue_number: int,
        title: Optional[str] = None,
        body: Optional[str] = None,
        assignees: Optional[List[str]] = None,
        state: Optional[IssueState] = None,
        state_reason: Optional[StateReasonEnum] = None,
        milestone: Optional[int] = None,
        labels: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        endpoint = f"repos/{owner}/{repo}/issues/{issue_number}"
        data = {
            "title": title,
            "body": body,
            "assignees": assignees,
            "state": state.value if state else None,  # Use enum value if provided
            "state_reason": state_reason.value if state_reason else None,  # Use enum value if provided
            "milestone": milestone,
            "labels": labels
        }
        data = {k: v for k, v in data.items() if v is not None}
        return self.patch(endpoint, data)

    def lock_issue(self, owner: str, repo: str, issue_number: int, lock_reason: Optional[LockReason] = None) -> Dict[str, Any]:
        endpoint = f"repos/{owner}/{repo}/issues/{issue_number}/lock"
        data = {
            "lock_reason": lock_reason.value if lock_reason else None  # Use enum value if provided
        }
        return self.put(endpoint, data)

    def unlock_issue(self, owner: str, repo: str, issue_number: int) -> int:
        endpoint = f"repos/{owner}/{repo}/issues/{issue_number}/lock"
        return self.delete(endpoint)
