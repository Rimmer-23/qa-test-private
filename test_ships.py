import sqlite3
import pytest

# Function to load data from the database
def load_components(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    ships = {row["ship"]: dict(row) for row in cur.execute("SELECT * FROM ships")}
    weapons = {row["weapon"]: dict(row) for row in cur.execute("SELECT * FROM weapons")}
    hulls = {row["hull"]: dict(row) for row in cur.execute("SELECT * FROM hulls")}
    engines = {row["engine"]: dict(row) for row in cur.execute("SELECT * FROM engines")}

    conn.close()
    return ships, weapons, hulls, engines

# hook function to generate 600 test cases
def pytest_generate_tests(metafunc):
    if "ship_name" in metafunc.fixturenames and "component_type" in metafunc.fixturenames:
        ship_ids = [f"Ship-{i}" for i in range(1, 201)]
        parts = ["weapon", "hull", "engine"]
        metafunc.parametrize("ship_name,component_type", [
            (ship, part) for ship in ship_ids for part in parts
        ])

# main test that checks each ship's component
def test_component_changed(original_and_randomized_dbs, ship_name, component_type):
    orig_db, rand_db = original_and_randomized_dbs

    o_ships, o_weapons, o_hulls, o_engines = load_components(orig_db)
    r_ships, r_weapons, r_hulls, r_engines = load_components(rand_db)

    o_ship = o_ships[ship_name]
    r_ship = r_ships[ship_name]

    o_id = o_ship[component_type]
    r_id = r_ship[component_type]

    # fail if component ID changed
    if o_id != r_id:
        pytest.fail(
            f"\n[{ship_name}] {component_type.upper()} was changed:\n"
            f"  Was: {o_id}\n"
            f"  Now: {r_id}"
        )

    # Compare component parameters if ID is the same
    orig_data = {
        "weapon": o_weapons,
        "hull": o_hulls,
        "engine": o_engines
    }[component_type][o_id]

    rand_data = {
        "weapon": r_weapons,
        "hull": r_hulls,
        "engine": r_engines
    }[component_type][r_id]

    for key in orig_data:
        if key == component_type:
            continue
        if orig_data[key] != rand_data[key]:
            pytest.fail(
                f"\n[{ship_name}] Parameter '{key}' in {component_type.upper()} was changed:\n"
                f"  Was: {orig_data[key]}\n"
                f"  Now: {rand_data[key]}"
            )
