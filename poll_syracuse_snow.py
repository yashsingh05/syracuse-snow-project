"""
poll_syracuse_snow.py
Snapshots the Syracuse Winter Operations snow route layer on each run.
Designed to be run on a schedule (e.g. GitHub Actions cron) throughout winter.
"""

import requests
import json
import os
from datetime import datetime, timezone

BASE_URL = "https://services6.arcgis.com/bdPqSfflsdgFRVVM/arcgis/rest/services/Winter_Operations_Snow_Routes/FeatureServer/0/query"

OUTPUT_DIR = "data/raw"


def fetch_all_features():
    """Pull every segment from the feature service, paginating automatically."""
    all_features = []
    offset = 0
    page_size = 2000  # ArcGIS servers commonly cap around 2000/request

    while True:
        params = {
            "where": "1=1",
            "outFields": "*",
            "f": "json",
            "resultOffset": offset,
            "resultRecordCount": page_size,
        }
        resp = requests.get(BASE_URL, params=params, timeout=30)
        resp.raise_for_status()
        payload = resp.json()

        if "error" in payload:
            raise RuntimeError(f"ArcGIS API error: {payload['error']}")

        features = payload.get("features", [])
        all_features.extend(features)

        # Stop when the server gives us fewer than a full page
        if len(features) < page_size:
            break
        offset += page_size

    return all_features


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    features = fetch_all_features()

    snapshot = {
        "polled_at_utc": timestamp,
        "source": BASE_URL,
        "feature_count": len(features),
        "features": features,
    }

    out_path = os.path.join(OUTPUT_DIR, f"snow_routes_{timestamp}.json")
    with open(out_path, "w") as f:
        json.dump(snapshot, f)

    print(f"Saved {len(features)} segments to {out_path}")


if __name__ == "__main__":
    main()