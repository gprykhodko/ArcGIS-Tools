import arcpy
import os
import time

arcpy.AddToolbox("https://hydro.arcgis.com/arcgis/services;Tools/Hydrology", "hydro")
arcpy.env.workspace = arcpy.env.workspace
arcpy.env.overwriteOutput = True
arcpy.env.addOutputsToMap = False
fc = arcpy.GetParameterAsText(0)
Station_ID = arcpy.GetParameterAsText(1)

out_fc = arcpy.env.workspace
expression = '!{0}!.replace("-", "").replace(" ","")'.format(Station_ID)
arcpy.CalculateField_management(fc, Station_ID, 
                                expression, "PYTHON")
field = arcpy.ListFields(fc, Station_ID)
with arcpy.da.SearchCursor(fc, ["SHAPE@", Station_ID]) as cursor_fc:
    for row_fc in cursor_fc:
        out_path = os.path.join(out_fc, row_fc[1])
        result = arcpy.Watershed_hydro(InputPoints=row_fc[0],
PointIDField="", SnapDistance="", SnapDistanceUnits="Meters", DataSourceResolution="FINEST", Generalize=False,
ReturnSnappedPoints=False)
        
        while result.status < 4:
            time.sleep(0.1)
        arcpy.management.CopyFeatures(result.getOutput(0), out_path)

del fc, out_fc, cursor_fc, out_path, result

file_name_field = 'Station_ID'

feature_classes = arcpy.ListFeatureClasses()

for fc in feature_classes:
    print(fc) # just so you know what the script is processing
    
    # add field to hold the file name if it does not exist
    existing_fields = [f.name for f in arcpy.ListFields(fc)]
    if file_name_field not in existing_fields:
        arcpy.management.AddField(fc, file_name_field, 'TEXT', field_length=200)
    
    # write the file name into each row of the file name filed
    with arcpy.da.UpdateCursor(fc, [file_name_field]) as uc:
        for row in uc:
            uc.updateRow([str(fc)])
    del row, uc

