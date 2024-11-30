"""_summary_
This is a temporary database mockup just for demo

db is formatted as 
db = {
    "PROVIDER_NAME":
    {
        "ACTION_NAME":{
            "author": "AnyActions",
            "provider": "atlassian",
            "description": "Search for Jira dashboards. Returns a paginated list of dashboards. This operation can be accessed anonymously.",
            "documentation": "https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-dashboards/#api-rest-api-3-dashboard-search-get",
            "request": "GET",
            "endpoint": "https://{user_domain}.atlassian.net/rest/api/3/dashboard/search",
            "endpoint_params": {"param_name": "link / instruction to set up this param"},
        }
    }
}

"""

# import pydantic
import json
from pathlib import Path
db_index = ["GOOGLE_SEARCH", "WIKIPEDIA_SEARCH", "JIRA_SEARCH_DASHBOARD"]

tool_name_to_index = {
    # tool_name is how LLM called these tools in their response
    # index helps us to find the tool in the db. Can be updated if data schema changes
    "google_search": "GOOGLE_SEARCH",
    "wikipedia_search": "WIKIPEDIA_SEARCH",
    "jira_search_dashboard": "JIRA_SEARCH_DASHBOARD"
}

CURRENT_DIR = Path(__file__).parent
db = json.load(open(CURRENT_DIR / "db_tmp.json"))