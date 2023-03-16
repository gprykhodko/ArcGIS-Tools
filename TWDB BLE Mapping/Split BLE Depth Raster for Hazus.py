########################################################################################
# Tool Name: 
# Version: 
# Use: This tool is designed to split water depth and elevation raster of different  
#      frequencies (e.g., 10, 100 , 500 years, etc.) by county boundaries. 
#      The split raster are stored in subfolders  indicated by the individual boundary names.
# Input parameters:  
#                    
#                   
# Author: Gennadii Prykhodko, Halff Accociates, Inc., 2022
########################################################################################

import arcpy, os

arcpy.env.overwriteOutput = True


 
def split_raster(field, split_feature, in_raster, split_by):
    out_coordinate_system = arcpy.Describe(in_raster).spatialReference
    project = arcpy.Project_management(split_feature, os.path.join(out_path, 'projectX'), out_coordinate_system)
    outCon = arcpy.sa.Con(arcpy.Raster(in_raster), 1)
    poly = arcpy.RasterToPolygon_conversion(outCon, os.path.join(out_path, 'outCon_polyX'), "NO_SIMPLIFY", "Value")
    arcpy.MakeFeatureLayer_management(project, "split_feature_pjr_lyr")
    split_feature = arcpy.management.SelectLayerByLocation("split_feature_pjr_lyr", "INTERSECT", poly, None, "NEW_SELECTION", "NOT_INVERT")
    split_feature_update = out_path + '\\' + 'split_feature_updated.shp'
    split_feature_lyr = arcpy.CopyFeatures_management(split_feature.getOutput(0), split_feature_update)#GP
    split_feature_lyr = arcpy.MakeFeatureLayer_management(split_feature_lyr.getOutput(0), 'split_feature_lyr')
    cursor = arcpy.SearchCursor(split_feature_update)
    base_name = arcpy.Raster(in_raster).name[:-4]
    
    for row in cursor:
        boundary_name = row.getValue(field)
        print ('Processing region ' + str(boundary_name))
        expresseion = f'{field} =' + "'"+ boundary_name +"'" #f'"{boundary_name}"'
        #print(expresseion)
        huc10 = arcpy.SelectLayerByAttribute_management(split_feature_lyr.getOutput(0), "NEW_SELECTION", expresseion)

        tmp_boundary = out_path + '\\' + 'tmp_' + str(boundary_name) + '.shp'
        arcpy.CopyFeatures_management(huc10.getOutput(0), tmp_boundary)

        spatial_reference = arcpy.Describe(tmp_boundary).spatialReference
    
        X_min = arcpy.Describe(tmp_boundary).extent.XMin
        Y_min = arcpy.Describe(tmp_boundary).extent.YMin
        X_max = arcpy.Describe(tmp_boundary).extent.XMax
        Y_max = arcpy.Describe(tmp_boundary).extent.YMax

        Rectangle = str(X_min) + ' ' + str(Y_min) + ' ' + str(X_max)+ ' '  + str(Y_max)
        if split_by == 'tract':
            clipped_raster = out_path + '\\' + base_name +'_' + boundary_name + '.tif'
        else: clipped_raster = out_path + '\\' + boundary_name + '.tif'

        with arcpy.EnvManager(snapRaster=in_raster):
            arcpy.Clip_management(in_raster, Rectangle, clipped_raster, tmp_boundary, "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")

    arcpy.env.workspace = out_path
    to_delete = arcpy.ListFeatureClasses()
    for i in to_delete:
        arcpy.Delete_management(os.path.join(out_path, i))

if __name__ == '__main__':

    in_raster = arcpy.GetParameterAsText(0)
    split_feature = arcpy.GetParameterAsText(1)
    out_path = arcpy.GetParameterAsText(2)

    if split_feature == 'County':
        split_feature = r'W:\Citrix\33000s\33606\006\GIS\Tools_Production\tool-data.gdb\Texas_County_Boundaries'
        split_raster("CNTY_NM", split_feature, in_raster, 'county')
    else:
        split_feature = r'W:\Citrix\33000s\33606\006\GIS\Tools_Production\tool-data.gdb\Texas_Census_Tracts'
        split_raster("TRT", split_feature, in_raster, 'tract')
