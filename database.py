from pathlib import Path
import sqlite3
import pandas as pd

DB_FILENAME = "poke_db.db"
COLUMNS = ['name', 'type1', 'type2', 'sum_stats',
           'hp', 'attack', 'special_attack', 'defense',
           'special_defense']


def init_db(filename: str = DB_FILENAME) -> None:
    if not Path(filename).is_file():
        Path(filename).touch()


def load_csv_to_db() -> None:
    init_db(DB_FILENAME)
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pokemons (name text, type1 text,
        type2 text, sum_stats int, hp int, attack int,
        special_attack int, defense int, special_defense int)
        ''')

    poke_data = pd.read_csv('Pokemon.csv')
    poke_data.drop(['#', 'Speed', 'Generation', 'Legendary'], axis=1,
                   inplace=True)

    poke_data.columns = COLUMNS
    poke_data['name'] = poke_data['name'].str.lower()
    poke_data['type1'] = poke_data['type1'].str.lower()
    poke_data['type2'] = poke_data['type2'].str.lower()
    poke_data.to_sql('Pokemons', conn, if_exists='append', index=False)


class PokeDatabase:
    def __init__(self, file=DB_FILENAME):
        self.file = file
        load_csv_to_db()

    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()


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
            SELECT * FROM Pokemons WHERE type1 = ?''', (type1,))

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
    with PokeDatabase(DB_FILENAME) as cursor:
        params = [type1, type2, sum_stats, hp, attack, special_attack,
                  defense, special_defense]
        params_names = ['type1', 'type2', 'sum_stats', 'hp', 'attack',
                        'special_attack', 'defense', 'special_defense']

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

