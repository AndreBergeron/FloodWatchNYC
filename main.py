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
from importlib import import_module

DATAPATH = os.environ["DATAPATH"]
GDB = os.environ["GDB"]
sScriptName = sys.argv[0]

if not DATAPATH or not os.path.isdir(DATAPATH):
    raise FileNotFoundError("DATAPATH is missing or invalid")

if not GDB or not arcpy.Exists(GDB):
    raise FileNotFoundError("GDB is missing or does not exist")

def InitiateProcess():
    """
    Initiates the FloodWatchNYC process by downloading and processing census data.
    """
    try: 
        logger.SetupLogging("Starting the FloodWatchNYC process")
        census_module = import_module("scripts.04_download_census")
        prepare_datasets_module = import_module("scripts.06_prepare_datasets")
        census_module.DownloadCensusData()
        prepare_datasets_module.ProcessCensusData()
        # for root, dirs, files in os.walk(arcpy.env.workspace):
        #         for dir in dirs:
        #             if dir.startswith("scripts"):
        #                 script_path = os.path.join(root, dir)
        #                 sys.path.append(script_path)
        #                 for script_file in glob.glob(os.path.join(script_path, "*.py")):
        #                     script_name = os.path.splitext(os.path.basename(script_file))[0]
        #                     if script_name != "04_download_census":
        #                         module = import_module(f"scripts.{script_name}")
        #                         if hasattr(module, "ProcessCensusData"):
        #                             module.ProcessCensusData()

        logger.SetupLogging("Finished the FloodWatchNYC process")
    except Exception as e:
        logger.SetupLogging(f"\t ERROR: {e}")
        raise

    return

if __name__ == "__main__":
    InitiateProcess()