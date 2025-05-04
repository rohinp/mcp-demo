from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
import time
from pydantic import BaseModel

app = FastAPI(title="Travel Advisory Service")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Simulated travel advisory database
advisory_data = {
    "amsterdam": {
        "safety_level": "High",
        "advisories": [
            "Bicycle traffic can be intense, watch when crossing bike lanes",
            "Pickpocketing is common in tourist areas",
            "Public transportation is reliable and recommended"
        ],
        "best_time_to_visit": "April to May (tulip season) or September"
    },
    "london": {
        "safety_level": "High",
        "advisories": [
            "Keep valuables secure on public transport",
            "Look right before crossing streets (left-side driving)",
            "Carry an umbrella as weather can change quickly"
        ],
        "best_time_to_visit": "May to September"
    },
    "new york": {
        "safety_level": "Moderate",
        "advisories": [
            "Be aware of your surroundings, especially at night",
            "Use official taxis or ride-sharing services",
            "The subway is efficient but can be confusing for first-time visitors"
        ],
        "best_time_to_visit": "April to June or September to November"
    },
    "tokyo": {
        "safety_level": "Very High",
        "advisories": [
            "Public transportation can be extremely crowded during rush hours",
            "English signage is limited in some areas",
            "Tipping is not customary and may cause confusion"
        ],
        "best_time_to_visit": "March to May or October to November"
    },
    "sydney": {
        "safety_level": "High",
        "advisories": [
            "Apply sunscreen regularly, UV levels are high",
            "Swim only at patrolled beaches between the flags",
            "Wildlife can be dangerous, follow local guidance"
        ],
        "best_time_to_visit": "September to November or March to May"
    },
}

class AdvisoryRequest(BaseModel):
    city: str

@app.get("/")
def read_root():
    return {"message": "Travel Advisory Service API", "status": "running"}

@app.post("/advisory")
def get_advisory(request: AdvisoryRequest):
    # Simulate network latency
    time.sleep(0.25)
    
    city = request.city.lower()
    
    if city not in advisory_data:
        # Return generic advisory for unknown cities
        return {
            "city": request.city,
            "safety_level": "Unknown",
            "advisories": [
                "Research local customs before visiting",
                "Register with your embassy when traveling internationally",
                "Keep copies of important documents"
            ],
            "best_time_to_visit": "Varies by season",
            "source": "default"
        }
    
    # Get data for known city
    city_data = advisory_data[city]
    
    return {
        "city": request.city,
        "safety_level": city_data["safety_level"],
        "advisories": city_data["advisories"],
        "best_time_to_visit": city_data["best_time_to_visit"],
        "source": "database"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    print("Starting Travel Advisory Service on port 8002...")
    print("Health check endpoint available at: http://localhost:8002/health")
    uvicorn.run(app, host="0.0.0.0", port=8002, log_level="info")  # Note different port from other services
