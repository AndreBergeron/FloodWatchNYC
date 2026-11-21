@echo off

@REM  @SET "DATAPATH=C:\Users\lberg\OneDrive\Desktop\InterviewPrep\FloodWatchNYC\data\"

@SET "CENSUS_DATA_PATH=C:\Users\lberg\OneDrive\Desktop\InterviewPrep\FloodWatchNYC\data\census_data"
@SET "GDB=C:\Users\lberg\OneDrive\Desktop\InterviewPrep\FloodWatchNYC\ArcFloodWatchNYC\FloodWatchNYC.gdb"

@"C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" "C:\Users\lberg\OneDrive\Desktop\InterviewPrep\FloodWatchNYC\main.py"
    
pause