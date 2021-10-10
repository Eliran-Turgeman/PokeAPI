from fastapi.testclient import TestClient
from pokeapi import app
from starlette.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT
)
from tests_consts import VALID_POKE_NAME, INVALID_POKE_NAME
from tests_utils import assert_response_types


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == HTTP_200_OK
    assert response.json() == {'message': "Welcome to PokeAPI"}


def test_get_valid_poke_by_name():
    response = client.get(f"/poke/{VALID_POKE_NAME}")
    assert response.status_code == HTTP_200_OK
    response = response.json()
    assert response["data"]['0']["Pokemon"] == VALID_POKE_NAME
    assert_response_types(response, idx='0')