"""_summary_
This is a temporary database mockup just for demo

db is formatted as 
db = {
    "PROVIDER_NAME":
    {
        "ACTION_NAME"
    }
}

"""

# import pydantic
import json
from pathlib import Path
db_index = ["GOOGLE_SEARCH", "WIKIPEDIA_SEARCH", "JIRA_SEARCH_DASHBOARD"]

tool_name_to_index = {
    # tool_name is how LLM called these tools in their response
    "google_search": "GOOGLE_SEARCH",
    "wikipedia_search": "WIKIPEDIA_SEARCH",
    "jira_search_dashboard": "JIRA_SEARCH_DASHBOARD"
}

CURRENT_DIR = Path(__file__).parent
db = json.load(open(CURRENT_DIR / "db_tmp.json"))