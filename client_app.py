from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import requests
import os
import uvicorn

# Create templates directory if it doesn't exist
os.makedirs("templates", exist_ok=True)

app = FastAPI(title="Weather & Forecast Client")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/get_weather_info")
async def get_weather_info(city: str = Form(...)):
    # Call all services
    weather_data = None
    forecast_data = None
    advisory_data = None
    errors = []
    
    # Call weather service
    try:
        weather_response = requests.post(
            "http://localhost:8000/weather", 
            json={"city": city},
            timeout=3
        )
        if weather_response.status_code == 200:
            weather_data = weather_response.json()
        else:
            errors.append(f"Weather service error: {weather_response.status_code}")
    except Exception as e:
        errors.append(f"Weather service error: {str(e)}")
    
    # Call forecast service
    try:
        forecast_response = requests.post(
            "http://localhost:8001/forecast", 
            json={"city": city, "days": 3},
            timeout=3
        )
        if forecast_response.status_code == 200:
            forecast_data = forecast_response.json()
        else:
            errors.append(f"Forecast service error: {forecast_response.status_code}")
    except Exception as e:
        errors.append(f"Forecast service error: {str(e)}")
    
    # Call travel advisory service
    try:
        advisory_response = requests.post(
            "http://localhost:8002/advisory", 
            json={"city": city},
            timeout=3
        )
        if advisory_response.status_code == 200:
            advisory_data = advisory_response.json()
        else:
            errors.append(f"Advisory service error: {advisory_response.status_code}")
    except Exception as e:
        errors.append(f"Advisory service error: {str(e)}")
    
    # Return combined data
    return {
        "weather": weather_data,
        "forecast": forecast_data,
        "advisory": advisory_data,
        "errors": errors
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
