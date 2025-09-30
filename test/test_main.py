from fastapi.testclient import TestClient
from ..main import app  # Import your FastAPI app instance

client = TestClient(app)  # Initialize client with your app

def test_return_health_check():
    response = client.get("/healthy")  # Use the client to make the request
    assert response.status_code == 200
    assert response.json() == {"Status": "Healthy"}