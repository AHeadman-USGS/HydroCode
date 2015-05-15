# csv export of pertantent data for discriminent analysis.  
# Working with CSV files makes life easier when working with R, or Excel.
# EVC, EVH, and (eventually), EVT are Landfire datasets (%cover, height and type), rasters are reprojected and 
# exported in arcGIS. I use NAD83.
# HLN is the number for the hydrologic landscape number.  Dataset available through USGS, read the metadata for details.
# Upstream Sq KM is currently part of the NHDPlus dataset. 
# avgSlope is the slope over the length of the streamline.  ((MaxZ-MinZ)/L)
# Currently this utilizes NHD Medium Resolution data, if exploratory analysis proves to be fruitful it will be modified
# for NHD HiRes.

import arcpy
import csv
import traceback

FeatureClass =r'D:\GIS\UCRB\workingGDB.gdb\NHD1406_data'
DEM = r'D:\GIS\UCRB\workingGDB.gdb\BigAssDEM'
EVCa = r'D:\GIS\UCRB\workingGDB.gdb\EVC_ProjectRaster'
EVHa = r'D:\GIS\UCRB\workingGDB.gdb\EVH_ProjectRaster'
HLNa = r'D:\GIS\UCRB\workingGDB.gdb\HLR'
ASPa = r'D:\GIS\UCRB\workingGDB.gdb\Aspect_BigAssDEM'
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

def GetASP (x, y):
    ASP = arcpy.GetCellValue_management(ASPa, x+' '+y,"1")
    ASP = str(ASP)
    ASP = float(ASP)
    return ASP


#Fields for the CSV file and writer object creation
Fields = ['PermID', 'FType','x', 'y','z','UpStream', 'slope', 'aspect','EVC','EVH','HLN']

wtr = csv.writer(open("D:\TestCSV.csv", "wb"))
wtr.writerow(Fields)
shitlist = []

rows = arcpy.SearchCursor(FCOutput)
for row in rows:
    try:
         PermID = row.getValue("Permanent_Identifier")
         Ftype = row.getValue("FType")
         x = str(row.getValue("POINT_X"))
         y = str(row.getValue("POINT_Y"))
         z = GetElev(x, y)
         Upstream = row.getValue("DIVDASQKM_12")
         slope = row.getValue("avgSlope")
         aspect = GetASP(x, y)
         EVC = GetEVC(x, y)
         EVH = GetEVH(x, y)
         HLN = GetHLN(x, y)
         RowLine = [PermID, Ftype, x, y, z, Upstream, slope, aspect, EVC, EVH, HLN]
         wtr.writerow(RowLine)
         del row
    except:
        shitlist.append([x, y])
        print "Something wrong at "+x+", "+y+". Here, have a traceback:"
        traceback.print_exc()
        del row
        continue
del rows
del wtr
print shitlist
