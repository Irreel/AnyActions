from swarm import Swarm
from agents import weather_agent
import pytest

client = Swarm()


def run_and_get_tool_calls(agent, query):
    message = {"role": "user", "content": query}
    response = client.run(
        agent=agent,
        messages=[message],
        execute_tools=False,
    )
    return response.messages[-1].get("tool_calls")


@pytest.mark.parametrize(
    "query",
    [
        "Find me a flight from New York to London.",
        "Show available flights to Paris.",
        "I need to book a flight to Tokyo.",
    ],
)
def test_calls_flight_when_asked(query):
    tool_calls = run_and_get_tool_calls(weather_agent, query)

    assert len(tool_calls) == 1
    assert tool_calls[0]["function"]["name"] == "find_flight"


@pytest.mark.parametrize(
    "query",
    [
        "What's the weather like today?",
        "What is the time right now?",
        "Hi!",
    ],
)
def test_does_not_call_weather_when_not_asked(query):
    tool_calls = run_and_get_tool_calls(weather_agent, query)

    assert not tool_calls
