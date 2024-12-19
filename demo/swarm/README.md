# Swarm agent

This example is a travel planning agent demonstrating the usage of AnyActions in OpenAI's Swarm framework. The agent has tools to search for flights and get Wikipedia information about scenic places.

## Setup

To run the weather agent Swarm:

1. Environment variables

```shell
export OPENAI_API_KEY=sk-...
```

2. Install Swarm

Requires Python 3.10+

```shell
pip install git+ssh://git@github.com/openai/swarm.git
```

or

```shell
pip install git+https://github.com/openai/swarm.git
```

2. Run

```shell
python3 run.py
```

## Evals

> [!NOTE]
> These evals are intended to be examples to demonstrate functionality, but will have to be updated and catered to your particular use case.

This example uses `Pytest` to run eval unit tests. We have two tests in the `evals.py` file, one which
tests if we call the `find_flight` function when expected, and one which assesses if we properly do NOT call the
`find_flight` function when we shouldn't have a tool call.

To run the evals, run

```shell
pytest evals.py
```

## Credits

This example is adjusted from the [Swarm](https://github.com/jxnl/swarm) project.
