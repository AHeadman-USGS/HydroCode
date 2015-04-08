## This initial script sorts points associated with the streamlines
## Estimates put this at about 80% accuracy.  These are broad qual/quant factors
## intended to provide an initial product while more data is gathered.
## This script utilizes products from Utah State University, USGS and the NHDPlus program.
## Currently this script is stand alone, requiring arcpy capabilities for ArcGIS 10.1 or later.

import arcpy

# Defining some variables
# Flowlines need the title "NHDFlowline" currently

FeatureClass =r'D:\GIS\UCRB\1406.gdb\NHDFlowline'
DEM = r'D:\GIS\UCRB\1406.gdb\FullDEM_Two'
FCOutput = FeatureClass+"PT"
FCOutputUTM = FCOutput+"UTM"
workspace = r'D:\GIS\UCRB\1406.gdb'
template = r'D:\GIS\UCRB\1406.gdb\ptstemplate'
arcpy.env.workspace = workspace
PerPts = FeatureClass+"PerPts"
IntPts = FeatureClass+"IntPts"
EphPts = FeatureClass+"EphPts"
Spatial_Ref = arcpy.Describe(FeatureClass).spatialReference
arcpy.env.workspace = workspace
ValBot = r'D:\GIS\UCRB\1406.gdb\ValleyBottom_'
Rip60 = r'D:\GIS\UCRB\1406.gdb\ZonalSt_Diss1_ProjectRaster'

# defining the sorting functions

def EphmPts (A, B, C, D, E):
    pic = arcpy.InsertCursor(EphPts)
    pc = pic.newRow()
    pc.setValue("X", A)
    pc.setValue("Y", B)
    pc.setValue("Z", C)
    pc.setValue("PERM_ID", D)
    pc.setValue("GNIS", E)
    pic.insertRow(pc)
    del pic

def IntmPts (A, B, C, D, E):
    pic = arcpy.InsertCursor(IntPts)
    pc = pic.newRow()
    pc.setValue("X", A)
    pc.setValue("Y", B)
    pc.setValue("Z", C)
    pc.setValue("PERM_ID", D)
    pc.setValue("GNIS", E)
    pic.insertRow(pc)
    del pic

def PernPts (A, B, C, D, E):
    pic = arcpy.InsertCursor(PerPts)
    pc = pic.newRow()
    pc.setValue("X", A)
    pc.setValue("Y", B)
    pc.setValue("Z", C)
    pc.setValue("PERM_ID", D)
    pc.setValue("GNIS", E)
    pic.insertRow(pc)
    del pic

# Creation of the feature classes
arcpy.CreateFeatureclass_management(workspace, "NHDFlowlinePerPts", "POINT", template, "SAME_AS_TEMPLATE", "SAME_AS_TEMPLATE", Spatial_Ref)
arcpy.CreateFeatureclass_management(workspace, "NHDFlowlineIntPts", "POINT", template, "SAME_AS_TEMPLATE", "SAME_AS_TEMPLATE", Spatial_Ref)
arcpy.CreateFeatureclass_management(workspace, "NHDFlowlineEphPts", "POINT", template, "SAME_AS_TEMPLATE", "SAME_AS_TEMPLATE", Spatial_Ref)
arcpy.FeatureToPoint_management(FeatureClass, FCOutput, "INSIDE")
arcpy.AddXY_management(FCOutput)

# Uncomment the following lines if there is descrepency between of projected vs. geographic data between the DEM and Flowlines

# arcpy.ConvertCoordinateNotation_management(FCOutput, FCOutputUTM, "X", "Y", "DD_2", "UTM")
rows = arcpy.SearchCursor(FCOutput)             #Change to FCOuputUTM if applicable
for row in rows:
    x = str(row.getValue("POINT_X"))
    y = str(row.getValue("POINT_Y"))
    #UTMPass = row.getValue("UTM")
    #UTMCoord = UTMPass[4:]
    StreamOrder = row.getValue("ST_ORDER")
    PermID = row.getValue("PERMANENT_IDENTIFIER")
    FCode = row.getValue("FCode")
    DEMValuePassA = arcpy.GetCellValue_management(DEM, x+' '+y,"1")   #Change to UTMCoord if applicable
    DEMValuePassB = str(DEMValuePassA)
    DEMValue = float(DEMValuePassB)
    ValBotPassA = arcpy.GetCellValue_management(ValBot, x+' '+y,"1")
    ValBotPassB = str(ValBotPassA)
    if ValBotPassB == 'NoData':
        ValBotValue = ValBotPassB
    else:
        ValBotValue = int(ValBotPassB)
    RipDataPassA = arcpy.GetCellValue_management(Rip60, x+' '+y,"1")
    RipDataPassB = str(RipDataPassA)
    if RipDataPassB == 'NoData':
        RipValue = 0.0
    else:
        RipValue = float(RipDataPassB)
    GNIS = row.getValue("NHDFlowline_GNIS_Name")
    if GNIS is not None:
        GN = 1
    else:
        GNIS = row.getValue("NHDFlowline_GNIS_Name_1")
        if GNIS is not None:
            GN = 1
        else:
            GN = 0
    erom = row.getValue("EROMJanCFS")


