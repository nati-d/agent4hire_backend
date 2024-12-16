from typing import Any, Optional
from ..base import GitHubAPIBase


class PullRequestReviewCommentsAPI(GitHubAPIBase):
    """
    Class to interact with GitHub's Pull Request Review Comments API.
    """

    def list_review_comments_in_repository(
        self,
        owner: str,
        repo: str,
        per_page: Optional[int] = 30,
        page: Optional[int] = 1,
        sort: Optional[str] = None,  # New parameter
        direction: Optional[str] = None,  # New parameter
        since: Optional[str] = None  # New parameter
    ) -> Any:
        """
        List review comments in a repository.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - per_page (int): Number of results per page (default is 30). (Optional)
        - page (int): The page number of the results to return (default is 1). (Optional)
        - sort (str): Sort order for the results. (Optional)
        - direction (str): Direction of the sort. (Optional)
        - since (str): The timestamp to filter results since. (Optional)

        Returns:
        - JSON response containing the list of review comments.
        """
        endpoint = f"/repos/{owner}/{repo}/pulls/comments"
        headers = {"Accept": "application/vnd.github+json"}
        params = {
            "per_page": per_page,
            "page": page,
            "sort": sort,  # Include sort in params
            "direction": direction,  # Include direction in params
            "since": since  # Include since in params
        }
        return self._get(endpoint, headers=headers, params=params)

    def get_review_comment(
        self,
        owner: str,
        repo: str,
        comment_id: int
    ) -> Any:
        """
        Get a review comment for a pull request.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - comment_id (int): The ID of the review comment. (Required)

        Returns:
        - JSON response containing the review comment details.
        """
        endpoint = f"/repos/{owner}/{repo}/pulls/comments/{comment_id}"
        headers = {"Accept": "application/vnd.github+json"}
        return self._get(endpoint, headers=headers)

    def update_review_comment(
        self,
        owner: str,
        repo: str,
        comment_id: int,
        body: str
    ) -> Any:
        """
        Update a review comment for a pull request.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - comment_id (int): The ID of the review comment. (Required)
        - body (str): The updated body of the comment. (Required)

        Returns:
        - JSON response containing the updated review comment.
        """
        endpoint = f"/repos/{owner}/{repo}/pulls/comments/{comment_id}"
        headers = {"Accept": "application/vnd.github+json"}
        data = {"body": body}
        return self._patch(endpoint, headers=headers, json=data)

    def delete_review_comment(
        self,
        owner: str,
        repo: str,
        comment_id: int
    ) -> Any:
        """
        Delete a review comment for a pull request.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - comment_id (int): The ID of the review comment. (Required)

        Returns:
        - JSON response indicating the result of the deletion.
        """
        endpoint = f"/repos/{owner}/{repo}/pulls/comments/{comment_id}"
        headers = {"Accept": "application/vnd.github+json"}
        return self._delete(endpoint, headers=headers)

    def list_review_comments_on_pull_request(
        self,
        owner: str,
        repo: str,
        pull_number: int,
        per_page: Optional[int] = 30,
        page: Optional[int] = 1,
        sort: Optional[str] = None,  # New parameter
        direction: Optional[str] = None,  # New parameter
        since: Optional[str] = None  # New parameter
    ) -> Any:
        """
        List review comments on a specific pull request.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - pull_number (int): The number of the pull request. (Required)
        - per_page (int): Number of results per page (default is 30). (Optional)
        - page (int): The page number of the results to return (default is 1). (Optional)
        - sort (str): Sort order for the results. (Optional)
        - direction (str): Direction of the sort. (Optional)
        - since (str): The timestamp to filter results since. (Optional)

        Returns:
        - JSON response containing the list of review comments for the pull request.
        """
        endpoint = f"/repos/{owner}/{repo}/pulls/{pull_number}/comments"
        headers = {"Accept": "application/vnd.github+json"}
        params = {
            "per_page": per_page,
            "page": page,
            "sort": sort,  # Include sort in params
            "direction": direction,  # Include direction in params
            "since": since  # Include since in params
        }
        return self._get(endpoint, headers=headers, params=params)

    def create_review_comment(
        self,
        owner: str,
        repo: str,
        pull_number: int,
        body: str,
        path: str,
        position: int,
        line: Optional[int] = None
    ) -> Any:
        """
        Create a review comment for a pull request.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - pull_number (int): The number of the pull request. (Required)
        - body (str): The body of the comment. (Required)
        - path (str): The relative path to the file that the comment pertains to. (Required)
        - position (int): The position in the diff to comment on. (Required)
        - line (int): The line number to comment on. (Optional)

        Returns:
        - JSON response containing the created review comment.
        """
        endpoint = f"/repos/{owner}/{repo}/pulls/{pull_number}/comments"
        headers = {"Accept": "application/vnd.github+json"}
        data = {
            "body": body,
            "path": path,
            "position": position,
            "line": line
        }
        return self._post(endpoint, headers=headers, json=data)

    def create_reply_for_review_comment(
        self,
        owner: str,
        repo: str,
        comment_id: int,
        body: str
    ) -> Any:
        """
        Create a reply for a review comment.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - comment_id (int): The ID of the review comment to reply to. (Required)
        - body (str): The body of the reply. (Required)

        Returns:
        - JSON response containing the created reply for the review comment.
        """
        endpoint = f"/repos/{owner}/{repo}/pulls/comments/{comment_id}/replies"
        headers = {"Accept": "application/vnd.github+json"}
        data = {"body": body}
        return self._post(endpoint, headers=headers, json=data)
