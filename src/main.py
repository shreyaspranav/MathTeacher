from langgraph.prebuilt import create_react_agent
import dotenv

dotenv.load_dotenv()

def get_weather(city: str) -> str:  
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_react_agent(
    model="google_genai:gemini-2.0-flash",  
    tools=[get_weather],  

    prompt="You are a helpful assistant"  
)

# Run the agent
response = agent.invoke(
    {"messages": [{"role": "user", "content": "Introduce about yourself to a croud of kids"}]}
)

print(response['messages'][1].content)