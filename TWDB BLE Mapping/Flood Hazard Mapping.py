########################################################################################
# Tool Name: 
# Version: 
# Use: 
#      
#      
# Input parameters:  
#                    
#                   
# Author: Gennadii Prykhodko, Halff Accociates, Inc., 2022
########################################################################################


import arcpy, os, re

matrix = """AREA <= 14374.8 Or 
(AREA > 14374.8 And AREA <= 21780 And MEAN < 0.5) Or 
(AREA > 21780 And AREA <= 43560 And MEAN < 0.33) Or 
(AREA > 43560 And AREA <= 87120 And MEAN < 0.1)"""


fill_area = 2*43560 # fill area in sq.ft (2 acres)

codeblock = """
def findNull(f, v):
    if f is None:
        return v
    else:
        return f"""

arcpy.env.overwriteOutput = True
arcpy.env.addOutputsToMap = False


def create_raster_list(dr):
    dir_match = [root for root, dirs, files in os.walk(dr) if any([os.path.basename(root).startswith('Ex'), os.path.basename(root).endswith(('yr','Yr', 'YR'))])]
    match = [os.path.join(folder, file) for folder in dir_match for file in os.listdir(folder) if any(['Depth' in file, 'DPT' in file]) and file.endswith('SL.tif')]
    return match

class PolyRaster:
    def __init__(self, raster, poly, base_name):
        self.raster = raster
        self.poly = poly
        self.base_name = base_name

        
def fillUnderTwo(in_poly, in_raster, base_name):
    
    polyToLine = arcpy.management.PolygonToLine(in_poly, os.path.join(out_path, 'polyToLineX'), "IGNORE_NEIGHBORS")
    lineToFeature = arcpy.management.FeatureToPolygon(polyToLine, os.path.join(out_path, 'lineToFeatureX'), None, "ATTRIBUTES", None)
    underTwo = arcpy.conversion.FeatureClassToFeatureClass(lineToFeature, out_path, "underTwoX", f'Shape_Area <= {fill_area}')
    dissolveA = arcpy.management.Dissolve(underTwo, os.path.join(out_path, 'underTwoAX'), None, None, "SINGLE_PART")
    
    arcpy.management.CalculateField(dissolveA, "ConstRaster", "0.1", "PYTHON3", '', "FLOAT")
    raster = arcpy.conversion.PolygonToRaster(dissolveA, "ConstRaster", os.path.join(out_path, base_name + "_matrix_filled_raster"), "CELL_CENTER", "NONE", in_raster, "DO_NOT_BUILD")
    merge = arcpy.management.Merge([in_poly, dissolveA], os.path.join(out_path, 'mergeX'))# possibly change to append
    poly = arcpy.management.Dissolve(merge, os.path.join(out_path, base_name + "_matrix_filled_polyX"), None, None, "SINGLE_PART")
    
    return PolyRaster(raster, poly, base_name)

def applyMatrix(in_raster):
    
    in_raster = arcpy.Raster(in_raster)
    arcpy.env.snapRaster = in_raster
    base_name = in_raster.name.split(".")[0]        
    out_raster = arcpy.sa.Int(in_raster)
    out_raster = arcpy.sa.RegionGroup(out_raster, "FOUR", "CROSS", "NO_LINK", None)
    zsTable = arcpy.sa.ZonalStatisticsAsTable(out_raster, "Value", in_raster, r"in_memory\\zsTable", 
                                              "DATA", "MEAN")
    arcpy.management.JoinField(out_raster, "OBJECTID", zsTable, "OBJECTID", ["AREA","MEAN"])
    with arcpy.EnvManager(snapRaster=in_raster):
        out_raster = arcpy.sa.SetNull(out_raster, out_raster, matrix)
    with arcpy.EnvManager(outputZFlag="Disabled", outputMFlag="Disabled"):
        polygon = arcpy.conversion.RasterToPolygon(out_raster, os.path.join(out_path, 'polygonX'), "NO_SIMPLIFY", "OBJECTID", "SINGLE_OUTER_PART", None)

    filled = fillUnderTwo(polygon, in_raster, base_name) #fill holes that are less or equal to 2 acres
    
    out_raster = arcpy.sa.ExtractByMask(in_raster, out_raster) 
    out_raster = (arcpy.sa.Int(out_raster*10 + 0.5))/10
    arcpy.management.Mosaic(out_raster, filled.raster, "LAST", "FIRST", None, None, "NONE", 0, "NONE")
    
    return filled