# The following results from DEMValue are based on Natural Breaks (Jenks optimization) in the 10m DEM.
    if ValBotValue == 1:
        if StreamOrder > 2:
            PernPts(x, y, DEMValue, PermID, GN)
        else:
            EphmPts(x, y, DEMValue, PermID, GN)
    if FCode == 46006:
        if StreamOrder > 1:
            PernPts(x, y, DEMValue, PermID, GN)
        else:
            EphmPts(x, y, DEMValue, PermID, GN)
    if FCode == 46007:
        EphmPts(x, y, DEMValue, PermID, GN)
    if erom is not None and erom > 10:
        PernPts(x, y, DEMValue, PermID, GN)
    else:
        if DEMValue >= 2010:
            if StreamOrder >= 3:
                if RipValue > 0.275:
                    PernPts(x, y, DEMValue, PermID, GN)
                else:
                    IntmPts(x, y, DEMValue, PermID, GN)
            if StreamOrder == 2:
               if RipValue >= 0.6:
                    PernPts(x, y, DEMValue, PermID, GN)
               if RipValue > 0.4 and RipValue < 0.6:
                    IntmPts(x, y, DEMValue, PermID, GN)
               else:
                    EphmPts(x, y, DEMValue, PermID, GN)
            if StreamOrder < 2:
                EphmPts(x, y, DEMValue, PermID, GN)
        if DEMValue < 2010 and DEMValue >= 1642:
            if StreamOrder > 5:
                PernPts(x, y, DEMValue, PermID, GN)
            if StreamOrder == 4 or StreamOrder == 5:
                if RipValue > 0.275:
                    PernPts(x, y, DEMValue, PermID, GN)
                else:
                    IntmPts(x, y, DEMValue, PermID, GN)
            if StreamOrder == 3:
                IntmPts(x, y, DEMValue, PermID, GN)
                if RipValue >= 0.6:
                    PernPts(x, y, DEMValue, PermID, GN)
                if RipValue > 0.4 and RipValue < 0.6:
                    IntmPts(x, y, DEMValue, PermID, GN)
                else:
                    EphmPts(x, y, DEMValue, PermID, GN)
            if StreamOrder < 3:
                EphmPts(x, y, DEMValue, PermID, GN)

        if DEMValue < 1642 and DEMValue >= 1462:
            if StreamOrder > 5:
                PernPts(x, y, DEMValue, PermID, GN)
            if StreamOrder == 5:
                if RipValue > 0.275:
                    PernPts(x, y, DEMValue, PermID, GN)
                else:
                    IntmPts(x, y, DEMValue, PermID, GN)
            if StreamOrder == 4:
                if RipValue >= 0.6:
                    PernPts(x, y, DEMValue, PermID, GN)
                if RipValue > 0.275 and RipValue < 0.6:
                    IntmPts(x, y, DEMValue, PermID, GN)
                else:
                    EphmPts(x, y, DEMValue, PermID, GN)
            if StreamOrder == 3:
                if RipValue > 0.275:
                    IntmPts(x, y, DEMValue, PermID, GN)
                else:
                    EphmPts(x, y, DEMValue, PermID, GN)
            if StreamOrder < 3:
                EphmPts(x, y, DEMValue, PermID, GN)


        if DEMValue < 1462:
            if StreamOrder > 6:
                PernPts(x, y, DEMValue, PermID, GN)
            if StreamOrder == 6:
                if RipValue >= 0.275:
                    PernPts(x, y, DEMValue, PermID, GN)
                else:
                    IntmPts(x, y, DEMValue, PermID, GN)

            if StreamOrder == 5:
                if RipValue == 0:
                    EphmPts(x, y, DEMValue, PermID, GN)
                else:
                    IntmPts(x, y, DEMValue, PermID, GN)

            if StreamOrder < 5 and StreamOrder >= 3:
                if RipValue > 0.275:
                     IntmPts(x, y, DEMValue, PermID, GN)
                else:
                    EphmPts(x, y, DEMValue, PermID, GN)
            else:
                EphmPts(x, y, DEMValue, PermID, GN)
    del row
del rows

# Controlling for named streams in ephemerals and reassigning them to the
# intermittent category
delrow = arcpy.UpdateCursor(EphPts)
for row in delrow:
    x = str(row.getValue("X"))
    y = str(row.getValue("Y"))
    z = str(row.getValue("Z"))
    PermID = str(row.getValue("PERM_ID"))
    GNISA = str(row.getValue("GNIS"))
    GNISB = int(GNISA)
    if GNISB == 1:
        IntmPts(x, y, z, PermID, GNISB)
        delrow.deleteRow(row)
    del row
del delrow
