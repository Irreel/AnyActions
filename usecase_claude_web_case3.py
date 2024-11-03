import os
import anthropic
from dotenv import load_dotenv

load_dotenv()
claude_api_key = os.getenv('CLAUDE_KEY')
client = anthropic.Anthropic(api_key=claude_api_key)

from AAPI import aapi

actionsHub = aapi.Hub(api_key="")
tools = actionsHub.tools("jira_search_dashboard")

## Call llm
llm_response = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=1024,
    tools = tools, # return tool definition
    messages=[{"role": "user", "content": "What are all the dashboards I have?"}],
)

# Print the console response
print(llm_response.content)

response, output_schema = actionsHub.act(llm_response)

# user_domain for testing: uw-team-aapi

print(response)

print(output_schema)





# import requests
# from requests.auth import HTTPBasicAuth
# import json

# url = "https://uw-team-aapi.atlassian.net/rest/api/3/dashboard/search"

# auth = HTTPBasicAuth("email@example.com", "<api_token>")

# headers = {
#   "Accept": "application/json"
# }

# response = requests.request(
#    "GET",
#    url,
#    headers=headers,
#    auth=auth
# )

# # response = requests.get(endpoint, params=pass_params)

# print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))