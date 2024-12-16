from .base import GitHubAPIBase

class Metrics(GitHubAPIBase):
    def get_repo_stats(self, owner, repo):
        url = f"/repos/{owner}/{repo}/stats/contributors"
        return self._get(url)

    def get_code_frequency(self, owner, repo):
        url = f"/repos/{owner}/{repo}/stats/code_frequency"
        return self._get(url)

    def get_issue_activity(self, owner, repo):
        url = f"/repos/{owner}/{repo}/stats/issue_activity"
        return self._get(url)
