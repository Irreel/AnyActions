# AnyActions Project

> Tool usage empowers your LLM agents to interact with external applications via RESTful APIs calls. They are usually either used to do data retrieval (e.g. search a flight schedule) or take action in another application (e.g. file a JIRA ticket).

AnyActions helps you build LLM agents with external tools and manage tool usage authentication easier and faster. 

## Setup
`python >= 3.10`

For the SDK set up, see [AnyActions-SDK/README.md](AnyActions-SDK/README.md)

## Core Design

ActionHub
- Manage local tool functions: Create, Read, Update, and Delete (CRUD)
- Manage authentication for invoking tool functions: Create, Read, Update, and Delete (CRUD). Currently, only API keys are supported. More authentication methods will be supported in the future.
- Parse LLM responses for tool usage

Retriever
- Retrieve available tools from AnyActions database
- Extract tool usage context for LLMs

Actor
- One-to-one client for executing tool functions based on LLM responses

##### Notes
We named with the term `action` based on the [OpenAI convention](https://platform.openai.com/docs/actions/introduction). In Anthropic's documentation, it is equivalent to `tool`. However, we realized that OpenAI also conflates the term `tool` with `action`. They are the same concept in our SDK.

## Acknowledgements
- [Swarm](https://github.com/openai/swarm)