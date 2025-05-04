from langchain.tools import Tool
import requests
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOllama
import time
import sys

# Weather service tool
def call_weather(city: str) -> str:
    try:
        res = requests.post("http://localhost:8000/weather", json={"city": city}, timeout=3)
        data = res.json()
        return f"The weather in {data['city']} is {data['temperature']} and {data['condition']}." 
    except Exception as e:
        return f"Error getting weather for {city}: {str(e)}"

# Forecast service tool
def call_forecast(city: str, days: int = 3) -> str:
    try:
        res = requests.post(
            "http://localhost:8001/forecast", 
            json={"city": city, "days": days},
            timeout=3
        )
        data = res.json()
        forecast_text = "\n".join([f"- {item}" for item in data['forecast']])
        return f"The {days}-day forecast for {data['city']} is:\n{forecast_text}"
    except Exception as e:
        return f"Error getting forecast for {city}: {str(e)}"

# Travel Advisory service tool
def call_advisory(city: str) -> str:
    try:
        res = requests.post(
            "http://localhost:8002/advisory", 
            json={"city": city},
            timeout=3
        )
        data = res.json()
        advisories = "\n".join([f"- {item}" for item in data['advisories']])
        return f"Travel advisory for {data['city']}:\nSafety Level: {data['safety_level']}\nBest time to visit: {data['best_time_to_visit']}\n\nAdvisories:\n{advisories}"
    except Exception as e:
        return f"Error getting travel advisory for {city}: {str(e)}"

# Combined service tool
def get_all_info(city: str) -> str:
    weather_info = call_weather(city)
    forecast_info = call_forecast(city)
    advisory_info = call_advisory(city)
    return f"{weather_info}\n\n{forecast_info}\n\n{advisory_info}"

# Define tools
weather_tool = Tool.from_function(
    name="get_weather",
    description="Gets the current weather for a given city. Input should be the city name, e.g., 'Amsterdam'.",
    func=call_weather,
)

forecast_tool = Tool.from_function(
    name="get_forecast",
    description="Gets the weather forecast for a given city. Input should be the city name, e.g., 'London'.",
    func=call_forecast,
)

advisory_tool = Tool.from_function(
    name="get_travel_advisory",
    description="Gets travel advisory information for a given city, including safety level and travel tips. Input should be the city name, e.g., 'Tokyo'.",
    func=call_advisory,
)

combined_tool = Tool.from_function(
    name="get_all_city_info",
    description="Gets comprehensive information about a city including weather, forecast, and travel advisory. Input should be the city name, e.g., 'New York'.",
    func=get_all_info,
)

def run_agent_demo():
    # Connect to local LLM
    print("Initializing LLM connection...")
    llm = ChatOllama(model="mistral", temperature=0)

    # Initialize agent with all tools
    print("Initializing agent...")
    agent = initialize_agent(
        tools=[weather_tool, forecast_tool, advisory_tool, combined_tool],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    # Ask questions that require different tools
    questions = [
        "What's the weather in Amsterdam today?",
        "What's the forecast for Tokyo?",
        "Is Sydney safe for tourists?",
        "I'm planning a trip to London. What's the weather and travel information?"
    ]

    for question in questions:
        print("\n" + "-"*50)
        print(f"Question: {question}")
        print("-"*50)
        try:
            response = agent.run(question)
            print("\nFinal Answer:", response)
        except Exception as e:
            print(f"Error: {str(e)}")
        time.sleep(1)  # Small pause between questions

if __name__ == "__main__":
    print("MCP Demo - Agent with Multiple Services")
    print("=" * 50)
    print("This demo shows an agent using multiple microservices (weather, forecast, and travel advisory)")
    print("Make sure all services are running before starting the agent:")
    print("- Weather Service: http://localhost:8000")
    print("- Forecast Service: http://localhost:8001")
    print("- Travel Advisory Service: http://localhost:8002")
    print("=" * 50)
    
    # Give the user a chance to start services if needed
    input("Press Enter to start the agent demo...")
    
    run_agent_demo()
