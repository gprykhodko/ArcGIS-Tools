import arcpy, os, re

arcpy.env.overwriteOutput = True
arcpy.env.addOutputsToMap = False

def mergeAX_repair(zone, gdbs, out_path):
    poly = [os.path.join(i, 'EBFE_Dataset\FLD_HAZ_AR') for i in gdbs]
    fld_zone = []
    for idx, val in enumerate(poly):
        fld_lyr = arcpy.MakeFeatureLayer_management(val, "fld_lyr_"+str(idx))
        fld_lyrA = arcpy.SelectLayerByAttribute_management(fld_lyr.getOutput(0), "NEW_SELECTION", "FLD_ZONE = {}".format(zone))
        #fld_lyrA = arcpy.RepairGeometry_management(fld_lyrA.getOutput(0))
        fld_zone.append(fld_lyrA.getOutput(0))
    poly10_merge = arcpy.management.Merge(fld_zone, os.path.join(out_path, 'FLD_FP_MergeX'))
    tenpct = arcpy.management.Dissolve(poly10_merge, os.path.join(out_path, 'FLD_FP_DissolveX'), None, "AR_REVERT FIRST;AR_SUBTRV FIRST;BFE_REVERT FIRST;DEP_REVERT FIRST;DEPTH FIRST;DUAL_ZONE FIRST;EST_AR_ID FIRST;EST_ID FIRST;EST_Risk FIRST;FLD_ZONE FIRST;LEN_UNIT FIRST;OBJECTID FIRST;SFHA_TF FIRST;Shape_Area FIRST;Shape_Length FIRST;SOURCE_CIT FIRST;STATIC_BFE FIRST;STUDY_TYP FIRST;V_DATUM FIRST;VEL_UNIT FIRST;VELOCITY FIRST;VERSION_ID FIRST;ZONE_SUBTY FIRST", "SINGLE_PART", "DISSOLVE_LINES")
    '''
    try:
        tenclip = arcpy.analysis.PairwiseClip(tenpct, r'W:\Citrix\33000s\33606\006\GIS\Tools_Production\tool-data.gdb\WBDHU8', os.path.join(out_path, 'FLD_HAZ_ARX'))
    except:
        tenclip = arcpy.analysis.Clip(tenpct, r'W:\Citrix\33000s\33606\006\GIS\Tools_Production\tool-data.gdb\WBDHU8', os.path.join(out_path, 'FLD_HAZ_ARX'))'''
    arcpy.management.Append(tenpct, os.path.join(out_path, 'EBFE_Dataset\FLD_HAZ_AR'), "NO_TEST", f'EST_ID "EST_ID" true true false 20 Text 0 0,First,#,{tenpct},FIRST_EST_ID,0,20;VERSION_ID "VERSION_ID" true true false 11 Text 0 0,First,#,{tenpct},FIRST_VERSION_ID,0,11;EST_AR_ID "EST_AR_ID" true true false 25 Text 0 0,First,#,{tenpct},FIRST_EST_AR_ID,0,25;V_DATUM "V_DATUM" true true false 17 Text 0 0,First,#,{tenpct},FIRST_V_DATUM,0,17;LEN_UNIT "LEN_UNIT" true true false 16 Text 0 0,First,#,{tenpct},FIRST_LEN_UNIT,0,16;SOURCE_CIT "SOURCE_CIT" true true false 15 Text 0 0,First,#,{tenpct},FIRST_SOURCE_CIT,0,15;EST_Risk "EST_Risk" true true false 30 Text 0 0,First,#,{tenpct},FIRST_EST_Risk,0,30;STUDY_TYP "STUDY_TYP" true true false 28 Text 0 0,First,#,{tenpct},FIRST_STUDY_TYP,0,28;SFHA_TF "SFHA_TF" true true false 1 Text 0 0,First,#,{tenpct},FIRST_SFHA_TF,0,1;ZONE_SUBTY "ZONE_SUBTY" true true false 72 Text 0 0,First,#,{tenpct},FIRST_ZONE_SUBTY,0,72;STATIC_BFE "STATIC_BFE" true true false 8 Double 0 0,First,#,{tenpct},FIRST_STATIC_BFE,-1,-1;DEPTH "DEPTH" true true false 8 Double 0 0,First,#,{tenpct},FIRST_DEPTH,-1,-1;VELOCITY "VELOCITY" true true false 8 Double 0 0,First,#,{tenpct},FIRST_VELOCITY,-1,-1;VEL_UNIT "VEL_UNIT" true true false 20 Text 0 0,First,#,{tenpct},FIRST_VEL_UNIT,0,20;AR_REVERT "AR_REVERT" true true false 17 Text 0 0,First,#,{tenpct},FIRST_AR_REVERT,0,17;AR_SUBTRV "AR_SUBTRV" true true false 72 Text 0 0,First,#,{tenpct},FIRST_AR_SUBTRV,0,72;BFE_REVERT "BFE_REVERT" true true false 8 Double 0 0,First,#,{tenpct},FIRST_BFE_REVERT,-1,-1;DEP_REVERT "DEP_REVERT" true true false 8 Double 0 0,First,#,{tenpct},FIRST_DEP_REVERT,-1,-1;DUAL_ZONE "DUAL_ZONE" true true false 1 Text 0 0,First,#,{tenpct},FIRST_DUAL_ZONE,0,1;FLD_ZONE "FLD_ZONE" true true false 17 Text 0 0,First,#,{tenpct},FIRST_FLD_ZONE,0,17', '', '')

