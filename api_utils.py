from fastapi.responses import JSONResponse
from starlette.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT
)

def prepare_result(data):
    if not isinstance(data, list):
        data = [data]
        
    result = {}
    for idx, entry in enumerate(data):
        result[idx] = {"Pokemon": entry[0].capitalize(),
                       "Types": [entry[1].capitalize(),
                                 entry[2].capitalize() if entry[2] else None],
                       "HP": entry[4],
                       "Attack": entry[5],
                       "Special Attack": entry[6],
                       "Defense": entry[7],
                       "Special Defense": entry[8],
                       }
    return result


def api_reply(poke_data):
    if not poke_data:
        return JSONResponse({'message': 'Pokemon Not Found'},
                            status_code=HTTP_404_NOT_FOUND)

    result = prepare_result(poke_data)

    return JSONResponse({'message': 'Pokemons Found',
                         'data': result}, status_code=HTTP_200_OK)