from ..base import GitHubAPIBase
from ..enums_github import AffiliationEnum, PermissionEnum

from typing import Optional, Dict, Any, List

class RepositoryCollaborator(GitHubAPIBase):
    def list_collaborators(self, owner: str, repo: str, 
                           affiliation: AffiliationEnum = AffiliationEnum.ALL,
                           permission: Optional[PermissionEnum] = None,
                           per_page: int = 30, page: int = 1) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/repos/{owner}/{repo}/collaborators"
        params = {
            'affiliation': affiliation.value,  # Use the value of the Enum
            'permission': permission.value if permission else None,
            'per_page': per_page,
            'page': page
        }
        return self._get(url, params)

    def check_collaborator(self, owner: str, repo: str, username: str) -> Dict[str, Any]:
        url = f"{self.base_url}/repos/{owner}/{repo}/collaborators/{username}"
        return self._get(url)

    def add_collaborator(self, owner: str, repo: str, username: str, 
                         permission: PermissionEnum = PermissionEnum.PUSH) -> Dict[str, Any]:
        url = f"{self.base_url}/repos/{owner}/{repo}/collaborators/{username}"
        data = {'permission': permission.value}  # Use the value of the Enum
        return self._put(url, data)

    def update_collaborator_permission(self, owner: str, repo: str, username: str, 
                                        permission: PermissionEnum) -> Dict[str, Any]:
        return self.add_collaborator(owner, repo, username, permission)

    def remove_collaborator(self, owner: str, repo: str, username: str) -> int:
        url = f"{self.base_url}/repos/{owner}/{repo}/collaborators/{username}"
        return self._delete(url)

    def get_user_permissions(self, owner: str, repo: str, username: str) -> Dict[str, Any]:
        url = f"{self.base_url}/repos/{owner}/{repo}/collaborators/{username}/permission"
        return self._get(url)
