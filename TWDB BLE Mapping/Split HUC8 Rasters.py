########################################################################################
# Tool Name: TWDB BLE Raster Split
# Version: 4.0 - For Python 3.7 or run under IDLE (ArcGIS Pro) 
# Use: This tool is designed to split water depth and elevation raster of different  
#      frequencies (e.g., 10, 100 , 500 years, etc.)  HUC10 boundaries.
#      The split raster are stored in subfolders indicated by the individual boundary names.
#      
# Input parameters: Users need to specify the root path of rasters to be split, output 
#                   path for the split rasters, clipping feature, and the field name 
#                   which the rasters are organized by. 
# Author: Gennadii Prykhodko, 2/22/2022
########################################################################################

import arcpy
from arcpy import env
from arcpy.sa import *
import time
import os, re

env.overwriteOutput = True


raster_path = arcpy.GetParameterAsText(0)
out_path = arcpy.GetParameterAsText(1)
split_feature = r'W:\Citrix\33000s\33606\006\GIS\Tools_Production\tool-data.gdb\WBDHU10'
huc8 = r'W:\Citrix\33000s\33606\006\GIS\Tools_Production\tool-data.gdb\WBDHU8'
 
sub_folders = os.listdir(raster_path)
env.workspace = os.path.join(raster_path,sub_folders[0])


rasters_in_sub_folder = arcpy.ListRasters("*_SL.tif")
if not rasters_in_sub_folder:
    rasters_in_sub_folder = arcpy.ListRasters("*", "tif")

split_feature_pjr = os.path.join(out_path, 'split_feature_prj.shp')
snap_raster = rasters_in_sub_folder[0]
out_coordinate_system = arcpy.Describe(snap_raster).spatialReference
arcpy.Project_management(split_feature, split_feature_pjr, out_coordinate_system)

outCon = Con(Raster(snap_raster), 1)
outCon_poly = os.path.join(out_path,'outCon.shp')
poly = arcpy.RasterToPolygon_conversion(outCon, outCon_poly, "NO_SIMPLIFY", "Value")
arcpy.MakeFeatureLayer_management(split_feature_pjr, "split_feature_pjr_lyr")
split_feature = arcpy.management.SelectLayerByLocation("split_feature_pjr_lyr", "INTERSECT", outCon_poly, None, "NEW_SELECTION", "NOT_INVERT")
split_feature_update = out_path + '\\' + 'split_feature_updated.shp'
split_buffer = arcpy.analysis.Buffer(split_feature, split_feature_update, '100 Feet')

split_feature_lyr = arcpy.MakeFeatureLayer_management(split_feature_update, 'split_feature_lyr')#GP


lakepond_clip = arcpy.analysis.Clip(r'W:\Citrix\33000s\33606\006\GIS\Tools_Production\Gennadii22_OS.sde\gennadii22.GISDBO.nhd_lakepond',
                                    split_feature_update, os.path.join(out_path,'lakepond_clip.shp'), None)
#change to _SL.tif
def create_raster_list(dr):
    dir_match = [root for root, dirs, files in os.walk(dr)]
    match = [os.path.join(folder, file) for folder in dir_match for file in os.listdir(folder) if any(['Depth' in file, 'DPT' in file]) and file.endswith('_SL.tif')]
    return match

in_rasters = create_raster_list(raster_path)
in_rasters.sort(key=lambda f: int(re.sub('\D', '', os.path.basename(f))))

