from database_utils import PokeDatabase, DB_FILENAME

def get_poke_by_name(poke_name: str) -> dict:
    with PokeDatabase(DB_FILENAME) as cursor:
        cursor.execute('''SELECT name, type1, type2, sum_stats,
           hp, attack, special_attack, defense,
           special_defense FROM Pokemons WHERE name = ?''',
                       (poke_name,))
        x = cursor.fetchone()
        return x


def get_poke_by_type(type1: str, type2: str = None) -> list:
    with PokeDatabase(DB_FILENAME) as cursor:
        if type2:
            cursor.execute('''
            SELECT name, type1, type2, sum_stats,
           hp, attack, special_attack, defense,
           special_defense FROM Pokemons WHERE type1 = ? AND type2 = ?''',
                           (type1, type2))

        else:
            cursor.execute('''
            SELECT name, type1, type2, sum_stats,
           hp, attack, special_attack, defense,
           special_defense FROM Pokemons WHERE type1 = ?''', (type1,))

        return cursor.fetchall()


def add_poke_to_db(name: str, type1: str, type2: str, sum_stats: int, hp: int,
                   attack: int, special_attack: int, defense: int,
                   special_defense: int) -> None:
    with PokeDatabase(DB_FILENAME) as cursor:
        cursor.execute('''
        INSERT INTO Pokemons ('name', 'type1', 'type2', 'sum_stats',
        'hp', 'attack', 'special_attack', 'defense', 'special_defense')
        VALUES (?,?,?,?,?,?,?,?,?)''', (name, type1, type2, sum_stats,
                                        hp, attack, special_attack, defense,
                                        special_defense))


def update_poke(name: str, type1: str = None, type2: str = None,
                sum_stats: int = None, hp: int = None, attack: int = None,
                special_attack: int = None, defense: int = None,
                special_defense: int = None) -> None:

    params = [type1, type2, sum_stats, hp, attack, special_attack,
                  defense, special_defense]
    params_names = ['type1', 'type2', 'sum_stats', 'hp', 'attack',
                    'special_attack', 'defense', 'special_defense']

    with PokeDatabase(DB_FILENAME) as cursor:
        for param, param_name in zip(params, params_names):
            if param:
                query = '''
                UPDATE Pokemons SET ''' + param_name + '''
                    = ? WHERE name = ?'''
            cursor.execute(query, (param, name))


def delete_poke(name: str) -> None:
    with PokeDatabase(DB_FILENAME) as cursor:
        cursor.execute('''
        DELETE FROM Pokemons WHERE name = ?''', (name,))


def get_poke_by_stats_above_or_below(hp: int, attack: int, sattack: int,
                             defense: int, sdefense: int, above: bool) -> list:
    params = [hp, attack, sattack, defense, sdefense]
    params_names = ['hp', 'attack', 'special_attack', 'defense', 'special_defense']
    operator = " > " if above else " < "

    query = '''SELECT name, type1, type2, sum_stats,
           hp, attack, special_attack, defense,
           special_defense FROM Pokemons WHERE '''

    for param, param_name in zip(params, params_names):
        if param:
            query += param_name + operator + str(param) + " AND "

    query = query[:-len(" AND ")]
    
    with PokeDatabase(DB_FILENAME) as cursor:
        cursor.execute(query)
        return cursor.fetchall()