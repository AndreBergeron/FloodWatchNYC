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

def DownloadCensusData():
    """
    Downloads census data from the US Census Bureau API and saves it to a specified directory.
    """
    try:
        # Define the URL for the census data
        url = "https://api.census.gov/data/2020/dec/pl?get=NAME,P1_001N&for=state:*"
        
        # Make a request to the API
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        
        # Parse the JSON response
        data = response.json()
        
        # Convert to DataFrame
        df = pd.DataFrame(data[1:], columns=data[0])
        
        # Save to CSV
        output_path = os.path.join(CENSUS_DATA_PATH, "census_data.csv")
        df.to_csv(output_path, index=False)
        
        logger.SetupLogging(f"Census data downloaded and saved to {output_path}")
    
    except Exception as e:
        logger.SetupLogging(f"Error downloading census data: {e}")

def DownloadACSData():
    """
    Downloads American Community Survey (ACS) data from the US Census Bureau API and saves it to a specified directory.
    """
    try:
        # Define the URL for the ACS data
        url = "https://api.census.gov/data/2020/acs/acs5?get=NAME,B01001_001E&for=state:*"
        
        # Make a request to the API
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        
        # Parse the JSON response
        data = response.json()
        
        # Convert to DataFrame
        df = pd.DataFrame(data[1:], columns=data[0])
        
        # Save to CSV
        output_path = os.path.join(CENSUS_DATA_PATH, "acs_data.csv")
        df.to_csv(output_path, index=False)
        
        logger.SetupLogging(f"ACS data downloaded and saved to {output_path}")
    
    except Exception as e:
        logger.SetupLogging(f"Error downloading ACS data: {e}")