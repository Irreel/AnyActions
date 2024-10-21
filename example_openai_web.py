import openai

from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv('OPENAI_KEY')

# Define a function to get the delivery date (this would typically interact with your order system)
def get_delivery_date(order_id):
    # This is a placeholder function. In a real scenario, you'd query your order system.
    # For demonstration, we'll return a fixed date.
    return "2023-07-15"

# Define the get_delivery_date function as a tool
def get_delivery_date_tool(order_id):
    delivery_date = get_delivery_date(order_id)
    return f"The delivery date for order {order_id} is {delivery_date}."



tools = [
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
]

messages = [
    {"role": "system", "content": "You are a helpful customer support assistant. Use the supplied tools to assist the user."},
    {"role": "user", "content": "Hi, can you tell me the delivery date for my order with ID 1234?"}
]

response = openai.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
)

print(type(response)) # <class 'openai.types.chat.chat_completion.ChatCompletion'>


"""sample response - Succeeded
ChatCompletion(
    id='chatcmpl-AGhdI7QUfUJISQQ7HHs1BsHgS2tnX', 
    choices=[Choice(finish_reason='tool_calls', index=0, logprobs=None, 
    message=ChatCompletionMessage(
        content=None, 
        refusal=None, 
        role='assistant', 
        function_call=None, 
        tool_calls=[
            ChatCompletionMessageToolCall(
                id='call_sx4YzfRsy87qvXvv9jqIgvgn', 
                function=Function(arguments='{"order_id":"1234"}', name='get_delivery_date'), 
                type='function')
            ]
        )
    )], 
    created=1728544336, 
    model='gpt-4o-2024-08-06', 
    object='chat.completion', 
    service_tier=None, system_fingerprint='fp_2f406b9113', 
    usage=CompletionUsage(completion_tokens=17, prompt_tokens=112, total_tokens=129, prompt_tokens_details={'cached_tokens': 0}, 
                          completion_tokens_details={'reasoning_tokens': 0})
    )

"""

"""sample response - Failed
ChatCompletion(
    id='chatcmpl-AGhcH7s5aYXg3lzvHJYsQcTk20oRR', 
    choices=[Choice(finish_reason='stop', index=0, logprobs=None, 
    message=ChatCompletionMessage(
        content='Could you please provide the order ID so I can check the delivery date for you?', 
        refusal=None, 
        role='assistant', 
        function_call=None, 
        tool_calls=None)
        )
        ], 
    created=1728544273, 
    model='gpt-4o-2024-08-06', 
    object='chat.completion', 
    service_tier=None, system_fingerprint='fp_2f406b9113', 
    usage=CompletionUsage(completion_tokens=18, prompt_tokens=107, total_tokens=125, prompt_tokens_details={'cached_tokens': 0}, 
                            completion_tokens_details={'reasoning_tokens': 0}))

"""