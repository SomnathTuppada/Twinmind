import subprocess
import time
import requests
import json

# Start server in background
print("Starting server...")
proc = subprocess.Popen(
    ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"],
    cwd=r"C:\Users\SOMNATH TUPPADA\OneDrive\Desktop\Projects for Companies\twinmind\second mind\backend"
)

# Wait for server to start
time.sleep(5)

try:
    # Test home endpoint
    print("\nTesting home endpoint...")
    response = requests.get("http://localhost:8000/", timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test query endpoint
    print("\nTesting query endpoint...")
    response = requests.post(
        "http://localhost:8000/query",
        json={"query": "test"},
        timeout=30
    )
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    
except Exception as e:
    print(f"Error: {type(e).__name__}: {str(e)}")

finally:
    print("\nStopping server...")
    proc.terminate()
    proc.wait(timeout=5)
    print("Done")
