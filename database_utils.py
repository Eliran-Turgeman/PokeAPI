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

    poke_data = pd.read_csv('Pokemon.csv')
    poke_data.drop(['#', 'Speed', 'Generation', 'Legendary'], axis=1,
                   inplace=True)

    poke_data.columns = COLUMNS
    poke_data['name'] = poke_data['name'].str.lower()
    poke_data['type1'] = poke_data['type1'].str.lower()
    poke_data['type2'] = poke_data['type2'].str.lower()
    try:
        poke_data.to_sql('Pokemons', conn, if_exists='fail', index=False)
    except ValueError:
        print("Can't create table")


def is_table_exists() -> bool:
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT count(*) FROM sqlite_master WHERE type='table' AND name='Pokemons'
    ''')
    
    return cursor.fetchone()[0]


class PokeDatabase:
    def __init__(self, file=DB_FILENAME):
        self.file = file
        if not is_table_exists():
            load_csv_to_db()

    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()