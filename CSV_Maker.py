# csv export of pertantent data for discriminent analysis.  
# Working with CSV files makes life easier when working with R, or Excel.
# EVC, EVH, and (eventually), EVT are Landfire datasets (%cover, height and type), rasters are reprojected and 
# exported in arcGIS. I use NAD83.
# HLN is the number for the hydrologic landscape number.  Dataset available through USGS, read the metadata for details.
# Stream order is currently part of the NHDPlus dataset. 
# avgSlope is the slope over the length of the streamline.  ((MaxZ-MinZ)/L)
# Currently this utilizes NHD Medium Resolution data, if exploratory analysis proves to be fruitful it will be modified
# for NHD HiRes.

import arcpy
import csv

FeatureClass =r'D:\GIS\UCRB\workingGDB.gdb\NHD1406_data'
DEM = r'D:\GIS\UCRB\workingGDB.gdb\BigAssDEM'
EVCa = r'D:\GIS\UCRB\workingGDB.gdb\EVC_ProjectRaster'
EVHa = r'D:\GIS\UCRB\workingGDB.gdb\EVH_ProjectRaster'
HLNa = r'D:\GIS\UCRB\workingGDB.gdb\HLR'
FCOutput = FeatureClass+"PT"
workspace = r'D:\GIS\UCRB\workingGDB.gdb'
Spatial_Ref = arcpy.Describe(FeatureClass).spatialReference
arcpy.FeatureToPoint_management(FeatureClass, FCOutput, "INSIDE")
arcpy.AddXY_management(FCOutput)

# A large number of functions to pull values from rasters
def GetElev (x, y):
    z = arcpy.GetCellValue_management(DEM, x+' '+y,"1")
    z = str(z)
    z = float(z)
    return z

def GetEVC (x, y):
    EVC = arcpy.GetCellValue_management(EVCa, x+' '+y,"1")
    EVC = str(EVC)
    EVC = int(EVC)
    return EVC

def GetEVH (x, y):
    EVH = arcpy.GetCellValue_management(EVHa, x+' '+y,"1")
    EVH = str(EVH)
    EVH = int(EVH)
    return EVH

def GetHLN (x, y):
    HLN = arcpy.GetCellValue_management(HLNa, x+' '+y,"1")
    HLN = str(HLN)
    HLN = int(HLN)
    return HLN


#Fields for the CSV file and writer object creation
Fields = ['PermID','x', 'y','z','order', 'slope','EVC','EVH','HLN']

wtr = csv.writer(open("D:\TestCSV.csv", "wb"))
wtr.writerow(Fields)

rows = arcpy.SearchCursor(FCOutput)
for row in rows:
     PermID = row.getValue("Permanent_Identifier")
     x = str(row.getValue("POINT_X"))
     y = str(row.getValue("POINT_Y"))
     z = GetElev(x, y)
     StreamOrder = row.getValue("StreamOrde")
     slope = row.getValue("avgSlope")
     EVC = GetEVC(x, y)
     EVH = GetEVH(x, y)
     HLN = GetHLN(x, y)
     RowLine = [PermID, x, y, z, StreamOrder, slope, EVC, EVH, HLN]
     wtr.writerow(RowLine)
     del row
del rows
del wtr
