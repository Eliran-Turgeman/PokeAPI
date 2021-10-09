from fastapi.testclient import TestClient
from pokeapi import app
from starlette.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT
)

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == HTTP_200_OK
    assert response.json() == {'message': "Welcome to PokeAPI"}