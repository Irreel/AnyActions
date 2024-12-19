
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

# print(response)

tool_result = hub.act(response)

# print(str(response.choices[0].message.tool_calls[0]))

response_2 = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "I want to book a flight from New York to Tokyo on Jan 6th 2025. Can you help me find a flight?"},
        {"role": "user", "content": "Tool usage result\n" + str(response.choices[0].message.tool_calls[0]) + str(tool_result)},
        {"role": "user", "content": "Consider the local weather and the flight time, recommend one best option for me."}
        ],
    tools=hub.tools(["serpapi_google_flights_search", "tomorrow_io_get_weather_forecast"])
)

print(response_2)

tool_result_2 = hub.act(response_2)

final_response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "I want to book a flight from New York to Tokyo on Jan 6th 2025. Can you help me find a flight?"},
        {"role": "user", "content": "Tool usage result\n" + str(response.choices[0].message.tool_calls[0]) + str(tool_result)},
        {"role": "user", "content": "Consider the local weather and the flight time, recommend one best option for me."},
        {"role": "user", "content": "Tool usage result\n" + str(response_2.choices[0].message.tool_calls[0]) + str(tool_result_2)},
        ],
    tools=hub.tools(["serpapi_google_flights_search", "tomorrow_io_get_weather_forecast"])
)

print(final_response)










# ######
# from anyactions import ActionHub
# hub = ActionHub(observer=True)

# tools = hub.tools(["tomorrowio_get_weather_forecast"])
# ######

# response = openai.chat.completions.create(
#     model="gpt-4o",
#     messages=[{"role": "user", "content": ""}],
#     tools=tools,
# )

# print(response)

# action_response = hub.act(response)

# print(action_response)

# result = openai.chat.completions.create(
#     model="gpt-4o",
#     messages=[
#         {"role": "assistant", "content": response["choices"][0]["message"]["content"]},
#         {"role": "user", "content": "What is the weather in Tokyo next week?"},
#     ],
#     tools=tools,
# )
