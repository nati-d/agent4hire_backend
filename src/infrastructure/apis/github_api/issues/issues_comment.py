from typing import Optional, Any
from enum import Enum
from ..base import GitHubAPIBase
from ..enums_github import SortDirection, SortOrder

class IssueCommentsAPI(GitHubAPIBase):
    """
    Class to interact with GitHub's Issue Comments API.
    """
    def list_issue_comments_for_repo(
        self, 
        owner: str, 
        repo: str, 
        sort: SortOrder = SortOrder.CREATED, 
        direction: Optional[SortDirection] = None, 
        since: Optional[str] = None, 
        per_page: int = 30, 
        page: int = 1
    ) -> Any:
        """
        List issue comments for a repository.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - sort (SortOrder): The property to sort the results by. Default: created.
        - direction (SortDirection): Either asc or desc. Ignored without the sort parameter.
        - since (str): Only show results that were last updated after the given time. This is a timestamp in ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ.
        - per_page (int): The number of results per page (max 100). Default: 30.
        - page (int): The page number of the results to fetch. Default: 1.

        Returns:
        - JSON response containing the list of issue comments.
        """
        endpoint = f"/repos/{owner}/{repo}/issues/comments"
        headers = {"Accept": "application/vnd.github+json"}
        params = {
            "sort": sort.value,
            "direction": direction.value if direction else None,
            "since": since,
            "per_page": per_page,
            "page": page
        }
        return self._get(endpoint, headers=headers, params=params)

    def get_issue_comment(self, owner: str, repo: str, comment_id: int) -> Any:
        """
        Get an issue comment.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - comment_id (int): The unique identifier of the comment. (Required)

        Returns:
        - JSON response containing the issue comment.
        """
        endpoint = f"/repos/{owner}/{repo}/issues/comments/{comment_id}"
        headers = {"Accept": "application/vnd.github+json"}
        return self._get(endpoint, headers=headers)

    def update_issue_comment(self, owner: str, repo: str, comment_id: int, body: str) -> Any:
        """
        Update an issue comment.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - comment_id (int): The unique identifier of the comment. (Required)
        - body (str): The contents of the comment. (Required)

        Returns:
        - JSON response containing the updated issue comment.
        """
        endpoint = f"/repos/{owner}/{repo}/issues/comments/{comment_id}"
        headers = {"Accept": "application/vnd.github+json"}
        data = {"body": body}
        return self._patch(endpoint, headers=headers, json=data)

    def delete_issue_comment(self, owner: str, repo: str, comment_id: int) -> Any:
        """
        Delete an issue comment.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - comment_id (int): The unique identifier of the comment. (Required)

        Returns:
        - HTTP response status code 204 indicating successful deletion.
        """
        endpoint = f"/repos/{owner}/{repo}/issues/comments/{comment_id}"
        headers = {"Accept": "application/vnd.github+json"}
        return self._delete(endpoint, headers=headers)

    def list_issue_comments(
        self, 
        owner: str, 
        repo: str, 
        issue_number: int, 
        since: Optional[str] = None, 
        per_page: int = 30, 
        page: int = 1
    ) -> Any:
        """
        List issue comments for a specific issue.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - issue_number (int): The number that identifies the issue. (Required)
        - since (str): Only show results that were last updated after the given time. This is a timestamp in ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ.
        - per_page (int): The number of results per page (max 100). Default: 30.
        - page (int): The page number of the results to fetch. Default: 1.

        Returns:
        - JSON response containing the list of issue comments for the specific issue.
        """
        endpoint = f"/repos/{owner}/{repo}/issues/{issue_number}/comments"
        headers = {"Accept": "application/vnd.github+json"}
        params = {
            "since": since,
            "per_page": per_page,
            "page": page
        }
        return self._get(endpoint, headers=headers, params=params)

    def create_issue_comment(
        self, 
        owner: str, 
        repo: str, 
        issue_number: int, 
        body: str
    ) -> Any:
        """
        Create an issue comment.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - issue_number (int): The number that identifies the issue. (Required)
        - body (str): The contents of the comment. (Required)

        Returns:
        - JSON response containing the created issue comment.
        """
        endpoint = f"/repos/{owner}/{repo}/issues/{issue_number}/comments"
        headers = {"Accept": "application/vnd.github+json"}
        data = {"body": body}
        return self._post(endpoint, headers=headers, json=data)
