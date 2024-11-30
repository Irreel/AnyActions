"""_tool_definition_
[This is the tool definition passing to the LLM]
{ 
    "name": "google_search",
    "description": "Performs a Google search for the given query",
    "input_schema": {
        "type": "object",
        "properties": {
            "q": {
                "type": "string",
                "description": "The search query to be used for the Google search"
            }
        },
        "required": ["q"]
    }
}
"""

def test_tool_calling():
    print("This is a test file to test the tool calling function")
    return