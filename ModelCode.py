
import arcpy
import csv
import os
import traceback

FeatureClass =r'D:\GIS\UCRB\1403.gdb\NHDFlowline'
DEM = r'D:\GIS\UCRB\1403.gdb\ElevZonal_ProjectRaster'
FCOutput = FeatureClass+"PT"
workspace = r'D:\GIS\UCRB\1403.gdb'
template = r'D:\GIS\UCRB\1403.gdb\ptstemplate'
arcpy.env.workspace = workspace
PerPts = FeatureClass+"PerPts"
IntPts = FeatureClass+"IntPts"
EphPts = FeatureClass+"EphPts"
Spatial_Ref = arcpy.Describe(FeatureClass).spatialReference
ValBot = r'D:\GIS\UCRB\1403.gdb\ValleyBottom_'
PETRast = r'D:\GIS\UCRB\1403.gdb\PET'
EVTRast = r'D:\GIS\UCRB\1403.gdb\EVT'
Rip60 = r'D:\GIS\UCRB\1403.gdb\NHD1403ZonalRiparian'

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

# CSV Writer
Fields = ['PermID','x', 'y','z', 'EVT', 'PET', 'Riparian', 'ValBot', 'GNIS', 'Order', 'Type']
wtr = csv.writer(open("D:\TestCSV.csv", "wb"))
wtr.writerow(Fields)

def EphmWriter (A, B, C, D, E, F, G, H, I, J):
    RowLine =[A, B, C, D, E, F, G, H, I, J, "Eph"]
    wtr.writerow(RowLine)

def IntWriter (A, B, C, D, E, F, G, H, I, J):
    RowLine =[A, B, C, D, E, F, G, H, I, J, "Int"]
    wtr.writerow(RowLine)

def PerWriter (A, B, C, D, E, F, G, H, I, J):
    RowLine =[A, B, C, D, E, F, G, H, I, J, "Per"]
    wtr.writerow(RowLine)

# Creation of the feature classes
arcpy.CreateFeatureclass_management(workspace, "NHDFlowlinePerPts", "POINT", template, "SAME_AS_TEMPLATE", "SAME_AS_TEMPLATE", Spatial_Ref)
arcpy.CreateFeatureclass_management(workspace, "NHDFlowlineIntPts", "POINT", template, "SAME_AS_TEMPLATE", "SAME_AS_TEMPLATE", Spatial_Ref)
arcpy.CreateFeatureclass_management(workspace, "NHDFlowlineEphPts", "POINT", template, "SAME_AS_TEMPLATE", "SAME_AS_TEMPLATE", Spatial_Ref)
arcpy.FeatureToPoint_management(FeatureClass, FCOutput, "INSIDE")
arcpy.AddXY_management(FCOutput)