def merge_fld(to_merge):
    poly_10 = arcpy.management.Rename(to_merge[0].poly, os.path.join(out_path, to_merge[0].base_name + "_matrix_filled_poly"))
    poly_100 = arcpy.management.Append(poly_10, to_merge[1].poly, "NO_TEST", None, '', '')
    poly_100 = arcpy.management.Dissolve(poly_100, os.path.join(out_path, to_merge[1].base_name + "_matrix_filled_poly"), None, None, "SINGLE_PART")
    poly_500 = arcpy.management.Append(poly_100, to_merge[2].poly, "NO_TEST", None, '', '')
    poly_500 = arcpy.management.Dissolve(poly_500, os.path.join(out_path, to_merge[2].base_name + "_matrix_filled_poly"), None, None, "SINGLE_PART")
    p_list = [poly_10, poly_100, poly_500]
    arcpy.management.Mosaic(to_merge[1].raster, to_merge[0].raster, "LAST", "FIRST", None, None, "NONE", 0, "NONE")#100 depth
    arcpy.management.MosaicToNewRaster([to_merge[2].raster, to_merge[0].raster], out_path, "BLE_DEP0_2PCT", None, "32_BIT_FLOAT", None, 1, "FIRST", "FIRST")#500 depth
    arcpy.management.Delete(to_merge[2].raster)
    arcpy.management.Delete(to_merge[1].raster)
    arcpy.management.Rename(to_merge[0].raster, os.path.join(out_path, "BLE_DEP_01PCT"))#to_merge[1].base_name 
    to_delete = arcpy.ListFeatureClasses("*X")
    for fc in to_delete:
        arcpy.management.Delete(os.path.join(out_path, fc))
    return p_list

'''
def smooth_ble_poly(in_poly, base_name):
    matrixLine = arcpy.management.PolygonToLine(in_poly, os.path.join(out_path, base_name + "_MATRIX_LINEX"), "IGNORE_NEIGHBORS")
    simlifyLine = arcpy.cartography.SimplifyLine(matrixLine, os.path.join(out_path, base_name + "_SIMLIFYX"), "POINT_REMOVE", "5 Feet", collapsed_point_option = 'NO_KEEP' )
    smoothLine = arcpy.cartography.SmoothLine(simlifyLine, os.path.join(out_path, base_name + "_SmoothLineX"), "PAEK", "10 Feet", "FIXED_CLOSED_ENDPOINT")
    polygon = arcpy.management.FeatureToPolygon(smoothLine, os.path.join(out_path, base_name + "_PolygonX"))
    points = arcpy.management.FeatureToPoint(in_poly, os.path.join(out_path, base_name + "_PointX"), "INSIDE")                                           
    join = arcpy.analysis.SpatialJoin(polygon, points, os.path.join(out_path, base_name + "_JoinX"), "JOIN_ONE_TO_ONE", "KEEP_COMMON", '', "INTERSECT")
    smoothed_poly = arcpy.conversion.FeatureClassToFeatureClass(join, out_path, base_name + "_smoothed_poly", "Join_Count <> 0")
    to_delete = arcpy.ListFeatureClasses("*X")
    for fc in to_delete:
        arcpy.management.Delete(os.path.join(out_path, fc))
    return smoothed_poly'''

def smooth_ble_poly(in_poly, base_name):
    matrixLine = arcpy.management.PolygonToLine(in_poly, os.path.join(out_path, base_name + "_MATRIX_LINEX"), "IGNORE_NEIGHBORS")
    matrixLine = arcpy.management.MultipartToSinglepart(matrixLine, os.path.join(out_path, base_name + "_MATRIX_LINESX"))
    smoothLine = arcpy.cartography.SmoothLine(matrixLine, os.path.join(out_path, base_name + "_SmoothLineX"), "PAEK", "10 Feet", "FIXED_CLOSED_ENDPOINT")
    polygon = arcpy.management.FeatureToPolygon(smoothLine, os.path.join(out_path, base_name + "_PolygonX"))
    points = arcpy.management.FeatureToPoint(in_poly, os.path.join(out_path, base_name + "_PointX"), "INSIDE")                                           
    
    if arcpy.Exists(os.path.join(out_path, base_name + "_poly_smoothed")):
        joinX = arcpy.analysis.SpatialJoin(polygon, points, os.path.join(out_path, base_name + "_poly_smoothedX"), "JOIN_ONE_TO_ONE", "KEEP_COMMON", '', "INTERSECT")
        join = arcpy.management.Append(joinX, os.path.join(out_path, base_name + "_poly_smoothed"), 'NO_TEST')
    if not arcpy.Exists(os.path.join(out_path, base_name + "_poly_smoothed")):
        join = arcpy.analysis.SpatialJoin(polygon, points, os.path.join(out_path, base_name + "_poly_smoothed"), "JOIN_ONE_TO_ONE", "KEEP_COMMON", '', "INTERSECT")
    to_delete = arcpy.ListFeatureClasses("*X")
    for fc in to_delete:
        arcpy.management.Delete(os.path.join(out_path, fc))
    return join

