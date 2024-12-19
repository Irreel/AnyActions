

import os
import openai
from dotenv import load_dotenv

load_dotenv()

from anyactions import ActionHub

hub = ActionHub()

response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "I want to book a flight from New York to Tokyo on Jan 6th 2025. Can you help me find a flight?"}],
    tools=hub.tools(["serpapi_google_flights_search"])
)

print(response)

tool_result = hub.act(response)

print(str(tool_result)[100:])





