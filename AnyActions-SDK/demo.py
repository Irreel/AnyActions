import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_KEY')

######
from anyactions import ActionHub
hub = ActionHub(observer=True)

# tools = hub.tools(["get_current_time", "get_current_date"])
# tools = hub.tools(["serpapi_google_search"])
tools = hub.tools(["serpapi_google_search_test"])
######

response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Explain what python is based on google search"}],
    tools=tools,
)

action_response = hub.act(response)

print(action_response[:100])

# print(output_schema)