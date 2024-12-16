import requests
from typing import Optional, Dict, Any, List

class GitHubAPIBase:
    def __init__(self, token: str) -> None:
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint}"  # Generate URL
        if params:
            params = {k: v for k, v in params.items() if v is not None}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def _post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint}"  # Generate URL
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def _put(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        url = f"{self.base_url}/{endpoint}"  # Generate URL
        response = requests.put(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json() if response.content else None

    def _delete(self, endpoint: str) -> int:
        url = f"{self.base_url}/{endpoint}"  # Generate URL
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()
        return response.status_code