import duckdb
import json
import glob

con = duckdb.connect("syracuse_snow.duckdb")

con.execute("""
    CREATE TABLE IF NOT EXISTS raw_snow_routes (
        snapshot_file VARCHAR,
        polled_at_utc VARCHAR,
        objectid BIGINT,
        roadname VARCHAR,
        routepriority VARCHAR,
        snowroutesegmentid VARCHAR,
        servicestatus VARCHAR,
        lastserviced BIGINT,
        passes DOUBLE,
        eventid VARCHAR,
        geometry_wkt VARCHAR
    )
""")

def paths_to_wkt(geometry):
    if not geometry or "paths" not in geometry:
        return None
    lines = []
    for path in geometry["paths"]:
        coord_strs = [f"{x} {y}" for x, y in path]
        lines.append("(" + ", ".join(coord_strs) + ")")
    return "MULTILINESTRING(" + ", ".join(lines) + ")"

for filepath in glob.glob("data/raw/snow_routes_*.json"):
    with open(filepath) as f:
        data = json.load(f)

    polled_at = data["polled_at_utc"]

    rows = []
    for feature in data["features"]:
        attrs = feature["attributes"]
        geom_wkt = paths_to_wkt(feature.get("geometry"))
        rows.append((
            filepath,
            polled_at,
            attrs.get("OBJECTID"),
            attrs.get("roadname"),
            attrs.get("routepriority"),
            attrs.get("snowroutesegmentid"),
            attrs.get("servicestatus"),
            attrs.get("lastserviced"),
            attrs.get("passes"),
            attrs.get("eventid"),
            geom_wkt,
        ))

    con.executemany(
        "INSERT INTO raw_snow_routes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        rows
    )
    print(f"Loaded {len(rows)} rows from {filepath}")

con.close()