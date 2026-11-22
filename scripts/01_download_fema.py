import sys
import os
import uuid
import glob
import re
import arcpy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import requests
import logger
import json
import time
from pathlib import Path

import requests
CENSUS_DATA_PATH = os.environ["CENSUS_DATA_PATH"]
GDB = os.environ["GDB"]
sScriptName = sys.argv[0]

arcpy.env.workspace = os.getcwd()
arcpy.env.overwriteOutput = True
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(4326)

"""Download FEMA NFHL Flood Hazard Zones (layer 28) for NYC via the REST service."""

LAYER_URL = "https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer/28"

# (xmin, ymin, xmax, ymax) in WGS84 longitude/latitude
NYC_BBOX = (-74.30, 40.47, -73.68, 40.93)
TEST_BBOX = (-74.02, 40.565, -73.96, 40.60)   # roughly Coney Island, a coastal test area

OUT_FIELDS = "FLD_ZONE,ZONE_SUBTY,SFHA_TF,STATIC_BFE,DFIRM_ID"
PAGE_SIZE = 500          # keep small: FEMA warns that big requests can fail
MAX_RETRIES = 4
TIMEOUT = 180            # seconds per request


def get_json(url, params):
    """GET with retries. Raises if FEMA returns an error message."""
    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(url, params=params, timeout=TIMEOUT)
            resp.raise_for_status()
            payload = resp.json()
            if "error" in payload:
                raise RuntimeError(payload["error"])
            return payload
        except (requests.RequestException, ValueError, RuntimeError) as exc:
            last_error = exc
            wait = 5 * attempt
            print(f"  attempt {attempt} failed ({exc}); retrying in {wait}s")
            time.sleep(wait)
    raise RuntimeError(f"Request failed after {MAX_RETRIES} attempts: {last_error}")


def download_flood_zones(bbox, out_path, max_pages=None):
    """Page through layer 28 inside bbox and save one GeoJSON file.

    max_pages limits how many pages to fetch (use it for tests).
    """
    xmin, ymin, xmax, ymax = bbox
    params = {
        "where": "1=1",
        "geometry": f"{xmin},{ymin},{xmax},{ymax}",
        "geometryType": "esriGeometryEnvelope",
        "inSR": 4326,
        "spatialRel": "esriSpatialRelIntersects",
        "outFields": OUT_FIELDS,
        "outSR": 4326,
        "orderByFields": "OBJECTID",     # stable order so pages don't overlap
        "resultRecordCount": PAGE_SIZE,
        "f": "geojson",
    }

    features, offset, page = [], 0, 0
    while True:
        params["resultOffset"] = offset
        payload = get_json(f"{LAYER_URL}/query", params)
        batch = payload.get("features", [])
        features.extend(batch)
        page += 1
        print(f"page {page}: +{len(batch)} (total {len(features)})")

        if len(batch) < PAGE_SIZE:       # short page means we're done
            break
        if max_pages and page >= max_pages:
            print("Stopped early (max_pages reached)")
            break
        offset += len(batch)
        time.sleep(1)                    # be polite to the server

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump({"type": "FeatureCollection", "features": features}, fh)
    print(f"Saved {len(features)} features -> {out_path}")
    return len(features)


if __name__ == "__main__":
    # STEP 1: run this alone first.
    download_flood_zones(TEST_BBOX, r"C:\fw\fema_test.geojson", max_pages=2)

    # STEP 2: once the test works, comment out step 1 and run this instead.
    # download_flood_zones(NYC_BBOX, r"C:\fw\fema_nyc.geojson")