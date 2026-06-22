import os
from dotenv import find_dotenv, load_dotenv
from openai import OpenAI

load_dotenv()
#GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
llm_model = "gpt-4o"
client = OpenAI(
    api_key=os.environ["GITHUB_TOKEN"],
    base_url="https://models.inference.ai.azure.com"
)
user_prompt = input("Enter your prompt: ")
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": user_prompt}
    ]
)

print("\nResponse:")
print(response.choices[0].message.content)