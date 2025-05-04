# MCP (Multi-Client Protocol) Demo

This project demonstrates a simple MCP architecture with multiple microservices and a client application. The demo includes:

1. **Weather Service**: Provides current weather information for cities
2. **Forecast Service**: Provides weather forecasts for cities
3. **Travel Advisory Service**: Provides travel safety and recommendations for cities
4. **Client Web App**: A web interface to interact with all services
5. **Agent**: An LLM-powered agent that can use all services to answer questions

## Architecture

```
┌─────────────┐     ┌───────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│             │     │                   │     │                 │     │                 │
│  Client App │────▶│  Weather Service  │     │ Forecast Service│     │ Advisory Service│
│  (Port 8080)│     │    (Port 8000)    │     │   (Port 8001)   │     │   (Port 8002)   │
│             │     │                   │     │                 │     │                 │
└─────────────┘     └───────────────────┘     └─────────────────┘     └─────────────────┘
        │                    ▲                        ▲                        ▲
        │                    │                        │                        │
        └────────────────────┼────────────────────────┼────────────────────────┘
                             │                        │                        │
                        ┌────┴────────────────────────┴────────────────────────┘
                        │                             
                        │            Agent           
                        │                             
                        └─────────────────────────────
```

## Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai/) with the Mistral model installed (for the agent demo)

## Setup

1. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. If you want to use the agent demo, make sure Ollama is installed and the Mistral model is available:
   ```
   ollama pull mistral
   ```

## Running the Demo

### Option 1: Using the Launcher Script (Recommended)

The easiest way to run the demo is to use the launcher script:

```
python start_demo.py
```

This will:
1. Start the Weather Service on port 8000
2. Start the Forecast Service on port 8001
3. Start the Travel Advisory Service on port 8002
4. Start the Client Web App on port 8080
4. Open the Client Web App in your default browser

Press Ctrl+C to stop all services when you're done.

### Option 2: Manual Startup

If you prefer to start each service manually, open separate terminal windows and run:

1. Weather Service:
   ```
   python weather_tool.py
   ```

2. Forecast Service:
   ```
   python forecast_service.py
   ```

3. Travel Advisory Service:
   ```
   python advisory_service.py
   ```

4. Client Web App:
   ```
   python client_app.py
   ```

## Using the Demo

1. **Web Client**:
   - Open http://localhost:8080 in your browser
   - Enter a city name (e.g., Amsterdam, London, Tokyo)
   - Click "Get Weather & Forecast" to see data from both services

2. **Agent Demo**:
   - Make sure both services are running
   - Run the agent demo:
     ```
     python agent.py
     ```
   - The agent will demonstrate how it can use both services to answer weather-related questions

## API Endpoints

### Weather Service (Port 8000)

- `GET /`: Service info
- `GET /health`: Health check
- `POST /weather`: Get weather for a city
  ```json
  {
    "city": "Amsterdam"
  }
  ```

### Forecast Service (Port 8001)

- `GET /`: Service info
- `GET /health`: Health check
- `POST /forecast`: Get forecast for a city
  ```json
  {
    "city": "Amsterdam",
    "days": 3
  }
  ```

### Travel Advisory Service (Port 8002)

- `GET /`: Service info
- `GET /health`: Health check
- `POST /advisory`: Get travel advisory for a city
  ```json
  {
    "city": "Amsterdam"
  }
  ```

### Client Web App (Port 8080)

- `GET /`: Web interface
- `POST /get_weather_info`: Backend endpoint that calls both services
  ```
  city=Amsterdam
  ```

## Project Structure

- `weather_tool.py`: Weather service implementation
- `forecast_service.py`: Forecast service implementation
- `advisory_service.py`: Travel Advisory service implementation
- `client_app.py`: Web client application
- `agent.py`: LLM agent that uses all services
- `start_demo.py`: Launcher script to start all components
- `templates/index.html`: Web interface template
- `static/`: Static assets for the web interface
