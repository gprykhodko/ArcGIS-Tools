import arcpy, os

def grid_containment_check(grids, in_gdb, report_file):
    arcpy.SetProgressorLabel('Performing grid containment check.....')
    arcpy.AddMessage('Performing grid containment check.....')
    grids_path = [os.path.join(in_gdb, grids[0]), os.path.join(in_gdb, grids[1])]
    with arcpy.EnvManager(snapRaster=grids_path[1]):
        grid_check = arcpy.sa.SetNull(~(arcpy.sa.IsNull(grids_path[1])),  grids_path[0])
    if not grid_check.mean:
        extent_compare = f'\n{grids[0]} does NOT extend outside of {grids[1]}'
        arcpy.SetProgressorLabel(f'{grids[0]} does NOT extend outside of {grids[1]}.....')
        arcpy.AddMessage(f'{grids[0]} does NOT extend outside of {grids[1]}.....')
    elif grid_check.mean:
        extent_compare = f'\n{grids[0]} extends outside of {grids[1]}'
        arcpy.SetProgressorLabel(f'{grids[0]} extends outside of {grids[1]}.....')
        arcpy.AddMessage(f'{grids[0]} extends outside of {grids[1]}.....')
    with open(report_file, "a") as report:
                report.write(extent_compare)
    return grid_check

def grid_value_check(grids, in_gdb, report_file):
    arcpy.SetProgressorLabel('Performing grid value check.....')
    arcpy.AddMessage('Performing grid value check.....')
    grids_path = [os.path.join(in_gdb, grids[0]), os.path.join(in_gdb, grids[1])]
    with arcpy.EnvManager(snapRaster=grids_path[1]):
        value_check = arcpy.sa.Minus(grids_path[0], grids_path[1])
#     if value_check.minimum > 0:
#         value_compare = '\nNo negative values for 1% grids'
    if value_check.minimum < 0:
        value_compare = f'\n{grids[1]} values greater than WSE values.'
        arcpy.AddMessage(value_compare)
        with open(report_file, "a") as report:
            report.write(value_compare)
    arcpy.management.Delete(value_check)
    #return value_compare

def snapping_check(grids, in_gdb, report_file):
    arcpy.SetProgressorLabel('Performing grid extent check.....')
    arcpy.AddMessage('Performing grid extent check.....')
    grids_path = [os.path.join(in_gdb, grids[0]), os.path.join(in_gdb, grids[1])]
    feature_compare = []
    for path, grid_name in zip(grids_path, grids):
        with arcpy.EnvManager(snapRaster=path):
            con_raster = arcpy.sa.Con(path, 0, None, '')
        poly = arcpy.conversion.RasterToPolygon(con_raster, os.path.join(scratch_gdb, grid_name+'_Poly'), "NO_SIMPLIFY", "Value", "SINGLE_OUTER_PART", None)
        feature_compare.append(poly)
    snap_compare = arcpy.management.FeatureCompare(feature_compare[0], feature_compare[1], "OBJECTID", "GEOMETRY_ONLY", "IGNORE_M;IGNORE_Z;IGNORE_POINTID;IGNORE_EXTENSION_PROPERTIES;IGNORE_SUBTYPES;IGNORE_RELATIONSHIPCLASSES;IGNORE_REPRESENTATIONCLASSES;IGNORE_FIELDALIAS", "0.003280833333 Feet", 0.001, 0.001, None, None, "CONTINUE_COMPARE", None)
    messages = snap_compare.getMessages()
    if 'Geometries are different' in messages:
        print(f'{grids[0]} and {grids[1]} are not snapped to each other')
        snap_compare = f'\n{grids[0]} and {grids[1]} extents are different'
        arcpy.AddMessage(snap_compare)
        with open(report_file, "a") as report:
            report.write(snap_compare)
    return feature_compare

def grid_vs_poly(grid, fld_haz_layer, fld_zone=None):
    if fld_zone:
        fld_haz_layer.getOutput(0).definitionQuery = f"FLD_ZONE = '{fld_zone}'"
    grid_layer = arcpy.MakeFeatureLayer_management(grid, "Grid_Layer")
    missing_polys = arcpy.management.SelectLayerByLocation(grid_layer, "INTERSECT", fld_haz_layer, None, "NEW_SELECTION", "INVERT")
    return len(missing_polys.getOutput(0).getSelectionSet())
           
               