rows = arcpy.SearchCursor(FCOutput)
for row in rows:
    try:
        x = str(row.getValue("POINT_X"))
        y = str(row.getValue("POINT_Y"))
        StreamOrder = row.getValue("ST_ORDER")
        PermID = row.getValue("PERMANENT_IDENTIFIER")
        FCode = row.getValue("FCode")
        DEMValuePassA = arcpy.GetCellValue_management(DEM, x+' '+y,"1")   #Change to UTMCoord if applicable
        DEMValuePassB = str(DEMValuePassA)
        if DEMValuePassB == 'NoData':
            DEMValue = 0.0
            print "no DEM data at "+x+" "+y
        else:
            DEMValue = float(DEMValuePassB)
        GNIS = row.getValue("GNIS_Name")
        if GNIS is not None:
            GN = 1
        else:
            GN = 0
        ValBotPassA = arcpy.GetCellValue_management(ValBot, x+' '+y,"1")
        ValBotPassB = str(ValBotPassA)
        if ValBotPassB == 'NoData':
            ValBotValue = ValBotPassB
        else:
            ValBotValue = int(ValBotPassB)
        PET = arcpy.GetCellValue_management(PETRast, x+' '+y,"1")
        PET = str(PET)
        if PET == 'NoData':
            PET = 0.0
            print "no PET data at "+x+" "+y
        else:
            PET = float(PET)
        RipDataPassA = arcpy.GetCellValue_management(Rip60, x+' '+y,"1")
        RipDataPassB = str(RipDataPassA)
        if RipDataPassB == 'NoData':
            RipValue = 0.0
        else:
            RipValue = float(RipDataPassB)
        EVT = arcpy.GetCellValue_management(EVTRast, x+' '+y,"1")
        EVT = str(EVT)
        if EVT == 'NoData':
            EVT = 0.0
            print "no EVT data at "+x+" "+y
        else:
            EVT = float(EVT)
        if ValBotValue == 1:
                PernPts(x, y, DEMValue, PermID, GN)
                PerWriter(PermID, x, y, DEMValue, EVT, PET, RipValue, ValBotValue, GNIS, StreamOrder)
        elif FCode == 46006:
                PernPts(x, y, DEMValue, PermID, GN)
                PerWriter(PermID, x, y, DEMValue, EVT, PET, RipValue, ValBotValue, GNIS, StreamOrder)
        elif FCode == 46007:
            EphmPts(x, y, DEMValue, PermID, GN)
            EphmWriter(PermID, x, y, DEMValue, EVT, PET, RipValue, ValBotValue, GNIS, StreamOrder)
        elif StreamOrder >= 6:
            PernPts(x, y, DEMValue, PermID, GN)
            PerWriter(PermID, x, y, DEMValue, EVT, PET, RipValue, ValBotValue, GNIS, StreamOrder)
        else:
            if DEMValue >= 2300:
                IntmPts(x, y, DEMValue, PermID, GN)
            elif PET > 525.09:
                if DEMValue <= 1676:
                    EphmPts(x, y, DEMValue, PermID, GN)
                    EphmWriter(PermID, x, y, DEMValue, EVT, PET, RipValue, ValBotValue, GNIS, StreamOrder)
                else:
                    if RipValue < 0.4:
                        EphmPts(x, y, DEMValue, PermID, GN)
                        EphmWriter(PermID, x, y, DEMValue, EVT, PET, RipValue, ValBotValue, GNIS, StreamOrder)
                    elif StreamOrder >= 5:
                        IntmPts(x, y, DEMValue, PermID, GN)
                        IntWriter(PermID, x, y, DEMValue, EVT, PET, RipValue, ValBotValue, GNIS, StreamOrder)
                    else:
                        IntmPts(x, y, DEMValue, PermID, GN)
                        IntWriter(PermID, x, y, DEMValue, EVT, PET, RipValue, ValBotValue, GNIS, StreamOrder)
            else:
                if PET <= 409.053:
                    IntmPts(x, y, DEMValue, PermID, GN)
                    IntWriter(PermID, x, y, DEMValue, EVT, PET, RipValue, ValBotValue, GNIS, StreamOrder)
                else:
                    if RipValue > 0.3:
                        IntmPts(x, y, DEMValue, PermID, GN)
                        IntWriter(PermID, x, y, DEMValue, EVT, PET, RipValue, ValBotValue, GNIS, StreamOrder)
                    elif StreamOrder >= 5:
                        IntmPts(x, y, DEMValue, PermID, GN)
                        IntWriter(PermID, x, y, DEMValue, EVT, PET, RipValue, ValBotValue, GNIS, StreamOrder)
                    else:
                        EphmPts(x, y, DEMValue, PermID, GN)
                        EphmWriter(PermID, x, y, DEMValue, EVT, PET, RipValue, ValBotValue, GNIS, StreamOrder)
    except:
        print "Slight problem at "+x+", "+y
        traceback.print_exc()
        del row
        continue
    del row
del rows

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

del wtr
