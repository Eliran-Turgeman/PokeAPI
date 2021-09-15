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
    update_poke, delete_poke, PokeDatabase

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
    if not pokemon:
        return JSONResponse({'message': 'Pokemon Not Found'},
                            status_code=HTTP_404_NOT_FOUND)

    type2 = pokemon[2].capitalize() if pokemon[2] else pokemon[2]
    result = {"Pokemon": pokemon[0].capitalize(),
              "Types": [pokemon[1].capitalize(), type2],
              "HP": pokemon[4],
              "Attack": pokemon[5],
              "Special Attack": pokemon[6],
              "Defense": pokemon[7],
              "Special Defense": pokemon[8],
              }
    return JSONResponse({'message': 'Pokemon Found',
                         'data': result}, status_code=HTTP_200_OK)


@app.get("/poketype/{poke_type}")
def get_pokemon_by_type(poke_type: str = Path(None,
                                              description="Primary type of "
                                                          "the pokemons you "
                                                          "want to query"),
                        type2: Optional[str] = None):
    pokemons = get_poke_by_type(poke_type.lower(), type2.lower())
    if not pokemons:
        return JSONResponse({'message': 'Pokemon Not Found'},
                            status_code=HTTP_404_NOT_FOUND)
    result = {}
    for idx, pokemon in enumerate(pokemons):
        result[idx] = {"Pokemon": pokemon[0].capitalize(),
                       "Types": [pokemon[1].capitalize(),
                                 pokemon[2].capitalize()],
                       "HP": pokemon[4],
                       "Attack": pokemon[5],
                       "Special Attack": pokemon[6],
                       "Defense": pokemon[7],
                       "Special Defense": pokemon[8],
                       }

    return JSONResponse({'message': 'Pokemons Found',
                         'data': result}, status_code=HTTP_200_OK)


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
