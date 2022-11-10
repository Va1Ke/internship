from fastapi.testclient import TestClient
from app.main import app
from app.database import db, test_db

client = TestClient(app)
app.dependency_overrides[db] = test_db

def test_read_item():
    response = client.get("/users/", json={
  "email": "user7",
  "name": "user7",
  "password": "7",
  "creation_date": "2022-11-09T21:14:29.914286"
})
    assert response.status_code == 200
    assert response.json() == {
  "email": "user7",
  "id": 5,
  "name": "user7",
  "password": "7",
  "creation_date": "2022-11-09T21:14:29.914286"
}