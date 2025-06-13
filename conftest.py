import pytest
import sqlite3
import random
import shutil
import os

DB_ORIGINAL = "database/original.db"

@pytest.fixture(scope="session")
def original_and_randomized_dbs(tmp_path_factory):
    # create a temporary directory
    temp_dir = tmp_path_factory.mktemp("data")
    randomized_db_path = temp_dir / "randomized.db"

    # Copy the original database
    shutil.copy(DB_ORIGINAL, randomized_db_path)

    # Connect to the copied database
    conn = sqlite3.connect(randomized_db_path)
    cursor = conn.cursor()

    # retrieve all ships
    ships = cursor.execute("SELECT * FROM ships").fetchall()

    for ship in ships:
        ship_name, weapon_id, hull_id, engine_id = ship

        # Randomly choose: swap a component or modify parameter values
        mode = random.choice(["swap_component", "modify_values"])

        if mode == "swap_component":
            # Replace one of the components (weapon, hull, engine) with a random one
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
            # For each component, change one random parameter to a new value
            for part, table, comp_id in [
                ("weapon", "weapons", weapon_id),
                 ("hull", "hulls", hull_id),
                ("engine", "engines", engine_id)
            ]:
                # Get all numeric fields (skip primary key)
                fields = [row[1] for row in cursor.execute(f"PRAGMA table_info({table})").fetchall()][1:]
                param = random.choice(fields)
                value = random.randint(1, 20)
                cursor.execute(f"""
                    UPDATE {table} SET {param} = ? WHERE {part} = ?
                """, (value, comp_id))

    conn.commit()
    conn.close()

    return DB_ORIGINAL, str(randomized_db_path)