def mergeAX(zone, gdbs, out_path):
    poly = [os.path.join(i, 'EBFE_Dataset\FLD_HAZ_AR') for i in gdbs]
    fld_zone = []
    for idx, val in enumerate(poly):
        fld_lyr = arcpy.MakeFeatureLayer_management(val, "fld_lyr_"+str(idx))
        fld_lyrA = arcpy.SelectLayerByAttribute_management(fld_lyr.getOutput(0), "NEW_SELECTION", "FLD_ZONE = {}".format(zone) )   
        fld_zone.append(fld_lyrA.getOutput(0))
    poly10_merge = arcpy.management.Merge(fld_zone, os.path.join(out_path, 'FLD_FP_MergeX'))
    tenpct = arcpy.analysis.PairwiseDissolve(poly10_merge, os.path.join(out_path, 'FLD_FP_DissolveX'), None, "AR_REVERT FIRST;AR_SUBTRV FIRST;BFE_REVERT FIRST;DEP_REVERT FIRST;DEPTH FIRST;DUAL_ZONE FIRST;EST_AR_ID FIRST;EST_ID FIRST;EST_Risk FIRST;FLD_ZONE FIRST;LEN_UNIT FIRST;OBJECTID FIRST;SFHA_TF FIRST;Shape_Area FIRST;Shape_Length FIRST;SOURCE_CIT FIRST;STATIC_BFE FIRST;STUDY_TYP FIRST;V_DATUM FIRST;VEL_UNIT FIRST;VELOCITY FIRST;VERSION_ID FIRST;ZONE_SUBTY FIRST", "SINGLE_PART")

    '''
    try:
        tenclip = arcpy.analysis.PairwiseClip(tenpct, os.path.join(out_path, 'HUC8_ClipX'), os.path.join(out_path, 'FLD_HAZ_ARX'))
    except:
        tenclip = arcpy.analysis.Clip(tenpct, os.path.join(out_path, 'HUC8_ClipX'), os.path.join(out_path, 'FLD_HAZ_ARX'))'''
    arcpy.management.Append(tenpct, os.path.join(out_path, 'EBFE_Dataset\FLD_HAZ_AR'), "NO_TEST", f'EST_ID "EST_ID" true true false 20 Text 0 0,First,#,{tenpct},FIRST_EST_ID,0,20;VERSION_ID "VERSION_ID" true true false 11 Text 0 0,First,#,{tenpct},FIRST_VERSION_ID,0,11;EST_AR_ID "EST_AR_ID" true true false 25 Text 0 0,First,#,{tenpct},FIRST_EST_AR_ID,0,25;V_DATUM "V_DATUM" true true false 17 Text 0 0,First,#,{tenpct},FIRST_V_DATUM,0,17;LEN_UNIT "LEN_UNIT" true true false 16 Text 0 0,First,#,{tenpct},FIRST_LEN_UNIT,0,16;SOURCE_CIT "SOURCE_CIT" true true false 15 Text 0 0,First,#,{tenpct},FIRST_SOURCE_CIT,0,15;EST_Risk "EST_Risk" true true false 30 Text 0 0,First,#,{tenpct},FIRST_EST_Risk,0,30;STUDY_TYP "STUDY_TYP" true true false 28 Text 0 0,First,#,{tenpct},FIRST_STUDY_TYP,0,28;SFHA_TF "SFHA_TF" true true false 1 Text 0 0,First,#,{tenpct},FIRST_SFHA_TF,0,1;ZONE_SUBTY "ZONE_SUBTY" true true false 72 Text 0 0,First,#,{tenpct},FIRST_ZONE_SUBTY,0,72;STATIC_BFE "STATIC_BFE" true true false 8 Double 0 0,First,#,{tenpct},FIRST_STATIC_BFE,-1,-1;DEPTH "DEPTH" true true false 8 Double 0 0,First,#,{tenpct},FIRST_DEPTH,-1,-1;VELOCITY "VELOCITY" true true false 8 Double 0 0,First,#,{tenpct},FIRST_VELOCITY,-1,-1;VEL_UNIT "VEL_UNIT" true true false 20 Text 0 0,First,#,{tenpct},FIRST_VEL_UNIT,0,20;AR_REVERT "AR_REVERT" true true false 17 Text 0 0,First,#,{tenpct},FIRST_AR_REVERT,0,17;AR_SUBTRV "AR_SUBTRV" true true false 72 Text 0 0,First,#,{tenpct},FIRST_AR_SUBTRV,0,72;BFE_REVERT "BFE_REVERT" true true false 8 Double 0 0,First,#,{tenpct},FIRST_BFE_REVERT,-1,-1;DEP_REVERT "DEP_REVERT" true true false 8 Double 0 0,First,#,{tenpct},FIRST_DEP_REVERT,-1,-1;DUAL_ZONE "DUAL_ZONE" true true false 1 Text 0 0,First,#,{tenpct},FIRST_DUAL_ZONE,0,1;FLD_ZONE "FLD_ZONE" true true false 17 Text 0 0,First,#,{tenpct},FIRST_FLD_ZONE,0,17', '', '')

