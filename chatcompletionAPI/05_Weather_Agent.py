import os, time, requests
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import MessageTextContent
from dotenv import load_dotenv

load_dotenv()

# ---- Weather Function ----
def get_weather(city: str):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200:
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        return f"Current temperature in {city}: {temp}°C, {description}"
    else:
        return f"Could not get weather for {city}"

# ---- Azure AI Agent Setup ----
project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=os.getenv("PROJECT_CONNECTION_STRING")
)

model = os.getenv("MODEL_DEPLOYMENT_NAME")

# Get weather data first
city = "New York"
weather_info = get_weather(city)
print(f"Weather fetched: {weather_info}")

with project_client:
    # Create agent with weather context
    agent = project_client.agents.create_agent(
        model=model,
        name="weather-assistant",
        instructions=f"""You are a helpful weather assistant. 
        Use this real-time weather data to answer questions: {weather_info}""",
    )
    print(f"Created agent, ID: {agent.id}")

    # Create thread
    thread = project_client.agents.create_thread()
    print(f"Created thread, ID: {thread.id}")

    # Create message
    message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content=f"What is the current temperature in {city}?"
    )
    print(f"Created message, ID: {message.id}")

    # Run agent
    run = project_client.agents.create_run(
        thread_id=thread.id,
        assistant_id=agent.id
    )

    # Wait for completion
    while run.status in ["queued", "in_progress", "requires_action"]:
        time.sleep(1)
        run = project_client.agents.get_run(
            thread_id=thread.id,
            run_id=run.id
        )
        print(f"Run status: {run.status}")

    # Get response
    messages = project_client.agents.list_messages(thread_id=thread.id)
    print("\n--- Agent Response ---")
    print(messages.data[0].content[0].text.value)