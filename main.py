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
GDB = os.environ["GDB"]
sScriptName = sys.argv[0]

if not DATAPATH or not os.path.isdir(DATAPATH):
    raise FileNotFoundError("DATAPATH is missing or invalid")

if not GDB or not arcpy.Exists(GDB):
    raise FileNotFoundError("GDB is missing or does not exist")

arcpy.env.workspace = os.getcwd()
arcpy.env.overwriteOutput = True
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(4326)

def InitiateProcess():

    logger.SetupLogging("\t\t This is a test")
    
    logger.SetupLogging("\t\t This is a test")
    return

InitiateProcess()