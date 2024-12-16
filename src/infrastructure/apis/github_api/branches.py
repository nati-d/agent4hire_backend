from typing import Any, Dict, List, Optional
from .base import GitHubAPIBase

class Branches(GitHubAPIBase):
    """
    Class to interact with GitHub's Branches API.
    """

    def list_branches(
        self,
        owner: str,
        repo: str,
        protected: Optional[bool] = None,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
        **kwargs: Dict[str, Any]
    ) -> Any:
        """
        List branches in a repository.

        Parameters:
        - owner (str): The owner of the repository (required).
        - repo (str): The name of the repository (required).
        - protected (bool): If true, only protected branches will be returned (optional).
        - per_page (int): Results per page (default is 30, max is 100) (optional).
        - page (int): Page number of the results to fetch (optional).

        Returns:
        - JSON response containing the list of branches.
        """
        endpoint = f"/repos/{owner}/{repo}/branches"
        params = {
            "protected": protected,
            "per_page": per_page,
            "page": page,
            **kwargs
        }
        return self._get(endpoint, params=params)

    def get_branch(
        self,
        owner: str,
        repo: str,
        branch: str
    ) -> Any:
        """
        Get a specific branch from a repository.

        Parameters:
        - owner (str): The owner of the repository (required).
        - repo (str): The name of the repository (required).
        - branch (str): The name of the branch (required).

        Returns:
        - JSON response containing the branch details.
        """
        endpoint = f"/repos/{owner}/{repo}/branches/{branch}"
        return self._get(endpoint)

    def rename_branch(
        self,
        owner: str,
        repo: str,
        branch: str,
        new_name: str
    ) -> Any:
        """
        Rename a branch in a repository.

        Parameters:
        - owner (str): The owner of the repository (required).
        - repo (str): The name of the repository (required).
        - branch (str): The current name of the branch (required).
        - new_name (str): The new name for the branch (required).

        Returns:
        - JSON response indicating the result of the rename operation.
        """
        endpoint = f"/repos/{owner}/{repo}/branches/{branch}/rename"
        data = {"new_name": new_name}
        return self._post(endpoint, json=data)

    def sync_fork_branch(
        self,
        owner: str,
        repo: str,
        branch: str
    ) -> Any:
        """
        Sync a fork branch with the upstream repository.

        Parameters:
        - owner (str): The owner of the forked repository (required).
        - repo (str): The name of the forked repository (required).
        - branch (str): The name of the branch to sync (required).

        Returns:
        - JSON response indicating the result of the sync operation.
        """
        endpoint = f"/repos/{owner}/{repo}/branches/{branch}/sync"
        return self._post(endpoint)

    def merge_branch(
        self,
        owner: str,
        repo: str,
        base: str,
        head: str,
        commit_message: Optional[str] = None
    ) -> Any:
        """
        Merge a branch into another branch.

        Parameters:
        - owner (str): The owner of the repository (required).
        - repo (str): The name of the repository (required).
        - base (str): The name of the base branch (the branch to merge into) (required).
        - head (str): The name of the head branch (the branch to merge) (required).
        - commit_message (str): A commit message for the merge (optional).

        Returns:
        - JSON response indicating the result of the merge operation.
        """
        endpoint = f"/repos/{owner}/{repo}/merges"
        data = {
            "base": base,
            "head": head,
            "commit_message": commit_message
        }
        return self._post(endpoint, json=data)