with arcpy.EnvManager(snapRaster=in_rasters[0]):
    copy10 = arcpy.management.CopyRaster(in_rasters[0], os.path.join(os.path.dirname(in_rasters[0]), os.path.basename(in_rasters[0]).split('.')[0] + '_Copy.tif'), '', None, "-9999", "NONE", "NONE", '', "NONE", "NONE", "TIFF", "NONE", "CURRENT_SLICE", "NO_TRANSPOSE")
    copy100 = arcpy.management.CopyRaster(in_rasters[1], os.path.join(os.path.dirname(in_rasters[1]), os.path.basename(in_rasters[1]).split('.')[0] + '_Copy.tif'), '', None, "-9999", "NONE", "NONE", '', "NONE", "NONE", "TIFF", "NONE", "CURRENT_SLICE", "NO_TRANSPOSE")
    copy500 = arcpy.management.CopyRaster(in_rasters[2], os.path.join(os.path.dirname(in_rasters[2]), os.path.basename(in_rasters[2]).split('.')[0] + '_Copy.tif'), '', None, "-9999", "NONE", "NONE", '', "NONE", "NONE", "TIFF", "NONE", "CURRENT_SLICE", "NO_TRANSPOSE")
with arcpy.EnvManager(outputCoordinateSystem=out_coordinate_system, snapRaster=Raster(copy10)):
    arcpy.conversion.PolygonToRaster(lakepond_clip, "Value", in_rasters[0], "CELL_CENTER", "NONE", copy10, "DO_NOT_BUILD")
    arcpy.conversion.PolygonToRaster(lakepond_clip, "Value", in_rasters[1], "CELL_CENTER", "NONE", copy100, "DO_NOT_BUILD")
    arcpy.conversion.PolygonToRaster(lakepond_clip, "Value", in_rasters[2], "CELL_CENTER", "NONE", copy500, "DO_NOT_BUILD")

arcpy.management.Mosaic(copy10, in_rasters[0], "LAST", "FIRST", None, None, "NONE", 0, "NONE")
arcpy.management.Mosaic(copy100, in_rasters[1], "LAST", "FIRST", None, None, "NONE", 0, "NONE")
arcpy.management.Mosaic(copy500, in_rasters[2], "LAST", "FIRST", None, None, "NONE", 0, "NONE")
    
cursor = arcpy.SearchCursor(split_feature_update)
for row in cursor:
    boundary_name = row.getValue("name")
    print ('Processing region ' + str(boundary_name))
    expresseion = 'name =' + "'"+ boundary_name +"'" #f'"{boundary_name}"'
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
    
    for sub_folder in sub_folders:  ### Loop by year frequency

        env.workspace = raster_path + '\\' + sub_folder
        #print(env.workspace)
        rasters_in_sub_folder = arcpy.ListRasters("*_SL.tif")
        if not rasters_in_sub_folder:
            rasters_in_sub_folder = arcpy.ListRasters("*", "tif")
        #print(rasters_in_sub_folder)
        for raster in rasters_in_sub_folder:   ### Loop by "Depth" or "WSE" raster
            arcpy.env.snapRaster = raster
            inRaster = env.workspace + '\\' + raster
            print('In Raster:',inRaster)
            output_location = out_path + '\\' + str(boundary_name) + '\\'  + 'Ex_' + sub_folder
            if not os.path.exists(output_location):
                os.makedirs(output_location)
            print('Output Location:',output_location)
            clipped_raster = output_location + '\\' + raster
            print('Raster Name:', clipped_raster)
            with arcpy.EnvManager(snapRaster=raster):
                arcpy.Clip_management(inRaster, Rectangle, clipped_raster, tmp_boundary, "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
    
del row, cursor
in_dpt = create_raster_list(raster_path)
in_dpt.sort(key=lambda f: int(re.sub('\D', '', os.path.basename(f))))
for idx, i in enumerate(in_dpt):
    arcpy.management.Delete(in_dpt[idx])
    arcpy.management.Rename(os.path.join(os.path.dirname(in_dpt[idx]),os.path.basename(in_dpt[idx][:-4]+'_Copy.tif')), in_dpt[idx])

#arcpy.Delete_management(split_feature_pjr)
env.workspace = out_path
to_delete = arcpy.ListFeatureClasses()
for i in to_delete:
    arcpy.Delete_management(os.path.join(out_path, i))
del arcpy