if __name__ == '__main__':
    
    in_gdb = arcpy.GetParameterAsText(0)
    report_file = arcpy.GetParameterAsText(1)
    arcpy.env.workspace = in_gdb
    scratch_gdb = arcpy.env.scratchWorkspace
    feature_datasets = arcpy.ListDatasets({}, "Feature")
    features = [(ds, fc) for ds in feature_datasets for fc in arcpy.ListFeatureClasses(feature_dataset = ds)]
    raster_datasets = arcpy.ListDatasets({}, "Raster")
    rasters = [raster for raster in raster_datasets]
    with open(report_file, "a") as report:
            report.write('\n-----------------------------------------------\nTool 5 - Results:\n-----------------------------------------------')
    if ('BLE_WSE_01PCT' or 'BLE_WSE0_2PCT') not in rasters: 
        arcpy.AddMessage('One or more WSE grids are missing from the database')
    if ('BLE_DEP_01PCT' or 'BLE_DEP0_2PCT') not in rasters:
        arcpy.AddMessage('One or more depth grids are missing from the database')
    #extent comparison
    if 'BLE_DEP_01PCT' and 'BLE_DEP0_2PCT' in rasters:
        arcpy.SetProgressorLabel('Checking if depth grids are in the database.....')
        arcpy.AddMessage('Checking if depth grids are in the database.....')
        grids = ['BLE_DEP_01PCT', 'BLE_DEP0_2PCT']
        depth_check = grid_containment_check(grids, in_gdb, report_file)
        depth_check.save(os.path.join(scratch_gdb, 'Depth_Grid_Compare'))

        
    if 'BLE_WSE_01PCT' and 'BLE_WSE0_2PCT' in rasters:
        arcpy.SetProgressorLabel('Checking if WSE grids are in the database.....')
        arcpy.AddMessage('Checking if WSE grids are in the database.....')
        grids = ['BLE_WSE_01PCT', 'BLE_WSE0_2PCT']
        wse_check = grid_containment_check(grids, in_gdb, report_file)
        wse_check.save(os.path.join(scratch_gdb, 'WSE_Grid_Compare'))

        
    #grid value check for positive values and correctly labeled datasets and snapping check
    if 'BLE_WSE_01PCT' and 'BLE_DEP_01PCT' in rasters:
        grids = ['BLE_WSE_01PCT', 'BLE_DEP_01PCT']
        value_check = grid_value_check(grids, in_gdb, report_file)
        polys_100 = snapping_check(grids, in_gdb, report_file)
    if 'BLE_WSE0_2PCT' and 'BLE_DEP0_2PCT' in rasters:
        grids = ['BLE_WSE0_2PCT','BLE_DEP0_2PCT']
        value_check = grid_value_check(grids, in_gdb, report_file)
        polys_500 = snapping_check(grids, in_gdb, report_file)

    try:
        feature_datasets = arcpy.ListDatasets({}, "Feature")
        features = [(ds, fc) for ds in feature_datasets for fc in arcpy.ListFeatureClasses(feature_dataset = ds)]
        fld_index = [i[1] for i in features].index('FLD_HAZ_AR')
        fld_feature = os.path.join(in_gdb, features[fld_index][0], features[fld_index][1])
        fld_haz_layer = arcpy.MakeFeatureLayer_management(fld_feature, "FLD_HAZ_AR")

        missing_polys_100 = grid_vs_poly(polys_100[0], fld_haz_layer, 'A')
        if missing_polys_100 > 0:
            with open(report_file, "a") as report:
                report.write(f'{missing_polys_100} features are missing from 100-yr FLD_HAZ_AR')
    
            arcpy.AddMessage(f'{missing_polys_100} features are missing from 100-yr FLD_HAZ_AR')
        
        fld_haz_layer = arcpy.MakeFeatureLayer_management(fld_feature, "FLD_HAZ_AR")   
        missing_polys_500 = grid_vs_poly(polys_500[0], fld_haz_layer)
        if missing_polys_500 > 0:
            with open(report_file, "a") as report:
                report.write(f'{missing_polys_500} features are missing from 500-yr FLD_HAZ_AR')
            
            arcpy.AddMessage(f'{missing_polys_500} features are missing from 500-yr FLD_HAZ_AR')
    
    except:
        arcpy.AddMessage('Unable to compare grids to FLD_HAZ_AR. Check the flood risk database for any missing items')
    
    with arcpy.EnvManager(workspace = arcpy.env.scratchWorkspace):
        to_delete = arcpy.ListFeatureClasses("*X")
        for fc in to_delete:
            arcpy.management.Delete(os.path.join(arcpy.env.scratchWorkspace, fc))
