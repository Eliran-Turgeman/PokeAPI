from fastapi import FastAPI, Path
from pydantic import BaseModel
from typing import Optional
import pandas as pd
from database import get_poke_by_name, get_poke_by_type

app = FastAPI()


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
    return {"Message": "Nothing interesting here"}


@app.get("/poke/{pokemon_name}")
def get_pokemon_by_name(pokemon_name: str = Path(None,
                                                 description="Name of the pokemon you'd like to retrieve")):
    pokemon = get_poke_by_name(pokemon_name)

    return {"Pokemon": pokemon[1],
            "Types": [pokemon[2], pokemon[3]],
            "HP": pokemon[5],
            "Attack": pokemon[6],
            "Special Attack": pokemon[7],
            "Defense": pokemon[8],
            "Special Defense": pokemon[9],
            }


@app.get("/poketype/{poke_type}")
def get_pokemon_by_type(poke_type: str = Path(None,
                                              description="Primary type of the pokemons you want to query"),
                        type2: Optional[str] = None):
    pokemons = get_poke_by_type(poke_type, type2)
    result = {}
    for idx, pokemon in enumerate(pokemons):
        result[idx] = {"Pokemon": pokemon[1],
            "Types": [pokemon[2], pokemon[3]],
            "HP": pokemon[5],
            "Attack": pokemon[6],
            "Special Attack": pokemon[7],
            "Defense": pokemon[8],
            "Special Defense": pokemon[9],
            }

    return result



@app.post("/newPoke/{pokemon_name}")
def create_pokemon(pokemon_name: int, pokemon: Pokemon):
    # if pokemon_name
    return {}
