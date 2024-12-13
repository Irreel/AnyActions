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
tools = hub.tools(["tomorrowio_get_weather_forecast"])
######

response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What is the weather in Tokyo next week?"}],
    tools=tools,
)

print(response)

action_response = hub.act(response)

print(action_response)

# print(output_schema)