from typing import Any, Dict, List, Optional
from enum import Enum

from .base import GitHubAPIBase


# Define Enums for sorting options
class CodeSort(Enum):
    INDEXED = "indexed"
    REPOSITORIES = "repositories"
    STARS = "stars"
    FORKS = "forks"
    UPDATED = "updated"
    CREATED = "created"

class CommitSort(Enum):
    AUTHOR_DATE = "author-date"
    COMMITTER_DATE = "committer-date"

class IssueSort(Enum):
    CREATED = "created"
    UPDATED = "updated"
    COMMENTS = "comments"

class LabelSort(Enum):
    NAME = "name"
    UPDATED = "updated"

class RepoSort(Enum):
    STARS = "stars"
    FORKS = "forks"
    UPDATED = "updated"
    BEST_MATCH = "best match"

class UserSort(Enum):
    FOLLOWERS = "followers"
    REPOSITORIES = "repositories"
    JOINED = "joined"


class GithubSearch(GitHubAPIBase):
    """
    Class to interact with GitHub's Search API.
    """

    def search_code(
        self,
        q: str,
        sort: Optional[CodeSort] = None,  # Updated to use Enum
        order: Optional[str] = None,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
        **kwargs: Dict[str, Any]
    ) -> Any:
        """
        Search for code in repositories.

        Parameters:
        - q (str): The search terms, including optional qualifiers (required).
        - sort (str): Sort results by: `indexed`, `repositories`, `stars`, `forks`, `updated`, `created` (optional).
        - order (str): The order of the results: `asc` or `desc` (optional).
        - per_page (int): Results per page (default is 30, max is 100) (optional).
        - page (int): Page number of the results to fetch (optional).

        Returns:
        - JSON response containing the search results for code.
        """
        endpoint = "/search/code"
        params = {
            "q": q,
            "sort": sort.value if sort else None,  # Use Enum value
            "order": order,
            "per_page": per_page,
            "page": page,
            **kwargs
        }
        return self._get(endpoint, params=params)

    def search_commits(
        self,
        q: str,
        sort: Optional[CommitSort] = None,  # Updated to use Enum
        order: Optional[str] = None,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
        **kwargs: Dict[str, Any]
    ) -> Any:
        """
        Search for commits.

        Parameters:
        - q (str): The search terms, including optional qualifiers (required).
        - sort (str): Sort results by: `author-date`, `committer-date` (optional).
        - order (str): The order of the results: `asc` or `desc` (optional).
        - per_page (int): Results per page (default is 30, max is 100) (optional).
        - page (int): Page number of the results to fetch (optional).

        Returns:
        - JSON response containing the search results for commits.
        """
        endpoint = "/search/commits"
        params = {
            "q": q,
            "sort": sort.value if sort else None,  # Use Enum value
            "order": order,
            "per_page": per_page,
            "page": page,
            **kwargs
        }
        headers = {"Accept": "application/vnd.github.cloak-preview"}
        return self._get(endpoint, headers=headers, params=params)

    def search_issues_and_pull_requests(
        self,
        q: str,
        sort: Optional[IssueSort] = None,  # Updated to use Enum
        order: Optional[str] = None,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
        **kwargs: Dict[str, Any]
    ) -> Any:
        """
        Search for issues and pull requests.

        Parameters:
        - q (str): The search terms, including optional qualifiers (required).
        - sort (str): Sort results by: `created`, `updated`, `comments` (optional).
        - order (str): The order of the results: `asc` or `desc` (optional).
        - per_page (int): Results per page (default is 30, max is 100) (optional).
        - page (int): Page number of the results to fetch (optional).

        Returns:
        - JSON response containing the search results for issues and pull requests.
        """
        endpoint = "/search/issues"
        params = {
            "q": q,
            "sort": sort.value if sort else None,  # Use Enum value
            "order": order,
            "per_page": per_page,
            "page": page,
            **kwargs
        }
        return self._get(endpoint, params=params)

    def search_labels(
        self,
        q: str,
        sort: Optional[LabelSort] = None,  # Updated to use Enum
        order: Optional[str] = None,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
        **kwargs: Dict[str, Any]
    ) -> Any:
        """
        Search for labels.

        Parameters:
        - q (str): The search terms, including optional qualifiers (required).
        - sort (str): Sort results by: `name`, `updated` (optional).
        - order (str): The order of the results: `asc` or `desc` (optional).
        - per_page (int): Results per page (default is 30, max is 100) (optional).
        - page (int): Page number of the results to fetch (optional).

        Returns:
        - JSON response containing the search results for labels.
        """
        endpoint = "/search/labels"
        params = {
            "q": q,
            "sort": sort.value if sort else None,  # Use Enum value
            "order": order,
            "per_page": per_page,
            "page": page,
            **kwargs
        }
        return self._get(endpoint, params=params)

    def search_repositories(
        self,
        q: str,
        sort: Optional[RepoSort] = None,  # Updated to use Enum
        order: Optional[str] = None,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
        **kwargs: Dict[str, Any]
    ) -> Any:
        """
        Search for repositories.

        Parameters:
        - q (str): The search terms, including optional qualifiers (required).
        - sort (str): Sort results by: `stars`, `forks`, `updated`, `best match` (optional).
        - order (str): The order of the results: `asc` or `desc` (optional).
        - per_page (int): Results per page (default is 30, max is 100) (optional).
        - page (int): Page number of the results to fetch (optional).

        Returns:
        - JSON response containing the search results for repositories.
        """
        endpoint = "/search/repositories"
        params = {
            "q": q,
            "sort": sort.value if sort else None,  # Use Enum value
            "order": order,
            "per_page": per_page,
            "page": page,
            **kwargs
        }
        return self._get(endpoint, params=params)

    def search_topics(
        self,
        q: str,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
        **kwargs: Dict[str, Any]
    ) -> Any:
        """
        Search for topics.

        Parameters:
        - q (str): The search terms, including optional qualifiers (required).
        - per_page (int): Results per page (default is 30, max is 100) (optional).
        - page (int): Page number of the results to fetch (optional).

        Returns:
        - JSON response containing the search results for topics.
        """
        endpoint = "/search/topics"
        params = {
            "q": q,
            "per_page": per_page,
            "page": page,
            **kwargs
        }
        return self._get(endpoint, params=params)

    def search_users(
        self,
        q: str,
        sort: Optional[UserSort] = None,  # Updated to use Enum
        order: Optional[str] = None,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
        **kwargs: Dict[str, Any]
    ) -> Any:
        """
        Search for users.

        Parameters:
        - q (str): The search terms, including optional qualifiers (required).
        - sort (str): Sort results by: `followers`, `repositories`, `joined` (optional).
        - order (str): The order of the results: `asc` or `desc` (optional).
        - per_page (int): Results per page (default is 30, max is 100) (optional).
        - page (int): Page number of the results to fetch (optional).

        Returns:
        - JSON response containing the search results for users.
        """
        endpoint = "/search/users"
        params = {
            "q": q,
            "sort": sort.value if sort else None,  # Use Enum value
            "order": order,
            "per_page": per_page,
            "page": page,
            **kwargs
        }
        return self._get(endpoint, params=params)
