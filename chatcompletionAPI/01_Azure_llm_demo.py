from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = AzureOpenAI(
    azure_endpoint = os.getenv("OPENAI_API_BASE"),
    api_key = os.getenv("OPENAI_API_KEY"),
    api_version="2024-10-21"
)

response = client.chat.completions.create(
    model = "gpt-4.1-mini-saroj",
    messages = [
         {"role": "system", "content": "act like a mentor"},
         {"role": "user", "content": "give me road map for AI path"}
        
    ]
)

print("final answe", response.choices[0].message.content)