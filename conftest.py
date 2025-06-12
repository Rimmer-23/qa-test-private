import pytest
import sqlite3
import random
import shutil
import os

DB_ORIGINAL = "database/original.db"

@pytest.fixture(scope="session")
def original_and_randomized_dbs(tmp_path_factory):
    # Создаём временную папку
    temp_dir = tmp_path_factory.mktemp("data")
    randomized_db_path = temp_dir / "randomized.db"

    # Копируем оригинальную БД
    shutil.copy(DB_ORIGINAL, randomized_db_path)

    # Подключаемся к копии
    conn = sqlite3.connect(randomized_db_path)
    cursor = conn.cursor()

    # Получаем список всех кораблей
    ships = cursor.execute("SELECT * FROM ships").fetchall()

    for ship in ships:
        ship_name, weapon_id, hull_id, engine_id = ship

        # Выбираем случайно: менять компонент или параметр
        mode = random.choice(["swap_component", "modify_values"])

        if mode == "swap_component":
            # Меняем один из компонентов на случайный
            part = random.choice(["weapon", "hull", "engine"])
            table = part + "s"
            new_id = cursor.execute(f"""
                SELECT {part} FROM {table}
                WHERE {part} != ?
                ORDER BY RANDOM() LIMIT 1
            """, (ship[["weapon", "hull", "engine"].index(part)+1],)).fetchone()[0]

            cursor.execute(f"""
                UPDATE ships SET {part} = ? WHERE ship = ?
            """, (new_id, ship_name))

        else:  # modify_values
            for part, table, comp_id in [
                ("weapon", "weapons", weapon_id),
                ("hull", "hulls", hull_id),
                ("engine", "engines", engine_id)
            ]:
                # Получаем список всех полей (кроме текстового ключа)
                fields = [row[1] for row in cursor.execute(f"PRAGMA table_info({table})").fetchall()][1:]
                param = random.choice(fields)
                value = random.randint(1, 20)
                cursor.execute(f"""
                    UPDATE {table} SET {param} = ? WHERE {part} = ?
                """, (value, comp_id))

    conn.commit()
    conn.close()

    return DB_ORIGINAL, str(randomized_db_path)
