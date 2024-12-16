from ..base import GitHubAPIBase
from ..enums_github import PermissionEnum
from typing import Optional, Dict, Any, List


class RepositoryInvitation(GitHubAPIBase):
    def list_invitations(self, owner: str, repo: str, 
                         per_page: int = 30, page: int = 1) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/repos/{owner}/{repo}/invitations"
        params = {
            'per_page': per_page,
            'page': page
        }
        headers = {'Accept': 'application/vnd.github+json'}
        return self._get(url, params=params, headers=headers)

    def update_invitation(self, owner: str, repo: str, invitation_id: int, 
                          permission: PermissionEnum) -> Dict[str, Any]:
        url = f"{self.base_url}/repos/{owner}/{repo}/invitations/{invitation_id}"
        data = {'permissions': permission.value}
        headers = {'Accept': 'application/vnd.github+json'}
        return self._patch(url, data=data, headers=headers)

    def delete_invitation(self, owner: str, repo: str, invitation_id: int) -> int:
        url = f"{self.base_url}/repos/{owner}/{repo}/invitations/{invitation_id}"
        headers = {'Accept': 'application/vnd.github+json'}
        return self._delete(url, headers=headers)

    def list_user_invitations(self, per_page: int = 30, page: int = 1) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/user/repository_invitations"
        params = {
            'per_page': per_page,
            'page': page
        }
        headers = {'Accept': 'application/vnd.github+json'}
        return self._get(url, params=params, headers=headers)

    def accept_invitation(self, invitation_id: int) -> Dict[str, Any]:
        url = f"{self.base_url}/user/repository_invitations/{invitation_id}"
        headers = {'Accept': 'application/vnd.github+json'}
        return self._patch(url, headers=headers)

    def decline_invitation(self, invitation_id: int) -> int:
        url = f"{self.base_url}/user/repository_invitations/{invitation_id}"
        headers = {'Accept': 'application/vnd.github+json'}
        return self._delete(url, headers=headers)
