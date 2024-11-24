import os
import dotenv
from openai import OpenAI
from constants import ToolDefinition


"""
This function generates an API description file which includes:
    the tool description passed to LLM
    the function description
    the function parameters description
"""


def genDscpFromYaml(endpoint: dict, source_yaml_path: str):
    dotenv.load_dotenv()
    client = OpenAI(api_key=os.getenv('OPENAI_KEY'))

    completion = client.chat.completions.create(
    model="o1-mini-2024-09-12",
    messages=[
        {"role": "user", "content": "You are processing the following yaml file: " + yaml_path}
    ],
    response_format=ToolDefinition
    )

    print(completion.choices[0].message.content)


"""
Try generated from the sample yaml set
"""