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

DATAPATH = os.environ["DATAPATH"]
CENSUS_DATA_PATH = os.path.join(DATAPATH, "raw", "census", "2020_Census_Tracts_20261121.geojson")
GDB = os.environ["GDB"]

sScriptName = sys.argv[0]

arcpy.env.workspace = os.getcwd()
arcpy.env.overwriteOutput = True
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(2263)
arcpy.env.outputZFlag = "Disabled"

def ProcessCensusData():
    """
    Process census data.
    """
    try: 
        logger.SetupLogging("\tStarting census data processing.")
        for root, dirs, files in os.walk(DATAPATH):
                for dir in dirs:
                    if dir.startswith("raw"):
                        data_path = os.path.join(root, dir)
                        sCensusDataPath = os.path.join(data_path, "tiger_tracts") 
                        sEvacuationPaths = os.path.join(data_path, "nycem")

                        for file in glob.glob(os.path.join(sCensusDataPath, "*.geojson")):
                            if "2020_Census_Tracts" in file:
                                sGeojsonPath = file
                                logger.SetupLogging(f"\tFound census geojson file: {sGeojsonPath}")
                                break
                        sEvacuationZonesGeojsonPath = None
                        sEvacuationCentersGeojsonPath = None
                        for file in glob.glob(os.path.join(sEvacuationPaths, "*.geojson")):
                            if "Hurricane_Evacuation_Zones" in file:
                                sEvacuationZonesGeojsonPath = file
                                logger.SetupLogging(f"\tFound evacuation zones geojson file: {sEvacuationZonesGeojsonPath}")
                            elif "Hurricane_Evacuation_Centers" in file:
                                sEvacuationCentersGeojsonPath = file
                                logger.SetupLogging(f"\tFound evacuation centers geojson file: {sEvacuationCentersGeojsonPath}")
                            if sEvacuationZonesGeojsonPath and sEvacuationCentersGeojsonPath:
                                break

        sOutputFeatureClasspath = os.path.join(GDB, "Census_Tracts")
        arcpy.JSONToFeatures_conversion(sGeojsonPath, sOutputFeatureClasspath, "POLYGON")
        arcpy.MakeFeatureLayer_management(sOutputFeatureClasspath, "NYC_Census_Tracts_Layer")
        logger.SetupLogging(f"\tOutput feature class path: {sOutputFeatureClasspath}")

        sOutputFeatureClasspathEvac = os.path.join(GDB, "Evacuation_Zones")
        arcpy.JSONToFeatures_conversion(sEvacuationZonesGeojsonPath, sOutputFeatureClasspathEvac, "POLYGON")
        arcpy.MakeFeatureLayer_management(sOutputFeatureClasspathEvac, "NYC_Evacuation_Zones_Layer")
        logger.SetupLogging(f"\tOutput feature class path: {sOutputFeatureClasspathEvac}")

        sOutputFeatureClasspathEvac = os.path.join(GDB, "Evacuation_Centers")
        arcpy.JSONToFeatures_conversion(sEvacuationCentersGeojsonPath, sOutputFeatureClasspathEvac, "POINT")
        arcpy.MakeFeatureLayer_management(sOutputFeatureClasspathEvac, "NYC_Evacuation_Centers_Layer")
        logger.SetupLogging(f"\tOutput feature class path: {sOutputFeatureClasspathEvac}")

        sCsvPath = os.path.join(DATAPATH, "raw", "census", "census_data.csv")
        sCensusTablePath = os.path.join(GDB, "Census_Data")

        arcpy.conversion.TableToTable(sCsvPath, GDB, "Census_Data")
        arcpy.management.AddField(sCensusTablePath, "GEOID_TEXT", "TEXT", field_length=11)
        arcpy.management.CalculateField(sCensusTablePath, "GEOID_TEXT", "str(!GEOID!).zfill(11)", "PYTHON3")

        arcpy.management.AddJoin(
            in_layer_or_view="NYC_Census_Tracts_Layer",
            in_field="geoid",
            join_table=sCensusTablePath,
            join_field="GEOID_TEXT",
            join_type="KEEP_ALL"
        )

        sOutputJoinedFeatureClass = os.path.join(GDB, "Census_Tracts_Joined")
        arcpy.management.CopyFeatures("NYC_Census_Tracts_Layer", sOutputJoinedFeatureClass)
        logger.SetupLogging(f"\tJoined feature class created: {sOutputJoinedFeatureClass}")
    
    except Exception as e:
        logger.SetupLogging(f"\t ERROR: {e}")
        raise

    return None

if __name__ == "__main__":
    ProcessCensusData()