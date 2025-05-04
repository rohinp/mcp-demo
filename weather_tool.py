from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import time

app = FastAPI(title="Weather Service")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Simulated weather database
weather_data = {
    "amsterdam": {"temperature_range": (15, 20), "conditions": ["sunny", "partly cloudy", "rainy"]},
    "london": {"temperature_range": (12, 18), "conditions": ["foggy", "rainy", "cloudy"]},
    "new york": {"temperature_range": (18, 25), "conditions": ["sunny", "windy", "partly cloudy"]},
    "tokyo": {"temperature_range": (20, 28), "conditions": ["humid", "sunny", "rainy"]},
    "sydney": {"temperature_range": (22, 30), "conditions": ["sunny", "clear", "hot"]},
}

class WeatherRequest(BaseModel):
    city: str

@app.get("/")
def read_root():
    return {"message": "Weather Service API", "status": "running"}

@app.post("/weather")
def get_weather(request: WeatherRequest):
    # Simulate network latency
    time.sleep(0.2)
    
    city = request.city.lower()
    
    if city not in weather_data:
        # Return generic data for unknown cities
        return {
            "city": request.city,
            "temperature": f"{random.randint(15, 25)}°C",
            "condition": random.choice(["sunny", "cloudy", "rainy"]),
            "source": "default"
        }
    
    # Get data for known city
    city_data = weather_data[city]
    temp_min, temp_max = city_data["temperature_range"]
    temperature = random.randint(temp_min, temp_max)
    condition = random.choice(city_data["conditions"])
    
    return {
        "city": request.city,
        "temperature": f"{temperature}°C",
        "condition": condition,
        "source": "database"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
