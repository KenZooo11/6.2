import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """Utwórz połączenie do bazy danych SQLite"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Połączono z bazą danych {db_file}, wersja SQLite: {sqlite3.version}")
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    """Utwórz tabelę w bazie danych SQLite"""
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def insert_data(conn, insert_data_sql, data):
    """Wstaw dane do tabeli w bazie danych SQLite"""
    try:
        c = conn.cursor()
        c.executemany(insert_data_sql, data)
        conn.commit()
        print("Dane zostały pomyślnie dodane do tabeli.")
    except Error as e:
        print(e)

def select_all(conn, table):
    """Pobierz wszystkie dane z tabeli w bazie danych SQLite"""
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()
    return rows

def delete(conn, table, record_id):
    """Usuń rekord z tabeli w bazie danych SQLite"""
    try:
        c = conn.cursor()
        c.execute(f"DELETE FROM {table} WHERE id=?", (record_id,))
        conn.commit()
        print(f"Rekord o ID {record_id} został pomyślnie usunięty z tabeli {table}.")
    except Error as e:
        print(e)

def update(conn, table, record_id, **kwargs):
    """ Aktualizuj rekord w tabeli w bazie danych SQLite """
    try:
        updates = [f"{key} = ?" for key in kwargs.keys()]
        updates = ", ".join(updates)
        
        values = tuple(kwargs.values())
        values += (record_id,)

        c = conn.cursor()
        c.execute(f"UPDATE {table} SET {updates} WHERE id=?", values)
        conn.commit()
        print(f"Rekord o ID {record_id} został pomyślnie zaktualizowany w tabeli {table}.")
    except Error as e:
        print(e)

if __name__ == '__main__':
    conn = create_connection("football_clubs.db")

    create_clubs_table_sql = """
    CREATE TABLE IF NOT EXISTS clubs (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        country TEXT NOT NULL
    );
    """
    create_table(conn, create_clubs_table_sql)

    create_players_table_sql = """
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER,
        position TEXT,
        club_id INTEGER,
        FOREIGN KEY (club_id) REFERENCES clubs (id)
    );
    """
    create_table(conn, create_players_table_sql)

    clubs_data = [
        ('FC Barcelona', 'Spain'),
        ('Manchester United', 'England'),
        ('Bayern Munich', 'Germany')
    ]
    insert_clubs_sql = """
    INSERT INTO clubs (name, country)
    VALUES (?, ?)
    """
    insert_data(conn, insert_clubs_sql, clubs_data)

    players_data = [
        ('Lionel Messi', 34, 'Forward', 1),
        ('Cristiano Ronaldo', 36, 'Forward', 2),
        ('Robert Lewandowski', 33, 'Forward', 3)
    ]
    insert_players_sql = """
    INSERT INTO players (name, age, position, club_id)
    VALUES (?, ?, ?, ?)
    """
    insert_data(conn, insert_players_sql, players_data)
        
    clubs = select_all(conn, "clubs")
    print("Kluby piłkarskie:")
    for club in clubs:
        print(club)

    players = select_all(conn, "players")
    print("\nZawodnicy:")
    for player in players:
        print(player)

    delete(conn, "players", 3)

    update(conn, "players", 2, age=30, position="Midfielder")

    conn.close()
