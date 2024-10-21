import anthropic

from dotenv import load_dotenv
import os

load_dotenv()
claude_api_key = os.getenv('CLAUDE_KEY')
client = anthropic.Anthropic(api_key=claude_api_key)


response = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=1024,
    tools=[
        {
            "name": "get_weather",
            "description": "Get the current weather in a given location",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    }
                },
                "required": ["location"],
            },
        }
    ],
    messages=[{"role": "user", "content": "What's the weather like in San Francisco?"}],
)
print(type(response)) #<class 'anthropic.types.message.Message'>

"""sample response
{
  "id": "msg_01Aq9w938a90dw8q",
  "model": "claude-3-5-sonnet-20240620",
  "stop_reason": "tool_use",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "<thinking>I need to use the get_weather, and the user wants SF, which is likely San Francisco, CA.</thinking>"
    },
    {
      "type": "tool_use",
      "id": "toolu_01A09q90qw90lq917835lq9",
      "name": "get_weather",
      "input": {"location": "San Francisco, CA", "unit": "celsius"}
    }
  ]
}


"""

"""

Message(id='msg_017s6nshnDmhZTocxxSpVFMR', 
    content=[TextBlock
        (
            text="Certainly! I can help you get the current weather information for San Francisco. To do that, I'll use the available weather tool. Let me fetch that information for you right away.", 
            type='text'
        ), 
        ToolUseBlock(
            id='toolu_01J2aRbTWH1wSaEZ5vFgGBSN', 
            input={'location': 'San Francisco, CA'}, 
            name='get_weather', 
            type='tool_use'
        )], 
        model='claude-3-5-sonnet-20240620', 
        role='assistant', 
        stop_reason='tool_use', 
        stop_sequence=None, type='message', 
        usage=Usage(input_tokens=384, output_tokens=95))

"""

"""Response with no tool usage

Message(id='msg_01VTyWScAUwhuvqEoj4zwBNA', 
    content=[TextBlock(text="I apologize, but I don't have access to real-time weather information. Weather conditions can change rapidly, and without current data, I can't provide an accurate report for San Francisco or any other location. To get the most up-to-date and accurate weather information for San Francisco, you could:\n\n1. Check a weather website or app\n2. Look at a local news station's weather report\n3. Use a smart home device with weather capabilities\n4. Contact a local weather service\n\nThese sources will be able to give you the current conditions, forecast, and any weather alerts for San Francisco.", type='text')], 
    model='claude-3-5-sonnet-20240620', 
    role='assistant', 
    stop_reason='end_turn', 
    stop_sequence=None, type='message', 
    usage=Usage(input_tokens=16, output_tokens=129)) 
    
"""