from pathlib import Path
import sqlite3
import pandas as pd

DB_FILENAME = "poke_db.db"


def table_exists(cursor):
    cursor.execute('''
        SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Pokemons' ''')

    if not cursor.fetchone()[0]:
        return False

    return True


def init_db():
    if not Path(DB_FILENAME).is_file():
        Path(DB_FILENAME).touch()


def load_csv_to_db():
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pokemons (name text, type1 text,
        type2 text, sum_stats int, hp int, attack int,
        special_attack int, defense int, special_defense int)
        ''')

    poke_data = pd.read_csv('Pokemon.csv')
    poke_data.drop(['#', 'Speed', 'Generation', 'Legendary'], axis=1, inplace=True)

    poke_data.columns = ['name', 'type1', 'type2', 'sum_stats',
                         'hp', 'attack', 'special_attack', 'defense',
                         'special_defense']

    poke_data.to_sql('Pokemons', conn, if_exists='append', index=False)


def get_poke_by_name(poke_name):
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()

    if not table_exists(cursor):
        load_csv_to_db()

    cursor.execute('''SELECT * FROM Pokemons WHERE name = ?''', (poke_name,))
    return cursor.fetchone()


def get_poke_by_type(type1, type2):
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()

    if not table_exists(cursor):
        load_csv_to_db()

    if type2:
        cursor.execute('''
        SELECT * FROM Pokemons WHERE type1 = ? AND type2 = ?''', (type1, type2))

    else:
        cursor.execute('''
        SELECT * FROM Pokemons WHERE type1 = ?''', (type1,))

    return cursor.fetchall()


def add_poke_to_db(name, type1, type2, sum_stats, hp, attack, special_attack,
                   defense, special_defense):
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()

    if not table_exists(cursor):
        load_csv_to_db()

    cursor.execute('''
    INSERT INTO Pokemons ('name', 'type1', 'type2', 'sum_stats',
    'hp', 'attack', 'special_attack', 'defense', 'special_defense')
    VALUES (?,?,?,?,?,?,?,?,?)''', (name, type1, type2, sum_stats, hp, attack,
                                    special_attack, defense, special_defense))

    conn.commit()


def update_poke(name, type1=None, type2=None, sum_stats=None, hp=None,
                attack=None, special_attack=None, defense=None,
                special_defense=None):

    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()

    if not table_exists(cursor):
        load_csv_to_db()

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

    conn.commit()


def delete_poke(name):
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()

    if not table_exists(cursor):
        load_csv_to_db()

    cursor.execute('''
    DELETE FROM Pokemons WHERE name = ?''', (name,))

    conn.commit()






