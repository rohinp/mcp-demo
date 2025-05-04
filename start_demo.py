#!/usr/bin/env python3
"""
MCP Demo Launcher
This script helps launch all the components of the MCP demo.
"""

import os
import sys
import time
import subprocess
import signal
import webbrowser
import atexit

# Global variables to track processes
processes = []

def print_header(message):
    """Print a formatted header message."""
    print("\n" + "=" * 60)
    print(f" {message}")
    print("=" * 60)

def start_service(name, command, cwd=None):
    """Start a service process and return the process object."""
    print(f"Starting {name}...")
    
    # Use shell=True on Windows, shell=False on Unix-like systems
    use_shell = sys.platform == 'win32'
    
    process = subprocess.Popen(
        command,
        cwd=cwd,
        shell=use_shell,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )
    
    # Register the process for cleanup
    processes.append((name, process))
    
    # Give the process a moment to start
    time.sleep(1)
    
    # Check if process is still running
    if process.poll() is not None:
        print(f"Error: {name} failed to start!")
        return None
    
    print(f"{name} started with PID {process.pid}")
    return process

def cleanup():
    """Clean up all running processes."""
    print_header("Shutting down all services")
    
    for name, process in processes:
        if process.poll() is None:  # If process is still running
            print(f"Terminating {name} (PID: {process.pid})...")
            try:
                if sys.platform == 'win32':
                    process.terminate()
                else:
                    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            except (OSError, ProcessLookupError) as e:
                print(f"Error terminating {name}: {e}")
    
    # Give processes time to terminate gracefully
    time.sleep(2)
    
    # Force kill any remaining processes
    for name, process in processes:
        if process.poll() is None:
            print(f"Force killing {name} (PID: {process.pid})...")
            try:
                process.kill()
            except (OSError, ProcessLookupError) as e:
                print(f"Error killing {name}: {e}")

def check_service(url, service_name, max_retries=5):
    """Check if a service is responding at the given URL."""
    import requests
    
    print(f"Checking {service_name} at {url}...")
    
    for i in range(max_retries):
        try:
            response = requests.get(url, timeout=1)
            if response.status_code == 200:
                print(f"✅ {service_name} is running!")
                return True
        except requests.RequestException:
            pass
        
        print(f"Waiting for {service_name} to start ({i+1}/{max_retries})...")
        time.sleep(2)
    
    print(f"❌ {service_name} is not responding!")
    return False

def main():
    """Main function to start all services."""
    # Register cleanup function to run on exit
    atexit.register(cleanup)
    
    print_header("MCP Demo Launcher")
    print("This script will start all components of the MCP demo:")
    print("1. Weather Service (Port 8000)")
    print("2. Forecast Service (Port 8001)")
    print("3. Travel Advisory Service (Port 8002)")
    print("4. Client Web App (Port 8080)")
    
    # Get the directory of this script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Get the Python executable path from the virtual environment
    python_executable = sys.executable
    print(f"Using Python executable: {python_executable}")
    
    # Start Weather Service
    weather_service = start_service(
        "Weather Service",
        [python_executable, "weather_tool.py"],
        cwd=base_dir
    )
    
    # Start Forecast Service
    forecast_service = start_service(
        "Forecast Service",
        [python_executable, "forecast_service.py"],
        cwd=base_dir
    )
    
    # Start Travel Advisory Service
    advisory_service = start_service(
        "Travel Advisory Service",
        [python_executable, "advisory_service.py"],
        cwd=base_dir
    )
    
    # Check if services are running
    weather_running = check_service("http://localhost:8000/health", "Weather Service")
    forecast_running = check_service("http://localhost:8001/health", "Forecast Service")
    advisory_running = check_service("http://localhost:8002/health", "Travel Advisory Service")
    
    if not (weather_running and forecast_running and advisory_running):
        print("Some services failed to start. Check the logs above.")
        sys.exit(1)
    
    # Start Client Web App
    client_app = start_service(
        "Client Web App",
        [python_executable, "client_app.py"],
        cwd=base_dir
    )
    
    if client_app:
        # Open web browser
        print("\nOpening client web app in browser...")
        time.sleep(2)  # Give the app a moment to start
        webbrowser.open("http://localhost:8080")
        
        print_header("MCP Demo is running")
        print("Access the client web app at: http://localhost:8080")
        print("Weather Service API: http://localhost:8000")
        print("Forecast Service API: http://localhost:8001")
        print("Travel Advisory API: http://localhost:8002")
        print("\nPress Ctrl+C to stop all services and exit.")
        
        try:
            # Keep the script running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nReceived keyboard interrupt. Shutting down...")
    else:
        print("Failed to start the client web app.")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nShutting down due to keyboard interrupt...")
    finally:
        cleanup()
