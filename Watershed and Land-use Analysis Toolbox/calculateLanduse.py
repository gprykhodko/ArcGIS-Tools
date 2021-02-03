# ########################################################################################
# Name: calculateLanduse.py
# Purpose: This script was developed in order to automate the process of calculating
#          acreage and percentage for each landuse category for regional stormwater
#          monitoring report. An ArcGIS Pro version of this tool is also available. Contact
#          the author for details.
# Output: A .csv table with watersheds and landuse categories (acreage/percentage) records
# Author: Gennadii Prykhodko, gennadii.prykhodko@mavs.uta.edu
# Date : July 2020
# ########################################################################################

import arcpy
import os
import sys
import csv
import numpy as np
import datetime

start = datetime.datetime.now()
arcpy.AddMessage("Start run: %s\n" % (start))
arcpy.env.workspace = arcpy.env.workspace
arcpy.env.scratchWorkspace = arcpy.env.scratchWorkspace
arcpy.env.overwriteOutput = True
arcpy.env.addOutputsToMap = False

watersheds_fc = arcpy.GetParameterAsText(0)
wshNameField = arcpy.GetParameterAsText(1)
landuse_fc = arcpy.GetParameterAsText(2)
landUseCatField = arcpy.GetParameterAsText(3)
sites_fc = arcpy.GetParameterAsText(4)

if arcpy.CheckProduct("ArcInfo") == "Unavailable":
    msg = "ArcGIS for Desktop Advanced license not available"
    arcpy.AddError(msg)
    arcpy.AddMessage(msg)
    sys.exit(msg)

watershedName = wshNameField 
lyr_name = "WatershedsLayer"
lyr1_name = "SitesLayer"
outPath = arcpy.env.scratchWorkspace
outCS = arcpy.SpatialReference("NAD 1983 StatePlane Texas N Central FIPS 4202 (US Feet)")
lyr = arcpy.MakeFeatureLayer_management(watersheds_fc, lyr_name)[0]
lyr1 = arcpy.MakeFeatureLayer_management(sites_fc, lyr1_name)[0]
arcpy.management.SelectLayerByLocation(lyr, "CONTAINS", lyr1, None, "NEW_SELECTION", "NOT_INVERT")
watersheds_fc = arcpy.management.CopyFeatures(lyr, "monitored_watersheds")
try:
    road = arcpy.analysis.Erase(watersheds_fc, landuse_fc, os.path.join(outPath, "roads"))
except:
    msg = "ArcGIS for Desktop Advanced license not available"
    arcpy.AddError(msg)
    arcpy.AddMessage(msg)
    sys.exit(msg)
    
landuse = arcpy.analysis.Clip(landuse_fc, watersheds_fc, os.path.join(outPath, "landuse"))

objectID = arcpy.FieldMap()

fms = arcpy.FieldMappings()

objectID.addInputField(road, "OBJECTID")

fms.addFieldMap(objectID)

arcpy.management.Append(road, landuse, "NO_TEST", fms, '')
exp = "func(!{0}!)".format(landUseCatField)
codeblock = """
def func(x):
    if x is None:
        return "Road"
    return x"""
arcpy.management.CalculateField(landuse, landUseCatField, exp, "PYTHON", codeblock)

expression = '!{0}!.replace("-", "_").replace(" ","_")'.format(watershedName)
arcpy.CalculateField_management(watersheds_fc, watershedName,
                                expression, "PYTHON")
del lyr_name, lyr1_name, lyr, lyr1, road, objectID, fms, codeblock, sites_fc, landuse_fc, expression


with arcpy.da.SearchCursor(watersheds_fc, ["SHAPE@", watershedName], ) as cursor:
    for i in cursor:
        arcpy.analysis.Clip(landuse, i[0], os.path.join(outPath, i[1]))
del landuse, cursor

file_name_field = "AreaAcre"

prev_workspace = arcpy.env.workspace

def find_all_fcs(workspace):

    arcpy.env.workspace = workspace
    feature_classes = arcpy.ListFeatureClasses()

    return feature_classes

feature_classes = find_all_fcs(arcpy.env.scratchWorkspace)
feature_classes.remove("landuse")
feature_classes.remove("roads")

