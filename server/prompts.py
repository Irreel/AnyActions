"""
Manage all the prompts we use here
"""


# TODO: Generate API function should be able to read API from local environment

genDscpFromYaml_withNoExec = """
You are a data processor responsible for extracting relevant information from a provided YAML file. Your task is to generate Python tools to enable an AI agent to interact with a specific external API defined in the YAML file.

Instructions:
For the specific endpoint, generate the following:

instruction: A URL link to the related API registration page, if not available, a URL link to its technical documentation.
tool_definition: A JSON object following OpenAI's tool calling format to describe the API endpoint.
tool_calling_function: A Python function to call the endpoint using the requests library.

An example tool_definition looks like this:
    {
        "type": "function",
        "function": {
            "name": "get_delivery_date",
            "description": "Get the delivery date for a customer's order. Call this whenever you need to know the delivery date, for example when a customer asks 'Where is my package'",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The customer's order ID.",
                    },
                },
                "required": ["order_id"],
                "additionalProperties": False,
            },
        }
    }

For the tool calling function, if it asks for an authorization token, you need to add this token as the first argument to the function.

Some information might be incomplete in the YAML file, so you need to infer from the endpoint description. If you are inferring a "name" in tool_definition, make sure the name is not duplicated with other endpoints in this YAML file.

You are processing the following YAML file this turn:
{source_yaml}

Specify the endpoint you are processing based on the following information:
{target_endpoint}
"""

genDscpFromYaml_withExec = """

"""


getInstructionFromDscp = """
Application website and application documentation link:
"""

structuredResponse = """
Please provide your response in the following JSON format:

{
    "instruction": "A clear instruction for the user explaining what will be done",
    "tool_definition": {
        "function": {
            "name": "name_of_the_function",
            "description": "description_of_what_the_function_does",
            "parameters": {
                "properties": {
                    "param1": {
                        "type": "type_of_parameter",
                        "description": "description_of_parameter"
                    }
                    // Add more parameters as needed
                },
                "required": ["list", "of", "required", "parameters"]
            }
        }
    },
    "tool_calling_function": "the_actual_function_call_python_code"
}
"""