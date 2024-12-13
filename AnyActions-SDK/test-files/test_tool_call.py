"""_tool_definition_
{
    "type": "function",
    "function": {
        "name": "test_tool_call",
        "parameters": {
            "type": "object",
            "properties": {
                "q": {
                    "type": "string"
                }
            },
            "required": [
                "q"
            ],
            "additionalProperties": false
        }
    }
}
"""

from anyactions import generated_action

@generated_action
def test_tool_call(q: str):
    return q