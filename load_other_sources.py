"""
load_other_sources.py
Loads SYRCityline snow complaints and Syracuse neighborhood boundaries into DuckDB.
"""

import duckdb
import requests
import json as jsonlib

con = duckdb.connect("syracuse_snow.duckdb")


def fetch_all(base_url, where="1=1"):
    all_features = []
    offset = 0
    page_size = 2000
    while True:
        params = {
            "where": where,
            "outFields": "*",
            "f": "json",
            "resultOffset": offset,
            "resultRecordCount": page_size,
        }
        resp = requests.get(base_url, params=params, timeout=30)
        resp.raise_for_status()
        payload = resp.json()
        features = payload.get("features", [])
        all_features.extend(features)
        if len(features) < page_size:
            break
        offset += page_size
    return all_features


def load_cityline_requests():
    url = "https://services6.arcgis.com/bdPqSfflsdgFRVVM/arcgis/rest/services/SYRCityline_Requests_2021_Present/FeatureServer/0/query"
    features = fetch_all(url, where="Category='Snow & Ice'")

    con.execute("""
        CREATE OR REPLACE TABLE raw_cityline_requests (
            id VARCHAR,
            summary VARCHAR,
            rating VARCHAR,
            address VARCHAR,
            category VARCHAR,
            created_at_local VARCHAR,
            acknowledged_at_local VARCHAR,
            closed_at_local VARCHAR,
            minutes_to_acknowledge DOUBLE,
            minutes_to_close VARCHAR,
            sla_in_hours DOUBLE,
            report_source VARCHAR,
            lat DOUBLE,
            lng DOUBLE
        )
    """)

    rows = []
    for f in features:
        a = f["attributes"]
        rows.append((
            a.get("Id"),
            a.get("Summary"),
            a.get("Rating"),
            a.get("Address"),
            a.get("Category"),
            a.get("Created_at_local"),
            a.get("Acknowledged_at_local"),
            a.get("Closed_at_local"),
            a.get("Minutes_to_Acknowledge"),
            a.get("Minutes_to_Close"),
            a.get("Sla_in_hours"),
            a.get("Report_Source"),
            a.get("Lat"),
            a.get("Lng"),
        ))

    con.executemany(
        "INSERT INTO raw_cityline_requests VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        rows
    )
    print(f"Loaded {len(rows)} cityline snow complaints")


def load_neighborhoods():
    url = "https://services6.arcgis.com/bdPqSfflsdgFRVVM/arcgis/rest/services/Syracuse_Neighborhoods/FeatureServer/0/query"
    features = fetch_all(url)

    con.execute("""
        CREATE OR REPLACE TABLE raw_neighborhoods (
            fid BIGINT,
            name VARCHAR,
            geometry_wkt VARCHAR
        )
    """)

    rows = []
    for f in features:
        a = f["attributes"]
        geom = f.get("geometry", {})
        rings = geom.get("rings", [])

        ring_strs = []
        for ring in rings:
            coord_strs = [f"{x} {y}" for x, y in ring]
            ring_strs.append("(" + ", ".join(coord_strs) + ")")

        wkt = "POLYGON(" + ", ".join(ring_strs) + ")"
        rows.append((a.get("FID"), a.get("Name"), wkt))

    con.executemany("INSERT INTO raw_neighborhoods VALUES (?, ?, ?)", rows)
    print(f"Loaded {len(rows)} neighborhoods")
if __name__ == "__main__":
    load_cityline_requests()
    load_neighborhoods()
    con.close()