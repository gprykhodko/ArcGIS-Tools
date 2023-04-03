import arcpy, os, zipfile
import pandas as pd
from arcgis.gis import GIS

arcpy.env.overwriteOutput = True
arcpy.env.addOutputsToMap = False

def unzip_data(portal, item_id):
    arcpy.SetProgressorLabel('Getting NHD data...')
    arcpy.AddMessage('Getting NHD data...')
    try:     
        #downloads_path = str(Path.home() / "Downloads")    # path to downloads folder
        data_dir = os.path.join(os.path.dirname(in_gdb), 'BLE_QAQC_Data')
        if os.path.isdir(data_dir):
            downloaded_gdb = os.path.join(data_dir, 'BLE-QAQC-Tools-Data.gdb')
        else:
            gis = GIS(portal)
            tool_data = gis.content.get(item_id)
            os.makedirs(data_dir)
            zipped_tool_data = tool_data.download(data_dir)    # download the data item
            z = zipfile.ZipFile(zipped_tool_data)
            z.extractall(data_dir)
            downloaded_gdb = os.path.join(data_dir, 'BLE-QAQC-Tools-Data.gdb')       
    except Exception as e:
        arcpy.AddMessage(f'Error getting data: {e}')
    return downloaded_gdb


def nhd_compare(test_feature, report_file):
    try: 
        huc8_index = [i[1] for i in features].index('S_HUC_Ar')
        huc8_feature = os.path.join(in_gdb, features[huc8_index][0], features[huc8_index][1])
    except:
        huc8_feature = os.path.join(unzip_data(fema_portal, item_id), 'WBDHU8')
        huc8_layer = arcpy.MakeFeatureLayer_management(huc8_feature, "WBDHU8")
        huc8_layer = arcpy.management.SelectLayerByLocation(huc8_layer.getOutput(0), "INTERSECT", test_feature, "-1 Miles", "NEW_SELECTION", "NOT_INVERT")
        test_feature_sr = arcpy.Describe(test_feature).spatialReference
        with arcpy.EnvManager(outputCoordinateSystem=test_feature_sr):
            huc8_feature = arcpy.conversion.FeatureClassToFeatureClass(huc8_layer, scratch_gdb, "HUC8_BaseFeatureX")
    test_index = [i[1] for i in features].index(test_feature)
    test_feature = os.path.join(in_gdb, features[test_index][0], features[test_index][1])
    huc_sr = arcpy.Describe(huc8_feature).spatialReference
    
    with arcpy.EnvManager(workspace = arcpy.env.scratchWorkspace):
        if arcpy.Exists(os.path.join(scratch_gdb, "NHD_ProjectX")):
            nhd_project = os.path.join(scratch_gdb, "NHD_ProjectX")
        if arcpy.Exists(os.path.join(scratch_gdb, "NHD_ClipedX")):
            nhd_clip = os.path.join(scratch_gdb, "NHD_ClipedX")
        else:
            nhd_fl = os.path.join(unzip_data(fema_portal, item_id), 'NHD')
            nhd_project = arcpy.management.Project(nhd_fl, os.path.join(scratch_gdb, "NHD_ProjectX"), huc_sr, None, None, "NO_PRESERVE_SHAPE", None, "NO_VERTICAL")
            nhd_clip = arcpy.analysis.PairwiseClip(nhd_project, huc8_feature, os.path.join(scratch_gdb, "NHD_ClipedX"), None)

    wtr_layer = arcpy.MakeFeatureLayer_management(test_feature, os.path.basename(test_feature))
    nhd_layer = arcpy.MakeFeatureLayer_management(nhd_clip, "NHD_Clipped")

    compare_layer = arcpy.management.SelectLayerByLocation(nhd_layer.getOutput(0), "INTERSECT", wtr_layer.getOutput(0), None, "NEW_SELECTION", "INVERT")
    nhdX = arcpy.conversion.FeatureClassToFeatureClass(compare_layer.getOutput(0), scratch_gdb, "nhdX")
    nhdX_layer = arcpy.MakeFeatureLayer_management(nhdX, "nhdX")
    nhdX_count = len(compare_layer.getOutput(0).getSelectionSet())
    arcpy.management.CalculateGeometryAttributes(nhdX_layer.getOutput(0), "AreaSqFt AREA_GEODESIC", '', '', None, "SAME_AS_INPUT")
    nhdX_max = arcpy.management.SelectLayerByAttribute(nhdX_layer.getOutput(0), "NEW_SELECTION", "AreaSqFt = (SELECT MAX(AreaSqFt) FROM nhdX)", None)
    arr = arcpy.da.FeatureClassToNumPyArray(nhdX_max, "AreaSqFt")
    nhd_max_ft = f'{round(arr["AreaSqFt"][0]):,}' + ' sq.ft'
    nhd_max_acres = f'{round(arr["AreaSqFt"][0]/43560):,}' + ' acres'
    nhd_compare = f'There are {nhdX_count} missing WTR_AR polygons with the max area of {nhd_max_ft} or {nhd_max_acres}'
    print(nhd_compare)
    wtr_layer = arcpy.MakeFeatureLayer_management(test_feature, os.path.basename(test_feature))
    nhd_layer = arcpy.MakeFeatureLayer_management(nhd_clip, "NHD_Clipped")
    compare_layer = arcpy.management.SelectLayerByLocation(wtr_layer.getOutput(0), "INTERSECT", nhd_layer.getOutput(0), None, "NEW_SELECTION", "INVERT")
    wtrX = arcpy.conversion.FeatureClassToFeatureClass(compare_layer.getOutput(0), scratch_gdb, "wtrX")
    wtrX_layer = arcpy.MakeFeatureLayer_management(nhdX, "nhdX")
    wtrX_count = len(compare_layer.getOutput(0).getSelectionSet())
    wtr_compare = f'\nThere are {wtrX_count} extra WTR_AR polygons'
    print(wtr_compare)
    
    df = pd.read_csv(report_file, '\t')
    if nhd_compare and wtr_compare == 0:
        
        df.loc[df["Item Name"] == os.path.basename(test_feature), 'Waterbodies Check'] = 'Pass'
        
    else:

        df.loc[df["Item Name"] == os.path.basename(test_feature), 'Waterbodies Check'] = 'Fail'

    df.to_csv(report_file, sep='\t', index=False)
    with open(report_file, "a") as report:
        report.write(nhd_compare)
        report.write(wtr_compare)

if __name__ == '__main__':
    
    in_gdb = arcpy.GetParameterAsText(0)
    report_file = arcpy.GetParameterAsText(1)
    fema_portal = r"https://fema.maps.arcgis.com/"
    item_id = '491035bd63624dd6b7181016736c4da6'  
    arcpy.env.workspace = in_gdb
    scratch_gdb = arcpy.env.scratchWorkspace
    feature_datasets = arcpy.ListDatasets({}, "Feature")
    features = [(ds, fc) for ds in feature_datasets for fc in arcpy.ListFeatureClasses(feature_dataset = ds)]
    if 'WTR_AR' in [i[1] for i in features]:
        print('Located WTR_AR in the database')
        with open(report_file, "a") as report:
            report.write('\n-----------------------------------------------\nTool 4 - Results:\n-----------------------------------------------')
        nhd_compare('WTR_AR', report_file)

    with arcpy.EnvManager(workspace = arcpy.env.scratchWorkspace):
        to_delete = arcpy.ListFeatureClasses("*X")
        for fc in to_delete:
                arcpy.management.Delete(os.path.join(arcpy.env.scratchWorkspace, fc))
    if 'WTR_AR' not in [i[1] for i in features]: 
        arcpy.AddMessage('BFE_2D is missing from the database')