def merge_huc10(gdbs, out_folder, gdb_name):
    out_path = arcpy.management.CreateFileGDB(out_folder, gdb_name)
    out_path = out_path.getOutput(0)
    arcpy.env.workspace = out_path
    arcpy.env.scratchWorkspace = out_path
    arcpy.management.ImportXMLWorkspaceDocument(out_path, r"W:\Citrix\33000s\33606\006\GIS\Tools_Production\EBFE_schema.xml", "SCHEMA_ONLY")
    depth500 = [os.path.join(i, 'BLE_DEP0_2PCT') for i in gdbs]
    depth100 = [os.path.join(i, 'BLE_DEP_01PCT') for i in gdbs]
    poly10 = [os.path.join(i, 'EBFE_Dataset\TENPCT_FP') for i in gdbs]
    #huc8 = r'W:\Citrix\33000s\33606\006\GIS\Tools_Production\tool-data.gdb\WBDHU8'
    
    depth500 = arcpy.management.MosaicToNewRaster(depth500, out_path, "BLE_DEP0_2PCT", None, "32_BIT_FLOAT", None, 1, "LAST", "FIRST")
    depth100 = arcpy.management.MosaicToNewRaster(depth100, out_path, "BLE_DEP_01PCT", None, "32_BIT_FLOAT", None, 1, "LAST", "FIRST")
    '''
    clip_feature_lyr = arcpy.MakeFeatureLayer_management(huc8, 'clip_feature_lyr')
    huc8 = re.sub('\D+', '', gdb_name)
    huc8 = f"huc8 = '{huc8}'"
    huc_select = arcpy.management.SelectLayerByAttribute(clip_feature_lyr.getOutput(0), "NEW_SELECTION", huc8)
    huc8 = arcpy.CopyFeatures_management(huc_select.getOutput(0), os.path.join(out_path, 'HUC8_ClipX'))
    X_min = arcpy.Describe(huc8).extent.XMin
    Y_min = arcpy.Describe(huc8).extent.YMin
    X_max = arcpy.Describe(huc8).extent.XMax
    Y_max = arcpy.Describe(huc8).extent.YMax
    
    Rectangle = str(X_min) + ' ' + str(Y_min) + ' ' + str(X_max)+ ' '  + str(Y_max)
    with arcpy.EnvManager(snapRaster=arcpy.Raster(depth500)):
        arcpy.management.Clip(depth500, Rectangle, os.path.join(out_path, "BLE_DEP0_2PCT"), huc8, None, "ClippingGeometry", "NO_MAINTAIN_EXTENT")
        arcpy.management.Clip(depth100, Rectangle, os.path.join(out_path, "BLE_DEP_01PCT"), huc8, None, "ClippingGeometry", "NO_MAINTAIN_EXTENT")'''
        
    poly10_merge = arcpy.management.Merge(poly10, os.path.join(out_path, 'TENPCT_FP_MergeX'))
    try:
        tenpct = arcpy.management.Dissolve(poly10_merge, os.path.join(out_path, 'TENPCT_FP_DissolveX'), None, "AR_REVERT FIRST;AR_SUBTRV FIRST;BFE_REVERT FIRST;DEP_REVERT FIRST;DEPTH FIRST;DUAL_ZONE FIRST;EST_AR_ID FIRST;EST_ID FIRST;EST_Risk FIRST;FLD_ZONE FIRST;LEN_UNIT FIRST;OBJECTID FIRST;SFHA_TF FIRST;Shape_Area FIRST;Shape_Length FIRST;SOURCE_CIT FIRST;STATIC_BFE FIRST;STUDY_TYP FIRST;V_DATUM FIRST;VEL_UNIT FIRST;VELOCITY FIRST;VERSION_ID FIRST;ZONE_SUBTY FIRST", "SINGLE_PART", "DISSOLVE_LINES")
    except:
        tenpct = arcpy.analysis.PairwiseDissolve(poly10_merge, os.path.join(out_path, 'TENPCT_FP_DissolveX'), None, "AR_REVERT FIRST;AR_SUBTRV FIRST;BFE_REVERT FIRST;DEP_REVERT FIRST;DEPTH FIRST;DUAL_ZONE FIRST;EST_AR_ID FIRST;EST_ID FIRST;EST_Risk FIRST;FLD_ZONE FIRST;LEN_UNIT FIRST;OBJECTID FIRST;SFHA_TF FIRST;Shape_Area FIRST;Shape_Length FIRST;SOURCE_CIT FIRST;STATIC_BFE FIRST;STUDY_TYP FIRST;V_DATUM FIRST;VEL_UNIT FIRST;VELOCITY FIRST;VERSION_ID FIRST;ZONE_SUBTY FIRST", "SINGLE_PART")

    '''
    try:
        tenclip = arcpy.analysis.PairwiseClip(tenpct, os.path.join(out_path, 'HUC8_ClipX'), os.path.join(out_path, 'TENPCT_FPX'))
    except:
        tenclip = arcpy.analysis.Clip(tenpct, os.path.join(out_path, 'HUC8_ClipX'), os.path.join(out_path, 'TENPCT_FPX'))'''
    arcpy.management.Append(tenpct, os.path.join(out_path, 'EBFE_Dataset\TENPCT_FP'), "NO_TEST", f'EST_ID "EST_ID" true true false 20 Text 0 0,First,#,{tenpct},FIRST_EST_ID,0,20;VERSION_ID "VERSION_ID" true true false 11 Text 0 0,First,#,{tenpct},FIRST_VERSION_ID,0,11;EST_AR_ID "EST_AR_ID" true true false 25 Text 0 0,First,#,{tenpct},FIRST_EST_AR_ID,0,25;V_DATUM "V_DATUM" true true false 17 Text 0 0,First,#,{tenpct},FIRST_V_DATUM,0,17;LEN_UNIT "LEN_UNIT" true true false 16 Text 0 0,First,#,{tenpct},FIRST_LEN_UNIT,0,16;SOURCE_CIT "SOURCE_CIT" true true false 15 Text 0 0,First,#,{tenpct},FIRST_SOURCE_CIT,0,15;EST_Risk "EST_Risk" true true false 30 Text 0 0,First,#,{tenpct},FIRST_EST_Risk,0,30;STUDY_TYP "STUDY_TYP" true true false 28 Text 0 0,First,#,{tenpct},FIRST_STUDY_TYP,0,28;SFHA_TF "SFHA_TF" true true false 1 Text 0 0,First,#,{tenpct},FIRST_SFHA_TF,0,1;ZONE_SUBTY "ZONE_SUBTY" true true false 72 Text 0 0,First,#,{tenpct},FIRST_ZONE_SUBTY,0,72;STATIC_BFE "STATIC_BFE" true true false 8 Double 0 0,First,#,{tenpct},FIRST_STATIC_BFE,-1,-1;DEPTH "DEPTH" true true false 8 Double 0 0,First,#,{tenpct},FIRST_DEPTH,-1,-1;VELOCITY "VELOCITY" true true false 8 Double 0 0,First,#,{tenpct},FIRST_VELOCITY,-1,-1;VEL_UNIT "VEL_UNIT" true true false 20 Text 0 0,First,#,{tenpct},FIRST_VEL_UNIT,0,20;AR_REVERT "AR_REVERT" true true false 17 Text 0 0,First,#,{tenpct},FIRST_AR_REVERT,0,17;AR_SUBTRV "AR_SUBTRV" true true false 72 Text 0 0,First,#,{tenpct},FIRST_AR_SUBTRV,0,72;BFE_REVERT "BFE_REVERT" true true false 8 Double 0 0,First,#,{tenpct},FIRST_BFE_REVERT,-1,-1;DEP_REVERT "DEP_REVERT" true true false 8 Double 0 0,First,#,{tenpct},FIRST_DEP_REVERT,-1,-1;DUAL_ZONE "DUAL_ZONE" true true false 1 Text 0 0,First,#,{tenpct},FIRST_DUAL_ZONE,0,1;FLD_ZONE "FLD_ZONE" true true false 17 Text 0 0,First,#,{tenpct},FIRST_FLD_ZONE,0,17', '', '')
    try:
        mergeAX("'A'", gdbs, out_path)
    except:
        mergeAX_repair("'A'", gdbs, out_path)
    try:
        mergeAX("'X'", gdbs, out_path)
    except:
        mergeAX_repair("'X'", gdbs, out_path)
        
    to_delete = arcpy.ListFeatureClasses("*X")
    for fc in to_delete:
        arcpy.management.Delete(os.path.join(out_path, fc))
    '''    
    to_delete = arcpy.ListRasters("*X")
    for i in to_delete:
        arcpy.Delete_management(os.path.join(out_path, i))'''
        
if __name__ == '__main__':

    if arcpy.CheckExtension("Spatial") == "Available":
        arcpy.CheckOutExtension("Spatial")

        gdbs = arcpy.GetParameterAsText(0).split(";")
        arcpy.AddMessage(gdbs)
        gdb_name = arcpy.GetParameterAsText(1)
        out_folder = arcpy.GetParameterAsText(2)
        merge_huc10(gdbs, out_folder, gdb_name)

        arcpy.CheckInExtension("Spatial")

    else:
        msg = "Spatial Analyst license is required for this tool and at this time it is NOT available"
        arcpy.AddError(msg)
        sys.exit(msg)
