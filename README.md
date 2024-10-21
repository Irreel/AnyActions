# AAPI
（正式名字待定）

## Setup
Currently, the library does not have any dependencies, but you need to setup OpenAI or Claude API key in `.env` for running the use cases.

Besides, to run `usecase_claude_web_wAPIkey.py`, you need to setup the API key at SerpAPI website and add it in `aapi/register_api_tmp.py`.

Enable `git lfs` to download the large files in `APIdb`.

## Use Case

### Use case 1
- no need for API key: Wikipedia
`usecase_claude_web_oAPIkey.py`: a use case to demo when 3rd party API calling does not need API key

### Use case 2
- need API key: Google search
`usecase_claude_web_wAPIkey.py`: a use case to demo when 3rd party API calling needs API key
  
### Use case 3 [TODO]
- need API key and some other Auth?: JIRA, Slack


## File Structure

- `AAPI`: the main library
  - `utils.py`: some utility functions
  - `main.py`: the main function to run the library
  - `db_tmp.py`: a *temporary* database mockup just for demo
  - `register_api_tmp.py`: a *temporary* placeholder assume it can register APIs
  - `tests`: do we need unit tests?
  
- `APIdb`: database for the server
  
- `usecases_*`: See [Use Case](#use-case)
  
- `example_*.py`: I use these to inspect different LLM response formats

## Design

Hub class()

- Initializing the API environment: `__init__` Only some placeholders for now
- Managing API keys: `verification()`
- Providing tool description for LLM interactions: `tools()`
- Executing API calls: `act()`

