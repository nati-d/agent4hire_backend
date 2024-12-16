# from dotenv import load_dotenv

from .branches import Branches
from .collaborators.collaborators import RepositoryCollaborator
from .collaborators.repository_invitation import RepositoryInvitation
from .issues.issue_lables import IssueLabelsAPI
from .issues.issues import Issues
from .issues.issues_assignee import IssueAssignees
from .issues.issues_comment import IssueCommentsAPI
from .pull_request.pull_request_review_requests import PullRequestReviewRequestsAPI
from .pull_request.pull_request_reviews import PullRequestReviewsAPI
from .pull_request.pull_requests import PullRequestsAPI
from .pull_request.pull_request_review_comment import PullRequestReviewCommentsAPI

from .search import GithubSearch
from .metrics import Metrics


import os

# Load environment variables from .env file, we can remove this when we are running this fully on flask
# load_dotenv()

class GitHubAPIIntializer:
    def __init__(self):
        self.token = os.getenv("GITHUB_API_token") # we should use current_app to get this in the future
        
        # collaborators
        self.collaborators = RepositoryCollaborator(self.token)
        self.repository_invitation = RepositoryInvitation(self.token)
        
        # issues
        self.issues = Issues(self.token)
        self.issues_assignees = IssueAssignees(self.token)
        self.issues_lables = IssueLabelsAPI(self.token)
        self.issues_comment = IssueCommentsAPI(self.token)
        
        # pull requests
        self.pull_requests = PullRequestsAPI(self.token)
        self.pull_request_reviews = PullRequestReviewsAPI(self.token)
        self.pull_request_review_comments = PullRequestReviewCommentsAPI(self.token)
        self.pull_request_review_requests = PullRequestReviewRequestsAPI(self.token)
        
        # search
        self.github_search = GithubSearch(self.token)
        
        # branches
        self.branches = Branches(self.token)
        
        # metrics
        self.metrics = Metrics(self.token)
        


GitHubAPI = GitHubAPIIntializer()
