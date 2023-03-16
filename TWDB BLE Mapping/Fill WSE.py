import arcpy, os, re

arcpy.env.overwriteOutput = True
arcpy.env.addOutputsToMap = False

def create_wse_list(dr):
    dir_match = [root for root, dirs, files in os.walk(dr)]
    match = [os.path.join(folder, file) for folder in dir_match for file in os.listdir(folder) if 'WSE' in file and file.endswith('SL.tif')]
    return match

def create_raster_list(dr):
    dir_match = [root for root, dirs, files in os.walk(dr)]
    match = [os.path.join(folder, file) for folder in dir_match for file in os.listdir(folder) if any(['Depth' in file, 'DPT' in file]) and file.endswith('tif')]
    return match

def fill_wse(in_wse):
    #wse_100 = arcpy.management.MosaicToNewRaster([in_wse[0], in_wse[1]], out_path, "BLE_WSE_01PCTX", None, "32_BIT_FLOAT", None, 1, "LAST", "FIRST")
    #wse_500 = arcpy.management.MosaicToNewRaster([wse_100, in_wse[1]], out_path, "BLE_WSE0_2PCTX", None, "32_BIT_FLOAT", None, 1, "LAST", "FIRST")
    for wse, dpt, name in zip([in_wse[1], in_wse[2]], [os.path.join(out_path, "BLE_DEP_01PCT"),os.path.join(out_path, "BLE_DEP0_2PCT")], ['BLE_WSE_01PCT','BLE_WSE0_2PCT']):
        print(wse)
        wse = arcpy.Raster(wse)
        arcpy.env.snapRaster = dpt
        out_evf = arcpy.ia.ElevationVoidFill(wse, 0)
        out_raster = arcpy.sa.ExtractByMask(out_evf, dpt)
        out_raster = (arcpy.sa.Int(out_raster*10 + 0.5))/10
        out_raster.save(os.path.join(out_path, name))
    to_delete = arcpy.ListRasters("*X")
    for i in to_delete:
        arcpy.Delete_management(os.path.join(out_path, i))



if __name__ == '__main__':

    if arcpy.CheckExtension("Spatial") == "Available":
        arcpy.CheckOutExtension("Spatial")
        
        dr = arcpy.GetParameterAsText(0)# from modelers folder
        out_path = arcpy.GetParameterAsText(1) #in huc8 gdb which is also out gdb
        arcpy.env.workspace = out_path
        arcpy.env.scratchWorkspace = out_path
        in_wse = create_wse_list(dr)
        in_wse.sort(key=lambda f: int(re.sub('\D', '', os.path.basename(f))))
        fill_wse(in_wse)

        arcpy.CheckInExtension("Spatial")

    else:
        msg = "Spatial Analyst license is required for Flood Hazard Mapping and at this time it is NOT available"
        arcpy.AddError(msg)
        sys.exit(msg)

