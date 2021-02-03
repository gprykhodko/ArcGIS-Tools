import arcpy, os, tempfile, shutil
import numpy as np

arcpy.env.overwriteOutput = True
arcpy.env.addOutputsToMap = False

def createTileList():

    try:
        arcpy.management.SelectLayerByLocation(lidar, "INTERSECT", huc8, 
                                       "1000 Meters", "NEW_SELECTION", "NOT_INVERT")
    finally:
        outLocation = tempfile.gettempdir()
        outName = "DEM_names.txt"

        fms = arcpy.FieldMappings()
        demName = arcpy.FieldMap()
        dirName = arcpy.FieldMap()
        demName.addInputField(lidar, "demname")
        dirName.addInputField(lidar, "dirname")
        fms.addFieldMap(demName)
        fms.addFieldMap(dirName)
        dems = arcpy.conversion.TableToTable(lidar, outLocation, outName, '', fms, '')

        return dems

def downloadTiles(tileList):
    
    objID, demName, dirName = np.loadtxt(str(tileList), skiprows=1, unpack=True, delimiter=",", dtype=str)
    del objID
    dirNames, counts = np.unique(dirName, return_counts=True)
    dirNamesSort = np.sort(dirName)
    demNameSort = np.sort(demName)
    numberOfDirectories = counts.size
    
    for i in range(numberOfDirectories):

        dr = f'\\\gorgoroth\\data\\{dirNames[i]}\\dem\\'
        for FileName in demNameSort:
            match = [f for f in os.listdir(dr) if any([f == FileName, f.startswith(FileName+".")])]
            if match:
                match = match[0]
                shutil.copy(os.path.join(dr, match), os.path.join(out_path, match))


if __name__ == '__main__':


    huc8 = arcpy.GetParameterAsText(1)
    lidar = arcpy.GetParameterAsText(0)
    out_path = arcpy.GetParameterAsText(2)

    tileList = createTileList()
    downloadTiles(tileList)

            
