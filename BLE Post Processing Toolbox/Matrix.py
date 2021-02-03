'''-----------------------------------------------------------
Tool Name:   Matrix
Source Name: Matrix.py
Version:     ArcGIS Pro 2.6
Author: Gennadii Prykhodko, Texas Water Development Board
Required Arguments:
             Input BLE Depth Grid (Raster)
             Target Geodatabase (Geodatabase)
Description: This tool takes BLE depth grid with horizontal
             and vertical units in feet and removes areas
             that are less than 0.25 acres or between 0.25 - 0.5
             acres and with average depth less than 0.5 feet or
             between 0.5 - 1 acres and average depth less than
             0.25 acres or between 1 - 2 acres and average depth
             less than 0.1 feet.
-----------------------------------------------------------'''

import arcpy, os


arcpy.env.overwriteOutput = True
arcpy.env.addOutputsToMap = False


matrix = """AREA <= 10890 Or 
(AREA > 10890 And AREA <= 21780 And MEAN < 0.5) Or 
(AREA > 21780 And AREA <= 43560 And MEAN < 0.25) Or 
(AREA > 43560 And AREA <= 87120 And MEAN < 0.1)"""

def applyMatrix(in_raster):
            
    in_raster = arcpy.Raster(in_raster)
    base_name = in_raster.name.split(".")[0]
    out_raster = arcpy.sa.Int(in_raster)
    out_raster = arcpy.sa.RegionGroup(out_raster, "FOUR", "CROSS", "NO_LINK", None)
    zsTable = arcpy.sa.ZonalStatisticsAsTable(out_raster, "Value", in_raster, r"memory\\zsTable", 
                                              "DATA", "MEAN", "CURRENT_SLICE")
    arcpy.management.JoinField(out_raster, "OBJECTID", zsTable, "OBJECTID", ["AREA","MEAN"])
    out_raster = arcpy.sa.SetNull(out_raster, out_raster, matrix)
    with arcpy.EnvManager(outputZFlag="Disabled", outputMFlag="Disabled"):
        polygon = arcpy.conversion.RasterToPolygon(out_raster, r"memory\\polygon", "NO_SIMPLIFY", "OBJECTID", "SINGLE_OUTER_PART", None)
    polygon = arcpy.management.EliminatePolygonPart(polygon, os.path.join(out_path, base_name + "_Polygon"), 
                                          "AREA", "13068 SquareFeet", 0, "CONTAINED_ONLY")
    out_raster = arcpy.sa.ExtractByMask(in_raster, out_raster) 
    out_raster = (arcpy.sa.Int(out_raster*10 + 0.5))/10
    out_raster.save(os.path.join(out_path, base_name + "_Cleaned"))
    del polygon, out_raster

if __name__ == '__main__':


    in_raster = arcpy.GetParameterAsText(0)
    out_path = arcpy.GetParameterAsText(1)

    applyMatrix(in_raster)

    