for fc in feature_classes:
    
    # add field to hold the file name if it does not exist
    existing_fields = [f.name for f in arcpy.ListFields(fc)]
    if file_name_field not in existing_fields:
        arcpy.management.AddField(fc, file_name_field, "FLOAT")
    #arcpy.CalculateGeometryAttributes_management(fc, [["AreaAcre", "AREA"]], area_unit = "ACRES", coordinate_system = outCS)
    arcpy.CalculateField_management(fc, "AreaAcre", "!shape.area@acres!", "PYTHON", "")

codeblock = """
import numpy as np
commercial = np.array(["Office", "Education", "Large stadium", "Railroad", "Communication", "Transit", "Mixed use", "Retail", "Institutional/semi-public", "Utilities", "Parking", "Hotel/motel"])
open_ = np.array(["Parks/recreation", "Landfill", "Cemeteries", "Residential acreage", "Ranch land", "Timberland", "Farmland", "Improved acreage", "Flood control", "Under construction", "Vacant"])
residential = np.array(["Group quarters", "Single family", "Multi-family", "Mobile home"])
water = np.array(["Water", "Small water bodies"])
road = np.array(["Airport", "Runway", "Road"])

def func(arg):
    if arg in commercial:
        return "Commercial"
    if arg in open_:
        return "Open"
    if arg in residential:
        return "Residential"
    if arg in water:
        return "Water"
    if arg in road:
        return "Road"
    return arg"""

for fc in feature_classes:
    arcpy.management.CalculateField(fc, landUseCatField, exp, "PYTHON", codeblock)

arcpy.management.Delete("roads")
arcpy.management.Delete("landuse")


for fc in feature_classes:
    arcpy.Dissolve_management(fc, os.path.join(prev_workspace, fc), landUseCatField, "AreaAcre SUM", "MULTI_PART", "DISSOLVE_LINES")

    arcpy.management.Delete(fc)

    
del feature_classes, codeblock, exp


def createCSV(data, csvname, mode = 'a'):
    with open(csvname, mode) as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(data)
        arcpy.AddMessage(data)

headers = np.array(["WatershedName","TotalArea","Commercial", "Industrial", "Open", "Residential", "Road", "Water"], dtype=object)
#try:
path = arcpy.GetParameterAsText(5)
os.chdir(path)
arcpy.env.workspace = path
#except:
    #path = os.path.dirname(arcpy.mp.ArcGISProject("CURRENT").filePath)
    
   
createCSV(headers, "landuse.csv", "w")

feature_classes = find_all_fcs(prev_workspace)
feature_classes.remove("monitored_watersheds")

for fc in feature_classes:
    arr = arcpy.da.FeatureClassToNumPyArray(fc, (landUseCatField, 'SUM_AreaAcre'))
    total = arr['SUM_AreaAcre'].sum()
    com = arr[arr[landUseCatField] == 'Commercial']['SUM_AreaAcre'][0]
    try:
        ind = arr[arr[landUseCatField] == 'Industrial']['SUM_AreaAcre'][0]
    except:
        ind = np.array([0])[0]
    open_ = arr[arr[landUseCatField] == 'Open']['SUM_AreaAcre'][0]
    res = arr[arr[landUseCatField] == 'Residential']['SUM_AreaAcre'][0]
    road = arr[arr[landUseCatField] == 'Road']['SUM_AreaAcre'][0]
    try:
        water = arr[arr[landUseCatField] == 'Water']['SUM_AreaAcre'][0]
    except:
        water = np.array([0])[0]
    com_perc = (com/total*100).round(1)
    ind_perc = (ind/total*100).round(1)
    open_perc = (open_/total*100).round(1)
    res_perc = (res/total*100).round(1)
    road_perc = (road/total*100).round(1)
    water_perc = (water/total*100).round(1)
    record = np.array([fc, total.round(1), 
    str(com.round(1)) + '/' + str(com_perc), 
    str(ind.round(1)) + '/' + str(ind_perc), 
    str(open_.round(1)) + '/' + str(open_perc), 
    str(res.round(1)) + '/ ' + str(res_perc),
    str(road.round(1)) + '/' + str(road_perc),
    str(water.round(1)) + '/' + str(water_perc)], dtype=object)
    
    createCSV(record, os.path.join(path, "landuse.csv"))
    
del feature_classes, record, headers, arr, total, com, ind, open_, res, road, water, com_perc, ind_perc, open_perc, res_perc, water_perc, landUseCatField, wshNameField

arcpy.AddMessage("Finished run: %s\n\n" % (datetime.datetime.now() - start))
