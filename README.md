# AnyActions
（Just a random name for now）

## Setup
Currently, the library does not have any dependencies, but you need to setup OpenAI or Claude API key in `.env` for running the use cases.

Besides, to run `usecase_claude_web_wAPIkey.py`, you need to setup the API key at SerpAPI website and add it in `aapi/register_api_tmp.py`.

Enable `git lfs` for now


## Use Case

### Use case 1
- no need for API key: Wikipedia
`usecase_claude_web_oAPIkey.py`: a use case to demo when 3rd party API calling does not need API key

### Use case 2
- need API key: Google search
`usecase_claude_web_wAPIkey.py`: a use case to demo when 3rd party API calling needs API key
  
### Use case 3 
- need API key and some other Auth: JIRA, Slack
- `usecase_claude_web_JIRA.py`

### Use case 4 [Pending]
- need tool usage in local/runtime environemnt, like screenshot, Apple Calendar
- `usecase_claude_os_screenshot.py`


## API Database

### Tool Naming Rules
Always look like `PROVIDERNAME_ACTIONNAME` and all uppercase:
- `PROVIDERNAME` is the name of the API provider, e.g. `GOOGLE`, `JIRA`, `SLACK`
- `ACTIONNAME` is the name of the API action, e.g. `SEARCH`, `CREATE_EVENT`. Usually, put the verb in the beginning, like `JIRA_SEARCH_DASHBOARD`


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



## Unit Test

### Running the Tests
To run the tests, navigate to the `AnyActions/AAPI/tests` directory in your terminal and execute:
```bash
python -m unittest discover
```

This command will discover and run all the test files in the directory that match the pattern `test*.py`.

### Notes
- The tests use mocking to simulate file operations and environment checks, which allows for isolated testing without needing actual files or environment states.
- You can expand the tests further based on additional methods and functionalities in library.