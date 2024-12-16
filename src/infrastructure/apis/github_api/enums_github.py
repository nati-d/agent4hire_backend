from enum import Enum

# Sorting 
class SortOrder(Enum):
    CREATED = "created"
    UPDATED = "updated"
    COMMENTS = "comments"

class SortDirection(Enum):
    DESC = "desc"
    ASC = "asc"


# Enum for collaborators
class AffiliationEnum(Enum):
    OUTSIDE = "outside"
    DIRECT = "direct"
    ALL = "all"


class PermissionEnum(Enum):
    PULL = "pull"
    TRIAGE = "triage"
    PUSH = "push"
    MAINTAIN = "maintain"
    ADMIN = "admin"
    
    
# Enum for the issues
class IssueState(Enum):
    OPEN = "open"
    CLOSED = "closed"


class StateReasonEnum(Enum):
    COMPLETED = "completed"
    NOT_PLANNED = "not_planned"
    REOPENED = "reopened"
    NULL = None  # Representing null

class LockReason(Enum):
    OFF_TOPIC = "off_topic"
    TOO_HEATED = "too_heated"
    RESOLVED = "resolved"
    SPAM = "spam"

class AssigneeState(Enum):
    OPEN = "open"
    CLOSED = "closed"
    
    
# Pull Request
class PullRequestState(Enum):
    OPEN = "open"
    CLOSED = "closed"
    ALL = "all"

class PullRequestSort(Enum):
    CREATED = "created"
    UPDATED = "updated"
    POPULARITY = "popularity"

class PullRequestSortDirection(Enum):
    ASC = "asc"
    DESC = "desc"