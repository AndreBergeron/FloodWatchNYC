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