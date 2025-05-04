from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
import time
from pydantic import BaseModel

app = FastAPI(title="Forecast Service")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Simulated forecast database
forecast_data = {
    "amsterdam": ["Expect rain tomorrow", "Temperature dropping next week", "Sunny weekend ahead"],
    "london": ["Foggy conditions expected to continue", "Rain clearing by Friday", "Cool temperatures next week"],
    "new york": ["Heat wave coming", "Thunderstorms possible on Thursday", "Clear skies for the weekend"],
    "tokyo": ["Typhoon warning for next week", "Humidity increasing", "Clear and warm weekend"],
    "sydney": ["Perfect beach weather ahead", "Possible storms by Sunday", "Temperatures rising next week"],
}

class ForecastRequest(BaseModel):
    city: str
    days: int = 3  # Default forecast for 3 days

@app.get("/")
def read_root():
    return {"message": "Forecast Service API", "status": "running"}

@app.post("/forecast")
def get_forecast(request: ForecastRequest):
    # Simulate network latency
    time.sleep(0.3)
    
    city = request.city.lower()
    days = min(request.days, 7)  # Cap at 7 days
    
    if city not in forecast_data:
        # Return generic forecast for unknown cities
        generic_forecasts = [
            f"Day {i+1}: {random.choice(['Sunny', 'Cloudy', 'Rainy', 'Partly cloudy'])}" 
            for i in range(days)
        ]
        return {
            "city": request.city,
            "forecast": generic_forecasts,
            "days": days,
            "source": "default"
        }
    
    # Get data for known city
    city_forecasts = forecast_data[city]
    
    # Generate a forecast with some randomness
    if len(city_forecasts) >= days:
        selected_forecasts = random.sample(city_forecasts, days)
    else:
        # If we don't have enough forecasts, repeat some with day numbers
        selected_forecasts = [f"Day {i+1}: {random.choice(city_forecasts)}" for i in range(days)]
    
    return {
        "city": request.city,
        "forecast": selected_forecasts,
        "days": days,
        "source": "database"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)  # Note different port from weather service
