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
import zipfile
import io

DATAPATH = os.environ["DATAPATH"]
CENSUS_DATA_PATH = os.path.join(DATAPATH, "raw", "census")
CENSUS_API_KEY = os.environ["CENSUS_API_KEY"]
GDB = os.environ["GDB"]
sScriptName = sys.argv[0]

arcpy.env.workspace = os.getcwd()
arcpy.env.overwriteOutput = True
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(4326)

def DownloadCensusData():
    """
    Downloads census data from the US Census Bureau API and saves it to a specified directory.
    """
    try:
        logger.SetupLogging("\tStarting census data download process.")
        # Define the URL for the census data
        url = "https://api.census.gov/data/2024/acs/acs5"

        listCounties = ["005", "047", "061", "081", "085"]
        listAcsVariables = [
            "NAME",
            "B01003_001E",  # Total population estimate
            "B01003_001M",  # Total population MOE
            "B19013_001E",  # Median household income estimate
            "B19013_001M",  # Median household income MOE
            "B17001_002E",  # Population below poverty level estimate
            "B17001_002M",  # Population below poverty level MOE
            "B15003_022E",  # Bachelor's degree estimate
            "B15003_022M",  # Bachelor's degree MOE
            "B15003_023E",  # Master's degree estimate
            "B15003_023M",  # Master's degree MOE
            "B15003_025E",  # Doctoral degree estimate
            "B15003_025M",  # Doctoral degree MOE
            "B23025_004E",  # Civilian employed population estimate
            "B23025_004M",  # Civilian employed population MOE
            "B25003_002E",  # Owner-occupied housing units estimate
            "B25003_002M",  # Owner-occupied housing units MOE
            "B25003_003E",  # Renter-occupied housing units estimate
            "B25003_003M",  # Renter-occupied housing units MOE
            "B25001_001E",  # Total housing units estimate
            "B25001_001M",  # Total housing units MOE
        ]
        rows = []

        for county in listCounties:
            params = {
                "get": ",".join(listAcsVariables),
                "for": "tract:*",
                "in": f"state:36 county:{county}",
                "key": CENSUS_API_KEY,
                }
            # Make a request to the API
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()
            header = data[0]
            rows.extend(data[1:])
        
        # Convert to DataFrame
        df = pd.DataFrame(rows, columns=header)
        df.rename(columns={
            "B01003_001E": "Total_Population_Estimate",
            "B01003_001M": "Total_Population_MOE",
            "B19013_001E": "Median_Household_Income_Estimate",
            "B19013_001M": "Median_Household_Income_MOE",
            "B17001_002E": "Population_Below_Poverty_Level_Estimate",
            "B17001_002M": "Population_Below_Poverty_Level_MOE",
            "B15003_022E": "Bachelors_Degree_Estimate",
            "B15003_022M": "Bachelors_Degree_MOE",
            "B15003_023E": "Masters_Degree_Estimate",
            "B15003_023M": "Masters_Degree_MOE",
            "B15003_025E": "Doctoral_Degree_Estimate",
            "B15003_025M": "Doctoral_Degree_MOE",
            "B23025_004E": "Civilian_Employed_Population_Estimate",
            "B23025_004M": "Civilian_Employed_Population_MOE",
            "B25003_002E": "Owner_Occupied_Housing_Units_Estimate",
            "B25003_002M": "Owner_Occupied_Housing_Units_MOE",
            "B25003_003E": "Renter_Occupied_Housing_Units_Estimate",
            "B25003_003M": "Renter_Occupied_Housing_Units_MOE",
            "B25001_001E": "Total_Housing_Units_Estimate",
            "B25001_001M": "Total_Housing_Units_MOE"
        }, inplace=True)

        df["GEOID"] = df["state"] + df["county"] + df["tract"]
        counties = df["county"].value_counts()
        logger.SetupLogging(f"\tDownloaded census data for counties: {', '.join(counties.index)} with counts: {', '.join(map(str, counties.values))}")

        # Save to CSV
        output_path = os.path.join(CENSUS_DATA_PATH, "census_data.csv")
        df.to_csv(output_path, index=False)
        
        logger.SetupLogging(f"\tCensus data downloaded and saved to {output_path}")
    
    except Exception as e:
        logger.SetupLogging(f"Error downloading census data: {e}")
        raise

if __name__ == "__main__":
    DownloadCensusData()