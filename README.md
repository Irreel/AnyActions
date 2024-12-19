# AnyActions: Developing Your AI Agents with Seamless Tool Integration

> Tool usage empowers your LLM agents to interact with external applications via RESTful APIs calls. They are usually either used to do data retrieval (e.g. search a flight schedule) or take action in another application (e.g. file a JIRA ticket).

AnyActions helps you build LLM agents with external tools (web search, check calendar, etc) and manage tool usage authentication easier and faster. 

```python
from anyactions import ActionHub
hub = ActionHub()

# Set up your tool real quick
tools = hub.tools(["serpapi_google_search"])

# Call LLMs
response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What is the weather in Tokyo next week?"}],
    tools=tools,
)
```

### Features
- Manage tool usage context, authentication, and invocation for LLMs
- Search and plug in available tools from our public database easily
- **Request AnyActions agent to generate tool usage context and tool functions for you!**

## Setup
`python >= 3.10`

For the SDK set up, see [AnyActions-SDK/README.md](AnyActions-SDK/README.md)

## Core Design

ActionHub
- The main component that manages tool usage, orchestrates the tool authentication and invocation process
- Manage authentication for tool usage: Create, Read, Update, and Delete (CRUD). Currently, only API keys are supported. More authentication methods will be supported in the future.
- Manage tool usage context for LLMs, like input schema.

Retriever
- Retrieve available tools from AnyActions database
- For unavailable tools, request our AnyActions agent to generate tool usage context and tool functions for you

Actor
- Parse LLM responses for tool usage
- One-to-one client for executing tool functions based on parsed LLM responses

##### Notes
We named with the term `action` based on the [OpenAI convention](https://platform.openai.com/docs/actions/introduction). In Anthropic's documentation, it is equivalent to `tool`. However, we realized that OpenAI also conflates the term `tool` with `action`. They are the same concept in our SDK.

## Acknowledgements
- [Swarm](https://github.com/openai/swarm)