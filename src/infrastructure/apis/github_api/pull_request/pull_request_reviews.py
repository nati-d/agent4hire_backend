from typing import Any, List, Optional
from ..base import GitHubAPIBase
from enum import Enum

class ReviewEvent(Enum):
    APPROVE = "APPROVE"
    REQUEST_CHANGES = "REQUEST_CHANGES"
    COMMENT = "COMMENT"

class PullRequestReviewsAPI(GitHubAPIBase):
    """
    Class to interact with GitHub's Pull Request Reviews API.
    """

    def list_reviews(self, owner: str, repo: str, pull_number: int) -> Any:
        """
        List reviews for a pull request.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - pull_number (int): The number of the pull request. (Required)

        Returns:
        - JSON response containing the list of reviews.
        """
        endpoint = f"/repos/{owner}/{repo}/pulls/{pull_number}/reviews"
        headers = {"Accept": "application/vnd.github+json"}
        return self._get(endpoint, headers=headers)

    def create_review(self, owner: str, repo: str, pull_number: int, body: str, event: Optional[ReviewEvent] = None, comments: Optional[List[dict]] = None, commit_id: Optional[str] = None) -> Any:
        """
        Create a review for a pull request.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - pull_number (int): The number of the pull request. (Required)
        - body (str): The contents of the review. (Required when using REQUEST_CHANGES or COMMENT)
        - event (Optional[ReviewEvent]): The event to perform. Can be 'APPROVE', 'REQUEST_CHANGES', or 'COMMENT'. Leave blank for PENDING. 
        - comments (List[dict]): An optional list of comments to add to the review. Each comment should contain a 'path', 'position', and 'body'.
        - commit_id (Optional[str]): The SHA of the commit that needs a review. Defaults to the most recent commit if not specified.

        Returns:
        - JSON response containing the created review.
        """
        endpoint = f"/repos/{owner}/{repo}/pulls/{pull_number}/reviews"
        headers = {"Accept": "application/vnd.github+json"}
        data = {"body": body if event in [ReviewEvent.REQUEST_CHANGES, ReviewEvent.COMMENT] else "", "event": event.value if event else "", "comments": comments or []}
        if commit_id:
            data["commit_id"] = commit_id
        return self._post(endpoint, headers=headers, json=data)

    def get_review(self, owner: str, repo: str, pull_number: int, review_id: int) -> Any:
        """
        Get a review for a pull request.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - pull_number (int): The number of the pull request. (Required)
        - review_id (int): The unique identifier of the review. (Required)

        Returns:
        - JSON response containing the review.
        """
        endpoint = f"/repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}"
        headers = {"Accept": "application/vnd.github+json"}
        return self._get(endpoint, headers=headers)

    def update_review(self, owner: str, repo: str, pull_number: int, review_id: int, body: str) -> Any:
        """
        Update a review for a pull request.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - pull_number (int): The number of the pull request. (Required)
        - review_id (int): The unique identifier of the review. (Required)
        - body (str): The updated contents of the review. (Required)

        Returns:
        - JSON response containing the updated review.
        """
        endpoint = f"/repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}"
        headers = {"Accept": "application/vnd.github+json"}
        data = {"body": body}
        return self._put(endpoint, headers=headers, json=data)

    def delete_pending_review(self, owner: str, repo: str, pull_number: int, review_id: int) -> Any:
        """
        Delete a pending review for a pull request.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - pull_number (int): The number of the pull request. (Required)
        - review_id (int): The unique identifier of the review. (Required)

        Returns:
        - HTTP response status code indicating successful deletion.
        """
        endpoint = f"/repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}"
        headers = {"Accept": "application/vnd.github+json"}
        return self._delete(endpoint, headers=headers)

    def list_comments(self, owner: str, repo: str, pull_number: int, review_id: int) -> Any:
        """
        List comments for a pull request review.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - pull_number (int): The number of the pull request. (Required)
        - review_id (int): The unique identifier of the review. (Required)

        Returns:
        - JSON response containing the list of comments for the review.
        """
        endpoint = f"/repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}/comments"
        headers = {"Accept": "application/vnd.github+json"}
        return self._get(endpoint, headers=headers)

    def dismiss_review(self, owner: str, repo: str, pull_number: int, review_id: int, message: str) -> Any:
        """
        Dismiss a review for a pull request.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - pull_number (int): The number of the pull request. (Required)
        - review_id (int): The unique identifier of the review. (Required)
        - message (str): The message explaining why the review was dismissed. (Required)

        Returns:
        - JSON response containing the result of the dismissal.
        """
        endpoint = f"/repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}/dismissals"
        headers = {"Accept": "application/vnd.github+json"}
        data = {"message": message}
        return self._put(endpoint, headers=headers, json=data)

    def submit_review(self, owner: str, repo: str, pull_number: int, review_id: int, event: ReviewEvent) -> Any:
        """
        Submit a review for a pull request.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - pull_number (int): The number of the pull request. (Required)
        - review_id (int): The unique identifier of the review. (Required)
        - event (ReviewEvent): The event to perform. Can be 'APPROVE', 'REQUEST_CHANGES', or 'COMMENT'. (Required)

        Returns:
        - JSON response containing the result of the submission.
        """
        endpoint = f"/repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}/events"
        headers = {"Accept": "application/vnd.github+json"}
        data = {"event": event.value}
        return self._put(endpoint, headers=headers, json=data)
