from typing import List, Optional, Any, Dict
from enum import Enum

from ..base import GitHubAPIBase

class PullRequestState(Enum):
    OPEN = "open"
    CLOSED = "closed"
    ALL = "all"

class PullRequestSort(Enum):
    CREATED = "created"
    UPDATED = "updated"
    POPULARITY = "popularity"

class PullRequestSortDirection(Enum):
    ASC = "asc"
    DESC = "desc"

class MergeMethodEnum(Enum):
    MERGE = "merge"
    SQUASH = "squash"
    REBASE = "rebase"

class PullRequestsAPI(GitHubAPIBase):
    """
    Class to interact with GitHub's Pull Requests API.
    """

    def list_pull_requests(
        self,
        owner: str,
        repo: str,
        state: PullRequestState = PullRequestState.OPEN,
        sort: Optional[PullRequestSort] = None,
        direction: Optional[PullRequestSortDirection] = None,
        per_page: Optional[int] = 30,
        page: Optional[int] = 1
    ) -> Any:
        """
        List pull requests for a repository.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - state (PullRequestState): The state of the pull requests to return (open, closed, or all). (Optional)
        - sort (PullRequestSort): The sort order for pull requests (created, updated, or popularity). (Optional)
        - direction (PullRequestSortDirection): The direction of sorting (asc or desc). (Optional)
        - per_page (int): Number of results per page (default is 30). (Optional)
        - page (int): The page number of the results to return (default is 1). (Optional)

        Returns:
        - JSON response containing the list of pull requests.
        """
        endpoint = f"/repos/{owner}/{repo}/pulls"
        headers = {"Accept": "application/vnd.github+json"}
        params = {
            "state": state.value,
            "per_page": per_page,
            "page": page
        }
        if sort:
            params["sort"] = sort.value
        if direction:
            params["direction"] = direction.value
            
        return self._get(endpoint, headers=headers, params=params)

    def create_pull_request(self, owner: str, repo: str, title: str, head: str, base: str, body: Optional[str] = None) -> Any:
        """
        Create a pull request.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - title (str): The title of the pull request. (Required)
        - head (str): The name of the branch where your changes are implemented. (Required)
        - base (str): The name of the branch you want the changes to be pulled into. (Required)
        - body (str): A description of the pull request. (Optional)

        Returns:
        - JSON response containing the created pull request.
        """
        endpoint = f"/repos/{owner}/{repo}/pulls"
        headers = {"Accept": "application/vnd.github+json"}
        data = {
            "title": title,
            "head": head,
            "base": base,
            "body": body
        }
        return self._post(endpoint, headers=headers, json=data)

    def get_pull_request(self, owner: str, repo: str, pull_number: int) -> Any:
        """
        Get a pull request.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - pull_number (int): The number that identifies the pull request. (Required)

        Returns:
        - JSON response containing the pull request details.
        """
        endpoint = f"/repos/{owner}/{repo}/pulls/{pull_number}"
        headers = {"Accept": "application/vnd.github+json"}
        return self._get(endpoint, headers=headers)

    def update_pull_request(
        self,
        owner: str,
        repo: str,
        pull_number: int,
        title: Optional[str] = None,
        body: Optional[str] = None,
        state: Optional[PullRequestState] = None
    ) -> Any:
        """
        Update a pull request.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - pull_number (int): The number that identifies the pull request. (Required)
        - title (str): The title of the pull request. (Optional)
        - body (str): A description of the pull request. (Optional)
        - state (PullRequestState): The state of the pull request (open or closed). (Optional)

        Returns:
        - JSON response containing the updated pull request.
        """
        endpoint = f"/repos/{owner}/{repo}/pulls/{pull_number}"
        headers = {"Accept": "application/vnd.github+json"}
        data = {}
        if title is not None:
            data["title"] = title
        if body is not None:
            data["body"] = body
        if state is not None:
            data["state"] = state.value
            
        return self._patch(endpoint, headers=headers, json=data)

    def list_commits_on_pull_request(self, owner: str, repo: str, pull_number: int) -> Any:
        """
        List commits on a pull request.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - pull_number (int): The number that identifies the pull request. (Required)

        Returns:
        - JSON response containing the list of commits on the pull request.
        """
        endpoint = f"/repos/{owner}/{repo}/pulls/{pull_number}/commits"
        headers = {"Accept": "application/vnd.github+json"}
        return self._get(endpoint, headers=headers)

    def list_pull_request_files(self, owner: str, repo: str, pull_number: int) -> Any:
        """
        List files in a pull request.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - pull_number (int): The number that identifies the pull request. (Required)

        Returns:
        - JSON response containing the list of files in the pull request.
        """
        endpoint = f"/repos/{owner}/{repo}/pulls/{pull_number}/files"
        headers = {"Accept": "application/vnd.github+json"}
        return self._get(endpoint, headers=headers)

    def check_if_merged(self, owner: str, repo: str, pull_number: int) -> Any:
        """
        Check if a pull request has been merged.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - pull_number (int): The number that identifies the pull request. (Required)

        Returns:
        - JSON response indicating whether the pull request has been merged.
        """
        endpoint = f"/repos/{owner}/{repo}/pulls/{pull_number}/merge"
        headers = {"Accept": "application/vnd.github+json"}
        return self._get(endpoint, headers=headers)

    def merge_pull_request(
        self,
        owner: str,
        repo: str,
        pull_number: int,
        commit_title: Optional[str] = None,
        commit_message: Optional[str] = None,
        sha: Optional[str] = None,
        merge_method: Optional[MergeMethodEnum] = MergeMethodEnum.MERGE
    ) -> Any:
        """
        Merge a pull request.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - pull_number (int): The number that identifies the pull request. (Required)
        - commit_title (str): Title for the automatic commit message. (Optional)
        - commit_message (str): Extra detail to append to automatic commit message. (Optional)
        - sha (str): SHA that pull request head must match to allow merge. (Optional)
        - merge_method (str): The merge method to use (merge, squash, or rebase). (Optional)

        Returns:
        - JSON response containing the result of the merge.
        """
        endpoint = f"/repos/{owner}/{repo}/pulls/{pull_number}/merge"
        headers = {"Accept": "application/vnd.github+json"}
        data = {
            "commit_title": commit_title,
            "commit_message": commit_message,
            "sha": sha,
            "merge_method": merge_method.value if merge_method else None
        }
        return self._put(endpoint, headers=headers, json=data)

    def update_pull_request_branch(self, owner: str, repo: str, pull_number: int) -> Any:
        """
        Update the branch of a pull request.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - pull_number (int): The number that identifies the pull request. (Required)

        Returns:
        - JSON response indicating the result of the update.
        """
        endpoint = f"/repos/{owner}/{repo}/pulls/{pull_number}/update-branch"
        headers = {"Accept": "application/vnd.github+json"}
        return self._post(endpoint, headers=headers)
