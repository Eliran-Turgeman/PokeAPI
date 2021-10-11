from fastapi.testclient import TestClient
from pokeapi import app
from starlette.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT
)
from tests_consts import VALID_POKE_NAME, INVALID_POKE_NAME, STATS_ABOVE_INPUT
from tests_utils import assert_response_types, build_request_url


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
    assert_response_types(response)


def test_get_invalid_poke_by_name():
    response = client.get(f"/poke/{INVALID_POKE_NAME}")
    assert response.status_code == HTTP_404_NOT_FOUND
    response = response.json()
    assert "data" not in response


def test_get_pokemon_by_stats_above():
    query_url = build_request_url("/poke/above/?", STATS_ABOVE_INPUT)
    response = client.get(query_url)
    assert response.status_code == HTTP_200_OK
    response = response.json()
    assert_response_types(response)


def test_get_pokemon_by_stats_below():
    query_url = build_request_url("/poke/below/?", STATS_ABOVE_INPUT)
    response = client.get(query_url)
    assert response.status_code == HTTP_200_OK
    response = response.json()
    assert_response_types(response)

