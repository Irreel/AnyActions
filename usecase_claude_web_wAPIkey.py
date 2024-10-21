import os
import anthropic
from dotenv import load_dotenv

load_dotenv()
claude_api_key = os.getenv('CLAUDE_KEY')
client = anthropic.Anthropic(api_key=claude_api_key)

from AAPI import aapi

actionsHub = aapi.Hub(api_key="")
tools = actionsHub.tools("google_search")

## Call llm
llm_response = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=1024,
    tools = tools, # return tool definition
    messages=[{"role": "user", "content": "Explain what python is according to wikipedia"}],
)

# Print the console response
print(llm_response.content)

response, output_schema = actionsHub.act(llm_response) # A more intuitive way to coding here is to pass tools definition in

print(response)

print(output_schema)