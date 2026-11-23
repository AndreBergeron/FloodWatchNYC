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
from pathlib import Path
import logger

CENSUS_DATA_PATH = os.environ["CENSUS_DATA_PATH"]
GDB = os.environ["GDB"]
sScriptName = sys.argv[0]

arcpy.env.workspace = os.getcwd()
arcpy.env.overwriteOutput = True
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(4326)

BASE = "https://rockyweb.usgs.gov/vdelivery/Datasets/Staged/Elevation/13/TIFF/current"
TILES = ["n41w074", "n41w075"]          # covers most of NYC plus Staten Island
OUT_DIR = Path(r"C:\fw\raw\usgs")       # keep this path short


def download_file(url, dest, timeout=300):
    """Stream a file to disk, skipping it if it's already complete."""
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)

    with requests.get(url, stream=True, timeout=timeout) as r:
        r.raise_for_status()
        expected = int(r.headers.get("Content-Length", 0))

        if dest.exists() and expected and dest.stat().st_size == expected:
            print(f"Skipping (already complete): {dest.name}")
            return dest

        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                f.write(chunk)

    size = dest.stat().st_size
    if expected and size != expected:
        raise RuntimeError(f"{dest.name}: got {size} bytes, expected {expected}")
    print(f"Downloaded {dest.name} ({size / 1e6:.1f} MB)")
    return dest


def download_usgs_dem():
    for tile in TILES:
        # The folder and the file name must use the same tile code
        for ext in ("tif", "xml"):                 # xml = metadata for your catalog
            url = f"{BASE}/{tile}/USGS_13_{tile}.{ext}"
            download_file(url, OUT_DIR / f"USGS_13_{tile}.{ext}")


if __name__ == "__main__":
    download_usgs_dem()