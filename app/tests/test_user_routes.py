import pytest
from httpx import AsyncClient
from app.main import app
from app.database import db, test_db

app.dependency_overrides[db] = test_db

@pytest.fixture(autouse=True)
def create_drop_all():
    from app.database import test_db
    test_db.drop_all()
    test_db.create_all()


@pytest.mark.anyio
async def test_root(create_drop_all):
    async with AsyncClient(app=app, base_url="http://127.0.0.1/users/") as ac:
        response = await ac.get("/users/")
    assert response.status_code == 200
    assert type(response) == list