import os
import dotenv
from openai import OpenAI


"""
This function generates an API description file which includes:
    the tool description passed to LLM
    the function description
    the function parameters description
"""



def genDscpFromYaml(yaml_path):
    dotenv.load_dotenv()
    client = OpenAI(api_key=os.getenv('OPENAI_KEY'))

    completion = client.chat.completions.create(
    model="o1-mini-2024-09-12",
    messages=[
        {"role": "user", "content": "You are a helpful assistant. Hello!"}
    ]
    )

    print(completion.choices[0].message.content)
