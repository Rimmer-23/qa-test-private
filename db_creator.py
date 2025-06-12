import sqlite3
import os
import random

os.makedirs("database", exist_ok=True)

DB_PATH = 'database/original.db'

def create_db():
    print(">>> STARTING DATABASE CREATION")

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(">>> Old database removed")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE weapons (
            weapon TEXT PRIMARY KEY,
            reload_speed INTEGER,
            rotation_speed INTEGER,
            diameter INTEGER,
            power_volley INTEGER,
            count INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE hulls (
            hull TEXT PRIMARY KEY,
            armor INTEGER,
            type INTEGER,
            capacity INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE engines (
            engine TEXT PRIMARY KEY,
            power INTEGER,
            type INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE ships (
            ship TEXT PRIMARY KEY,
            weapon TEXT,
            hull TEXT,
            engine TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print(f">>> Database created at {DB_PATH}")

def populate_db():
    print(">>> POPULATING DATABASE")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    def rand(): return random.randint(1, 20)

    # Weapons
    weapons = [f"Weapon-{i}" for i in range(1, 21)]
    for w in weapons:
        cursor.execute(
            "INSERT INTO weapons VALUES (?, ?, ?, ?, ?, ?)",
            (w, rand(), rand(), rand(), rand(), rand())
        )

    # Hulls
    hulls = [f"Hull-{i}" for i in range(1, 6)]
    for h in hulls:
        cursor.execute(
            "INSERT INTO hulls VALUES (?, ?, ?, ?)",
            (h, rand(), rand(), rand())
        )

    # Engines
    engines = [f"Engine-{i}" for i in range(1, 7)]
    for e in engines:
        cursor.execute(
            "INSERT INTO engines VALUES (?, ?, ?)",
            (e, rand(), rand())
        )

    # Ships
    ships = [f"Ship-{i}" for i in range(1, 201)]
    for s in ships:
        cursor.execute(
            "INSERT INTO ships VALUES (?, ?, ?, ?)",
            (
                s,
                random.choice(weapons),
                random.choice(hulls),
                random.choice(engines)
            )
        )

    conn.commit()
    conn.close()
    print(">>> POPULATION COMPLETE")

if __name__ == '__main__':
    create_db()
    populate_db()