def calc_attr(in_fld, out_fld):
    fms = arcpy.FieldMappings()
    fms.addTable(out_fld)
    arcpy.management.Append(in_fld, out_fld, "NO_TEST", fms)
    arcpy.management.CalculateFields(out_fld, "PYTHON3", "V_DATUM \"\'NAVD88\'\";LEN_UNIT \"\'FT\'\";STATIC_BFE -9999;DEPTH -9999;VELOCITY -9999;VE" +
    "L_UNIT \"\'\'\";BFE_REVERT -9999;DEP_REVERT -9999;DUAL_ZONE \"\'F\'\";STUDY_TYP \"\'NP\'\";S" +
    "OURCE_CIT \"\'STUDY1\'\";AR_REVERT \"\'NP\'\";AR_SUBTRV \"\'NP\'\"", '', "NO_ENFORCE_DOMAINS")
    if '10_SL' in in_fld.getOutput(0):
        arcpy.management.CalculateFields(out_fld, "PYTHON3", "SFHA_TF \"\'T\'\";ZONE_SUBTY \"\'NP\'\"", '', "NO_ENFORCE_DOMAINS")
    if 'AR_500' in in_fld.getOutput(0): #500yr
        arcpy.management.CalculateFields(out_fld, "PYTHON3", "ZONE_SUBTY \"findNull(!ZONE_SUBTY!,\'0500\')\";EST_Risk" +
    " \"findNull(!EST_Risk!, \'Moderate\')\";FLD_ZONE \"findNull(!FLD_ZONE!, \'X\')\";SFHA_TF" +
    " \"findNull(!SFHA_TF!, \'F\')\"", codeblock, "NO_ENFORCE_DOMAINS")
    if '100' in os.path.basename(in_fld.getOutput(0)): #100yr
        arcpy.management.CalculateFields(out_fld, "PYTHON3", "ZONE_SUBTY \"findNull(!ZONE_SUBTY!,\'NP\')\";EST_Risk" +
    " \"findNull(!EST_Risk!, \'High\')\";FLD_ZONE \"findNull(!FLD_ZONE!, \'A\')\";SFHA_TF" +
    " \"findNull(!SFHA_TF!, \'T\')\"", codeblock, "NO_ENFORCE_DOMAINS")


def map_ble():
    in_rasters = create_raster_list(dr)
    in_rasters.sort(key=lambda f: int(re.sub('\D', '', os.path.basename(f))))
    to_merge = [applyMatrix(i) for i in in_rasters]
    base_name = [i.base_name for i in to_merge]
    to_smooth = merge_fld(to_merge)
    to_erase = []
    for poly, name in zip(to_smooth, base_name):
        fld_lyrA = arcpy.MakeFeatureLayer_management(poly, "fld_lyrA")
        fld_lyrB = arcpy.MakeFeatureLayer_management(poly, "fld_lyrB")
        fld_lyrA = arcpy.SelectLayerByAttribute_management(fld_lyrA.getOutput(0), "NEW_SELECTION", """Shape_Area <> (SELECT MAX(Shape_Area) FROM {} )""".format(name+'_matrix_filled_poly') )
        fld_lyrB = arcpy.SelectLayerByAttribute_management(fld_lyrB.getOutput(0), "NEW_SELECTION", """Shape_Area = (SELECT MAX(Shape_Area) FROM {} )""".format(name+'_matrix_filled_poly') )
        smooth_ble_poly(fld_lyrA.getOutput(0), name)
        smoothed_poly = smooth_ble_poly(fld_lyrB.getOutput(0), name)    
        to_erase.append(smoothed_poly)
    try:
        fld_500X = arcpy.analysis.PairwiseErase(to_erase[2], to_erase[1], os.path.join(out_path,"FLD_HAZ_AR_500X"))
    except:
        fld_500X = arcpy.analysis.Erase(to_erase[2], to_erase[1], os.path.join(out_path, "FLD_HAZ_AR_500X"))
    fld_500 = arcpy.management.MultipartToSinglepart(fld_500X, os.path.join(out_path,"FLD_HAZ_AR_500"))
    to_erase[2] = fld_500
    #at this point attributes will need to be populated
    for i in to_erase[1:3]:
        calc_attr(i,  os.path.join(out_path, r'EBFE_Dataset\FLD_HAZ_AR'))
    calc_attr(to_erase[0], os.path.join(out_path, r'EBFE_Dataset\TENPCT_FP'))
    return to_erase


if __name__ == '__main__':

    if arcpy.CheckExtension("Spatial") == "Available":
        arcpy.CheckOutExtension("Spatial")

        dr = arcpy.GetParameterAsText(0)# HUC10 folder
        out_folder = arcpy.GetParameterAsText(1) #out gdb
        gdb_name = os.path.basename(dr)
        gdb_name = re.sub('[^0-9a-zA-Z]+', '_', gdb_name)
        out_path = arcpy.management.CreateFileGDB(out_folder, gdb_name)
        out_path = out_path.getOutput(0)
        #import xml workspace can be moved to calc_attr function
        arcpy.management.ImportXMLWorkspaceDocument(out_path, r"W:\Citrix\33000s\33606\006\GIS\Tools_Production\EBFE_schema.xml", "SCHEMA_ONLY")
        arcpy.env.workspace = out_path
        arcpy.env.scratchWorkspace = out_path
        map_ble()

        arcpy.CheckInExtension("Spatial")

    else:
        msg = "Spatial Analyst license is required for Flood Hazard Mapping and at this time it is NOT available"
        arcpy.AddError(msg)
        sys.exit(msg)






