from collections import Counter
from typing import cast

from jira import JIRA
from jira.client import ResultList
from jira.resources import Issue

# Some Authentication Methods
jira = JIRA(
    server='https://dalek.mot.com/', options={'verify': True}, basic_auth=("johnrf", "Etcfcsgo1.6$mot"))

# Who has authenticated
myself = jira.myself()

# Find all issues reported by the admin
# Note: we cast() for mypy's benefit, as search_issues can also return the raw json !
#   This is if the following argument is used: `json_result=True`
issue = jira.issue("PACE-2677", fields='summary, labels')

print(issue)


