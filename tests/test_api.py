import sys
import os

from fastapi.testclient import TestClient

from ..app import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


