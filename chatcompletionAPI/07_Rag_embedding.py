#importing important utilities and libraries
import json
import requests
import openai
from openai import AzureOpenAI
import os
from dotenv import load_dotenv


#setting openai configuration details
load_dotenv()
deployment_name = os.getenv('get_embed_model')


#creating an Azure OpenAI client
client = AzureOpenAI(
  api_key = os.getenv("get_resource_key"),  
  api_version = "2024-02-15-preview",
  azure_endpoint =os.getenv("get_resource_api_endpoint") 
)

data="red is a color"

response = client.embeddings.create(
    input = data,
    model= deployment_name
)


print(response.model_dump_json(indent=2))