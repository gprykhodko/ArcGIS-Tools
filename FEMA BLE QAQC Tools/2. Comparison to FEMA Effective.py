########################################################################################
# Tool Name: Comparison to FEMA Effective
# Version: 
# Use: 
#      
#      
# Input parameters:  
#                    
#                   
# Author: Gennadii Prykhodko, Halff Accociates, Inc., 2022
########################################################################################
import arcpy, os, zipfile
import pandas as pd
from arcgis.gis import GIS
arcpy.env.overwriteOutput = True
arcpy.env.addOutputsToMap = False
# Download and extract the data
def unzip_data(portal, item_id):
    arcpy.SetProgressorLabel('Getting FEMA effective data...')
    arcpy.AddMessage('Getting FEMA effective data...')
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
        arcpy.AddMessage(f'Error unzipping file: {e}')
    return downloaded_gdb
def nfhl_compare(test_feature, feature_type, report_file):
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
        if arcpy.Exists(os.path.join(scratch_gdb, "NFHL_ProjectX")):
            nfhl_project = os.path.join(scratch_gdb, "NFHL_ProjectX")
        if arcpy.Exists(os.path.join(scratch_gdb, "NFHL_ClipedX")):
            nfhl_clip = os.path.join(scratch_gdb, "NFHL_ClipedX")
        else:
            nfhl_fl = os.path.join(unzip_data(fema_portal, item_id), 'NFHL')
            nfhl_project = arcpy.management.Project(nfhl_fl, os.path.join(scratch_gdb, "NFHL_ProjectX"), huc_sr, None, None, "NO_PRESERVE_SHAPE", None, "NO_VERTICAL")
            nfhl_clip = arcpy.analysis.PairwiseClip(nfhl_project, huc8_feature, os.path.join(scratch_gdb, "NFHL_ClipedX"), None)
    #message = nfhl_clip.getMessages(1)
    #if 'empty output' in message:
        #nfhl_compare = 'There are no detailed studies in this watershed'
        #print(message)
    dtl_layer = arcpy.management.MakeFeatureLayer(test_feature, os.path.basename(test_feature))
    nfhl_layer = arcpy.management.MakeFeatureLayer(nfhl_clip, "NFHL_Clipped")
    arcpy.SetProgressorLabel(f"Comparing {os.path.basename(test_feature)} to FEMA effective....")
    arcpy.AddMessage(f"Comparing {os.path.basename(test_feature)} to FEMA effective....")
    compare_layer = arcpy.management.SelectLayerByLocation(dtl_layer.getOutput(0), "INTERSECT", nfhl_layer.getOutput(0), None, "NEW_SELECTION", "NOT_INVERT")
    dtl_count = len(compare_layer.getOutput(0).getSelectionSet())
    nfhl_count = arcpy.management.GetCount(nfhl_clip).outputCount
    df = pd.read_csv(report_file, '\t')
    if dtl_count == nfhl_count:
        nfhl_compare = f'There are no missing {os.path.basename(test_feature)} {feature_type} in the database'
        df.loc[df["Item Name"] == os.path.basename(test_feature), 'NFHL Spatial Check'] = 'Pass'
        print(nfhl_compare)
    elif dtl_count > nfhl_count:
        nfhl_compare = f'There are {dtl_count - nfhl_count} extra {os.path.basename(test_feature)} {feature_type} in the database'
        df.loc[df["Item Name"] == os.path.basename(test_feature), 'NFHL Spatial Check'] = 'Fail'
        print(nfhl_compare)
    elif dtl_count < nfhl_count:
        nfhl_compare = f'There are {nfhl_count - dtl_count} missing {os.path.basename(test_feature)} {feature_type} in the database'
        df.loc[df["Item Name"] == os.path.basename(test_feature), 'NFHL Spatial Check'] = 'Fail'
        print(nfhl_compare)
    df.to_csv(report_file, sep='\t', index=False)
    with open(report_file, "a") as report:
        report.write(nfhl_compare)
if __name__ == '__main__':
    
    in_gdb = arcpy.GetParameterAsText(0)
    report_file = arcpy.GetParameterAsText(1)
    fema_portal = r"https://fema.maps.arcgis.com/"
    item_id = '491035bd63624dd6b7181016736c4da6'  
    arcpy.env.workspace = in_gdb
    scratch_gdb = arcpy.env.scratchWorkspace
    feature_datasets = arcpy.ListDatasets({}, "Feature")
    features = [(ds, fc) for ds in feature_datasets for fc in arcpy.ListFeatureClasses(feature_dataset = ds)]
    if 'DTL_STUD_AR' or 'DTL_STUD_LN' in [i[1] for i in features]:
        with open(report_file, "a") as report:
            report.write('\n-----------------------------------------------\nTool 2 - Results:\n-----------------------------------------------')
    if 'DTL_STUD_AR' in [i[1] for i in features]:
        nfhl_compare(test_feature='DTL_STUD_AR', feature_type='polygons', report_file=report_file)
    if 'DTL_STUD_LN' in [i[1] for i in features]:
        nfhl_compare(test_feature='DTL_STUD_LN', feature_type='lines', report_file=report_file)
    with open(report_file, "a") as report:
        report.write('\nManual review of DTL_STUD_AR polygons compared to BLE extents required')
    arcpy.SetParameterAsText(2, report_file)
    arcpy.AddMessage('Comaprison to FEMA effective is complete.....')
    with arcpy.EnvManager(workspace = arcpy.env.scratchWorkspace):
        to_delete = arcpy.ListFeatureClasses("*X")
        for fc in to_delete:
            arcpy.management.Delete(os.path.join(arcpy.env.scratchWorkspace, fc))
    if 'DTL_STUD_AR' and 'DTL_STUD_LN' not in [i[1] for i in features]: 
        arcpy.AddMessage('There are no detailed studies features in the database.....')
