from typing import Any, List, Optional
from ..base import GitHubAPIBase


class PullRequestReviewRequestsAPI(GitHubAPIBase):
    """
    Class to interact with GitHub's Pull Request Review Requests API.
    """

    def get_all_requested_reviewers(
        self,
        owner: str,
        repo: str,
        pull_number: int,
        per_page: Optional[int] = None,
        page: Optional[int] = None
    ) -> Any:
        """
        Get all requested reviewers for a pull request.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - pull_number (int): The number of the pull request. (Required)
        - per_page (Optional[int]): The number of items to return per page. (Optional)
        - page (Optional[int]): The page number to return. (Optional)

        Returns:
        - JSON response containing the list of requested reviewers.
        """
        endpoint = f"/repos/{owner}/{repo}/pulls/{pull_number}/requested_reviewers"
        headers = {"Accept": "application/vnd.github+json"}
        params = {}
        if per_page is not None:
            params['per_page'] = per_page
        if page is not None:
            params['page'] = page
        return self._get(endpoint, headers=headers, params=params)

    def request_reviewers(
        self,
        owner: str,
        repo: str,
        pull_number: int,
        reviewers: List[str],
        team_reviewers: Optional[List[str]] = None
    ) -> Any:
        """
        Request reviewers for a pull request.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - pull_number (int): The number of the pull request. (Required)
        - reviewers (List[str]): A list of GitHub usernames to request as reviewers. (Required)
        - team_reviewers (Optional[List[str]]): A list of team usernames to request as reviewers. (Optional)

        Returns:
        - JSON response containing the result of the request.
        """
        endpoint = f"/repos/{owner}/{repo}/pulls/{pull_number}/requested_reviewers"
        headers = {"Accept": "application/vnd.github+json"}
        data = {"reviewers": reviewers}
        if team_reviewers is not None:
            data['team_reviewers'] = team_reviewers
        return self._post(endpoint, headers=headers, json=data)

    def remove_requested_reviewers(
        self,
        owner: str,
        repo: str,
        pull_number: int,
        reviewers: List[str],
        team_reviewers: Optional[List[str]] = None
    ) -> Any:
        """
        Remove requested reviewers from a pull request.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - pull_number (int): The number of the pull request. (Required)
        - reviewers (List[str]): A list of GitHub usernames to remove from the requested reviewers. (Required)
        - team_reviewers (Optional[List[str]]): A list of team usernames to remove from the requested reviewers. (Optional)

        Returns:
        - JSON response containing the result of the removal.
        """
        endpoint = f"/repos/{owner}/{repo}/pulls/{pull_number}/requested_reviewers"
        headers = {"Accept": "application/vnd.github+json"}
        data = {"reviewers": reviewers}
        if team_reviewers is not None:
            data['team_reviewers'] = team_reviewers
        return self._delete(endpoint, headers=headers, json=data)
