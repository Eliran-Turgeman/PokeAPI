from typing import Optional
import json
from fastapi import FastAPI, Path, HTTPException, status
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from starlette.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT
)
from database import get_poke_by_name, get_poke_by_type, add_poke_to_db, \
    update_poke, delete_poke, PokeDatabase, get_poke_by_stats_above
from api_utils import prepare_result, api_reply

app = FastAPI()
db = PokeDatabase()


class Pokemon(BaseModel):
    name: str
    primary_type: str
    secondary_type: str
    sum_stats: int
    hit_points: int
    attack_strength: int
    defensive_strength: int
    special_attack_strength: int
    special_defensive_strength: int


@app.get("/")
def root():
    return JSONResponse({'message': "Welcome to PokeAPI"},
                        status_code=HTTP_200_OK)


@app.get("/poke/{pokemon_name}")
def get_pokemon_by_name(pokemon_name: str = Path(None,
                                                 description="Name of the "
                                                             "pokemon you'd "
                                                             "like to "
                                                             "retrieve")):
    pokemon = get_poke_by_name(pokemon_name.lower())
    return api_reply(pokemon)


@app.get("/poketype/{poke_type}")
def get_pokemon_by_type(poke_type: str = Path(None,
                                              description="Primary type of "
                                                          "the pokemons you "
                                                          "want to query"),
                        type2: Optional[str] = None):
    pokemons = get_poke_by_type(poke_type.lower(), type2.lower() if type2 else None)
    return api_reply(pokemons)


@app.get("/poke/above/")
def get_pokemon_by_stats_above(hp: Optional[int] = None,
                                attack: Optional[int] = None,
                                sattack: Optional[int] = None,
                                defense: Optional[int] = None,
                                sdefense: Optional[int] = None):
    params = [hp, attack, sattack, defense, sdefense]
    if all(param is None for param in params):
        return JSONResponse({'message': 'No parameters specified'},
                            status_code=HTTP_404_NOT_FOUND)
    pokemons = get_poke_by_stats_above(hp, attack, sattack, defense, sdefense)
    return api_reply(pokemons)


@app.post("/newPoke/{pokemon_name}")
def create_pokemon(pokemon_name: str, pokemon: Pokemon):
    if get_poke_by_name(pokemon_name.lower()):
        return JSONResponse({'message': 'Pokemon Already Exists'},
                            status_code=HTTP_409_CONFLICT)

    add_poke_to_db(pokemon.name.lower(), pokemon.primary_type.lower(),
                   pokemon.secondary_type.lower(),
                   pokemon.sum_stats, pokemon.hit_points,
                   pokemon.attack_strength, pokemon.special_attack_strength,
                   pokemon.defensive_strength,
                   pokemon.special_defensive_strength)

    return JSONResponse({'message': 'Pokemon Created Successfully'},
                        status_code=status.HTTP_201_CREATED)


@app.put("/updatePoke/{pokemon_name}")
def update_pokemon(pokemon_name: str, pokemon: Pokemon):
    if not get_poke_by_name(pokemon_name.lower()):
        return JSONResponse({'message': 'Pokemon Not Found'},
                            status_code=HTTP_404_NOT_FOUND)

    update_poke(pokemon_name.lower(), pokemon.primary_type.lower(),
                pokemon.secondary_type.lower(),
                pokemon.sum_stats, pokemon.hit_points,
                pokemon.attack_strength, pokemon.special_attack_strength,
                pokemon.defensive_strength,
                pokemon.special_defensive_strength)

    return JSONResponse({'message': 'Pokemon Details Updated'},
                        status_code=status.HTTP_200_OK)


@app.delete("/deletePoke/{pokemon_name}")
def delete_pokemon(pokemon_name: str):
    if not get_poke_by_name(pokemon_name.lower()):
        return JSONResponse({'message': 'Pokemon Not Found'},
                            status_code=HTTP_404_NOT_FOUND)

    delete_poke(pokemon_name.lower())

    return JSONResponse({'message': 'Pokemon Deleted Successfully'},
                        status_code=status.HTTP_200_OK)
