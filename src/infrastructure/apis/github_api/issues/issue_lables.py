from typing import Optional, List, Any
from enum import Enum
from ..base import GitHubAPIBase


class IssueLabelsAPI(GitHubAPIBase):
    """
    Class to interact with GitHub's Issue Labels API.
    """

    def list_labels_for_issue(self, owner: str, repo: str, issue_number: int) -> Any:
        """
        List labels for an issue.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - issue_number (int): The number that identifies the issue. (Required)

        Returns:
        - JSON response containing the list of labels for the issue.
        """
        endpoint = f"/repos/{owner}/{repo}/issues/{issue_number}/labels"
        headers = {"Accept": "application/vnd.github+json"}
        return self._get(endpoint, headers=headers)

    def add_labels_to_issue(self, owner: str, repo: str, issue_number: int, labels: List[str]) -> Any:
        """
        Add labels to an issue.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - issue_number (int): The number that identifies the issue. (Required)
        - labels (List[str]): The names of the labels to add. (Required)

        Returns:
        - JSON response containing the added labels.
        """
        endpoint = f"/repos/{owner}/{repo}/issues/{issue_number}/labels"
        headers = {"Accept": "application/vnd.github+json"}
        data = {"labels": labels}
        return self._post(endpoint, headers=headers, json=data)

    def set_labels_for_issue(self, owner: str, repo: str, issue_number: int, labels: List[str]) -> Any:
        """
        Set labels for an issue. This replaces all existing labels.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - issue_number (int): The number that identifies the issue. (Required)
        - labels (List[str]): The names of the labels to set. (Required)

        Returns:
        - JSON response containing the set labels.
        """
        endpoint = f"/repos/{owner}/{repo}/issues/{issue_number}/labels"
        headers = {"Accept": "application/vnd.github+json"}
        data = {"labels": labels}
        return self._put(endpoint, headers=headers, json=data)

    def remove_all_labels_from_issue(self, owner: str, repo: str, issue_number: int) -> Any:
        """
        Remove all labels from an issue.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - issue_number (int): The number that identifies the issue. (Required)

        Returns:
        - HTTP response status code 204 indicating successful removal.
        """
        endpoint = f"/repos/{owner}/{repo}/issues/{issue_number}/labels"
        headers = {"Accept": "application/vnd.github+json"}
        return self._delete(endpoint, headers=headers)

    def remove_label_from_issue(self, owner: str, repo: str, issue_number: int, name: str) -> Any:
        """
        Remove a label from an issue.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - issue_number (int): The number that identifies the issue. (Required)
        - name (str): The name of the label to remove. (Required)

        Returns:
        - HTTP response status code 204 indicating successful removal.
        """
        endpoint = f"/repos/{owner}/{repo}/issues/{issue_number}/labels/{name}"
        headers = {"Accept": "application/vnd.github+json"}
        return self._delete(endpoint, headers=headers)

    def list_labels_for_repo(self, owner: str, repo: str) -> Any:
        """
        List labels for a repository.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)

        Returns:
        - JSON response containing the list of labels for the repository.
        """
        endpoint = f"/repos/{owner}/{repo}/labels"
        headers = {"Accept": "application/vnd.github+json"}
        return self._get(endpoint, headers=headers)

    def create_label(self, owner: str, repo: str, name: str, color: str, description: Optional[str] = None) -> Any:
        """
        Create a label.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - name (str): The name of the label. (Required)
        - color (str): The color of the label. (Required)
        - description (str): A short description of the label. (Optional)

        Returns:
        - JSON response containing the created label.
        """
        endpoint = f"/repos/{owner}/{repo}/labels"
        headers = {"Accept": "application/vnd.github+json"}
        data = {
            "name": name,
            "color": color,
            "description": description
        }
        return self._post(endpoint, headers=headers, json=data)

    def get_label(self, owner: str, repo: str, name: str) -> Any:
        """
        Get a label.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - name (str): The name of the label. (Required)

        Returns:
        - JSON response containing the label.
        """
        endpoint = f"/repos/{owner}/{repo}/labels/{name}"
        headers = {"Accept": "application/vnd.github+json"}
        return self._get(endpoint, headers=headers)

    def update_label(self, owner: str, repo: str, name: str, new_name: Optional[str] = None, color: Optional[str] = None, description: Optional[str] = None) -> Any:
        """
        Update a label.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - name (str): The name of the label. (Required)
        - new_name (str): The new name of the label. (Optional)
        - color (str): The new color of the label. (Optional)
        - description (str): The new description of the label. (Optional)

        Returns:
        - JSON response containing the updated label.
        """
        endpoint = f"/repos/{owner}/{repo}/labels/{name}"
        headers = {"Accept": "application/vnd.github+json"}
        data = {
            "new_name": new_name,
            "color": color,
            "description": description
        }
        return self._patch(endpoint, headers=headers, json=data)

    def delete_label(self, owner: str, repo: str, name: str) -> Any:
        """
        Delete a label.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - name (str): The name of the label. (Required)

        Returns:
        - HTTP response status code 204 indicating successful deletion.
        """
        endpoint = f"/repos/{owner}/{repo}/labels/{name}"
        headers = {"Accept": "application/vnd.github+json"}
        return self._delete(endpoint, headers=headers)

    def list_labels_for_issues_in_milestone(self, owner: str, repo: str, milestone_number: int) -> Any:
        """
        List labels for issues in a milestone.

        Parameters:
        - owner (str): The account owner of the repository. (Required)
        - repo (str): The name of the repository without the .git extension. (Required)
        - milestone_number (int): The number that identifies the milestone. (Required)

        Returns:
        - JSON response containing the list of labels for issues in the milestone.
        """
        endpoint = f"/repos/{owner}/{repo}/milestones/{milestone_number}/labels"
        headers = {"Accept": "application/vnd.github+json"}
        return self._get(endpoint, headers=headers)
