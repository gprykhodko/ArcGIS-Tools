########################################################################################
# Tool Name: Feature, Schema Check
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
def get_feature_service(url_fl, fc_name, scratch_gdb):
    gis = GIS(r"https://devportal.halff.com/portaldev")
    fl = FeatureLayer(url_fl)
    fs = fl.query()
    fs.save(scratch_gdb, fc_name)
    fc = os.path.join(scratch_gdb, fc_name)
    return fc
# Download and extract the data
def unzip_data(portal, item_id):
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
        print(f'Error unzipping file: {e}')
    return downloaded_gdb
def frd_check(report_file):
    arcpy.SetProgressorLabel("Reading geodatabase items....")
    arcpy.AddMessage("Reading geodatabase items....")
    feature_datasets = arcpy.ListDatasets({}, "Feature")
    raster_datasets = arcpy.ListDatasets({}, "Raster")
    tables = arcpy.ListTables()
    features = [(ds, fc) for ds in feature_datasets for fc in arcpy.ListFeatureClasses(feature_dataset = ds)]
    rasters = [(raster, raster) for raster in raster_datasets]
    tables = [("NA", table) for table in tables]
    
    all_db_items = features + rasters + tables
    control_items = [('EBFE_Dataset', 'XS_1D'), 
                 ('EBFE_Dataset', 'DTL_STUD_LN'), 
                 ('EBFE_Dataset', 'DTL_STUD_AR'), 
                 ('EBFE_Dataset', 'WTR_AR'), 
                 ('EBFE_Dataset', 'WTR_LN'), 
                 ('EBFE_Dataset', 'BFE_2D'), 
                 ('EBFE_Dataset', 'SUBBASINS'), 
                 ('EBFE_Dataset', 'FLD_HAZ_AR'), 
                 ('EBFE_Dataset', 'TENPCT_FP'),   
                 ('Mit_Haz_Datasets', 'S_AOMI_Pt'), 
                 ('Mit_Haz_Datasets', 'S_AOMI_Ar'), 
                 ('Mit_Haz_Datasets', 'S_FRAC_Ar'), 
                 ('Base_Dataset', 'S_HUC_Ar'), 
                 ('Base_Dataset', 'S_Pol_Ar'), 
                 ('CNMS_Dataset', 'S_Studies_Ln'), 
                 ('CNMS_Dataset', 'S_UnMapped_Ln'),    
                 ('BLE_DEP0_2PCT', 'BLE_DEP0_2PCT'), 
                 ('BLE_DEP_01PCT', 'BLE_DEP_01PCT'), 
                 ('BLE_WSE0_2PCT', 'BLE_WSE0_2PCT'), 
                 ('BLE_WSE_01PCT', 'BLE_WSE_01PCT'),
                 ('NA', 'L_Source_Cit')]
    control = {('EBFE_Dataset', 'TENPCT_FP'): [('OBJECTID', '<i4'), ('SHAPE', '<f8', (2,)), ('EST_ID', '<U20'), ('VERSION_ID', '<U11'), ('EST_AR_ID', '<U25'), ('V_DATUM', '<U17'), ('LEN_UNIT', '<U16'), ('SOURCE_CIT', '<U15'), ('EST_Risk', '<U30'), ('STUDY_TYP', '<U28'), ('SFHA_TF', '<U1'), ('ZONE_SUBTY', '<U72'), ('STATIC_BFE', '<f8'), ('DEPTH', '<f8'), ('VELOCITY', '<f8'), ('VEL_UNIT', '<U20'), ('AR_REVERT', '<U17'), ('AR_SUBTRV', '<U72'), ('BFE_REVERT', '<f8'), ('DEP_REVERT', '<f8'), ('DUAL_ZONE', '<U1'), ('FLD_ZONE', '<U17'), ('SHAPE_Length', '<f8'), ('SHAPE_Area', '<f8')], ('EBFE_Dataset', 'FLD_HAZ_AR'): [('OBJECTID', '<i4'), ('SHAPE', '<f8', (2,)), ('EST_ID', '<U20'), ('VERSION_ID', '<U11'), ('EST_AR_ID', '<U25'), ('ZONE_SUBTY', '<U72'), ('V_DATUM', '<U17'), ('LEN_UNIT', '<U16'), ('SOURCE_CIT', '<U15'), ('EST_Risk', '<U30'), ('STUDY_TYP', '<U28'), ('SFHA_TF', '<U1'), ('STATIC_BFE', '<f8'), ('DEPTH', '<f8'), ('VELOCITY', '<f8'), ('VEL_UNIT', '<U20'), ('AR_REVERT', '<U17'), ('AR_SUBTRV', '<U72'), ('BFE_REVERT', '<f8'), ('DEP_REVERT', '<f8'), ('DUAL_ZONE', '<U1'), ('FLD_ZONE', '<U17'), ('SHAPE_Length', '<f8'), ('SHAPE_Area', '<f8')], ('EBFE_Dataset', 'SUBBASINS'): [('OBJECTID', '<i4'), ('SHAPE', '<f8', (2,)), ('EST_ID', '<U20'), ('VERSION_ID', '<U11'), ('E_SUBAS_ID', '<U20'), ('HUC8_CODE', '<U8'), ('E_SUBAS_NM', '<U50'), ('EST_AREA', '<f8'), ('AREA_UNIT', '<U50'), ('US_1', '<U20'), ('US_2', '<U20'), ('US_3', '<U20'), ('US_4', '<U20'), ('DS_1', '<U20'), ('PRECIP_IN', '<f8'), ('MAINCHSLP', '<f8'), ('E_Q_10PCT', '<f8'), ('E_Q_04PCT', '<f8'), ('E_Q_02PCT', '<f8'), ('E_Q_01PCT', '<f8'), ('E_Q_01PLUS', '<f8'), ('E_Q_01MIN', '<f8'), ('E_Q_0_2PCT', '<f8'), ('SOURCE_CIT', '<U50'), ('WTR_NM', '<U100'), ('BASIN_DESC', '<U254'), ('NODE_ID', '<U25'), ('BASIN_TYP', '<U19'), ('SHAPE_Length', '<f8'), ('SHAPE_Area', '<f8')], ('EBFE_Dataset', 'BFE_2D'): [('OBJECTID', '<i4'), ('SHAPE', '<f8', (2,)), ('EST_ID', '<U20'), ('VERSION_ID', '<U11'), ('EBFE_LN_ID', '<U25'), ('BLELEV1PCT', '<i4'), ('BFE_LN_TYP', '<U24'), ('LEN_UNIT', '<U16'), ('V_DATUM', '<U17'), ('SOURCE_CIT', '<U11'), ('SHAPE_Length', '<f8')], ('EBFE_Dataset', 'WTR_LN'): [('OBJECTID', '<i4'), ('SHAPE', '<f8', (2,)), ('EST_ID', '<U20'), ('VERSION_ID', '<U11'), ('WTR_LN_ID', '<U25'), ('WTR_NM', '<U100'), ('SOURCE_CIT', '<U11'), ('SHOWN_FIRM', '<U1'), ('SHOWN_INDX', '<U1'), ('SHAPE_Length', '<f8')], ('EBFE_Dataset', 'WTR_AR'): [('OBJECTID', '<i4'), ('SHAPE', '<f8', (2,)), ('EST_ID', '<U20'), ('VERSION_ID', '<U11'), ('WTR_AR_ID', '<U25'), ('WTR_NM', '<U100'), ('SOURCE_CIT', '<U11'), ('SHOWN_FIRM', '<U1'), ('SHOWN_INDX', '<U1'), ('SHAPE_Length', '<f8'), ('SHAPE_Area', '<f8')], ('EBFE_Dataset', 'DTL_STUD_AR'): [('OBJECTID', '<i4'), ('SHAPE', '<f8', (2,)), ('DTL_AR_ID', '<U8'), ('VERSION_ID', '<U11'), ('EFF_DATE', '<M8[us]'), ('FIRM_PAN', '<U15'), ('TYPE', '<U20'), ('CD_YN', '<U10'), ('CD_POC', '<U70'), ('CD_ADD1', '<U150'), ('CD_ADD2', '<U150'), ('CD_CTY', '<U100'), ('CD_STATE', '<U25'), ('CD_ZIP', '<U10'), ('CD_PHONE', '<U20'), ('CD_EMAIL', '<U100'), ('SOURCE_CIT', '<U11'), ('LOMR_ID', '<U25'), ('CASE_NO', '<U13'), ('SCALE', '<U5'), ('STATUS', '<U11'), ('SHAPE_Length', '<f8'), ('SHAPE_Area', '<f8')], ('EBFE_Dataset', 'DTL_STUD_LN'): [('OBJECTID', '<i4'), ('SHAPE', '<f8', (2,)), ('DTL_LN_ID', '<U8'), ('VERSION_ID', '<U11'), ('EFF_DATE', '<M8[us]'), ('FIRM_PAN', '<U15'), ('TYPE', '<U20'), ('CD_YN', '<U10'), ('CD_POC', '<U70'), ('CD_ADD1', '<U150'), ('CD_ADD2', '<U150'), ('CD_CTY', '<U100'), ('CD_STATE', '<U25'), ('CD_ZIP', '<U10'), ('CD_PHONE', '<U20'), ('CD_EMAIL', '<U100'), ('SOURCE_CIT', '<U11'), ('LOMR_ID', '<U25'), ('CASE_NO', '<U13'), ('SCALE', '<U5'), ('STATUS', '<U11'), ('SHAPE_Length', '<f8')], ('EBFE_Dataset', 'XS_1D'): [('OBJECTID', '<i4'), ('SHAPE', '<f8', (2,)), ('EST_ID', '<U20'), ('VERSION_ID', '<U11'), ('XS_LN_ID', '<U25'), ('WTR_NM', '<U100'), ('STREAM_STN', '<f8'), ('START_ID', '<U25'), ('XS_LN_TYP', '<U24'), ('E_WSE_1PCT', '<f8'), ('V_DATUM', '<U14'), ('MODEL_ID', '<U300'), ('SOURCE_CIT', '<U11'), ('E_WSE_10PC', '<f8'), ('E_WSE_4PCT', '<f8'), ('E_WSE_2PCT', '<f8'), ('E_WSE_1PLU', '<f8'), ('E_WSE_1MIN', '<f8'), ('E_WSE_0_2P', '<f8'), ('E_Q_10PCT', '<f8'), ('E_Q_04PCT', '<f8'), ('E_Q_02PCT', '<f8'), ('E_Q_01PCT', '<f8'), ('E_Q_01PLUS', '<f8'), ('E_Q_01MIN', '<f8'), ('E_Q_0_2PCT', '<f8'), ('XS_LTR', '<U12'), ('STRMBED_EL', '<f8'), ('LEN_UNIT', '<U16'), ('SHAPE_Length', '<f8')], ('Mit_Haz_Datasets', 'S_FRAC_Ar'): [('OBJECTID', '<i4'), ('SHAPE', '<f8', (2,)), ('CEN_BLK_ID', '<U17'), ('ARV_BG_TOT', '<f8'), ('ARV_CN_TOT', '<f8'), ('TOT_LOSS01', '<f8'), ('BL_TOT01', '<f8'), ('CL_TOT01', '<f8'), ('HAZARD_TYP', '<U4'), ('SCENAR_ID', '<U25'), ('TOT_LOSS10', '<f8'), ('BL_TOT10', '<f8'), ('CL_TOT10', '<f8'), ('TOT_LOSS04', '<f8'), ('BL_TOT04', '<f8'), ('CL_TOT04', '<f8'), ('TOT_LOSS02', '<f8'), ('BL_TOT02', '<f8'), ('CL_TOT02', '<f8'), ('TOT_LSS0_2', '<f8'), ('BL_TOT0_2', '<f8'), ('CL_TOT0_2', '<f8'), ('TOT_LSSAAL', '<f8'), ('BL_TOTAAL', '<f8'), ('CL_TOTAAL', '<f8'), ('HUC8_CODE', '<U8'), ('CASE_NO', '<U12'), ('VERSION_ID', '<U11'), ('SOURCE_CIT', '<U25'), ('SHAPE_Length', '<f8'), ('SHAPE_Area', '<f8')], ('Mit_Haz_Datasets', 'S_AOMI_Ar'): [('OBJECTID', '<i4'), ('SHAPE', '<f8', (2,)), ('AOMI_ID', '<U25'), ('CID', '<U6'), ('POL_NAME1', '<U50'), ('AOMI_CLASS', '<U4'), ('AOMI_TYP', '<U30'), ('AOMI_INFO', '<U1000'), ('HUC8_CODE', '<U8'), ('CASE_NO', '<U12'), ('VERSION_ID', '<U11'), ('SOURCE_CIT', '<U25'), ('SHAPE_Length', '<f8'), ('SHAPE_Area', '<f8')], ('Mit_Haz_Datasets', 'S_AOMI_Pt'): [('OBJECTID', '<i4'), ('Shape', '<f8', (2,)), ('AOMI_ID', '<U25'), ('CID', '<U6'), ('POL_NAME1', '<U50'), ('AOMI_CLASS', '<U30'), ('AOMI_TYP', '<U30'), ('AOMI_CAT', '<U25'), ('AOMI_SRCE', '<U50'), ('AOMI_INFO', '<U254'), ('NOTES', '<U1000'), ('HUC8_CODE', '<U8'), ('CASE_NO', '<U12'), ('VERSION_ID', '<U11'), ('SOURCE_CIT', '<U25')], ('Base_Dataset', 'S_Pol_Ar'): [('OBJECTID', '<i4'), ('SHAPE', '<f8', (2,)), ('DFIRM_ID', '<U6'), ('VERSION_ID', '<U11'), ('POL_AR_ID', '<U25'), ('POL_NAME1', '<U50'), ('POL_NAME2', '<U50'), ('POL_NAME3', '<U50'), ('CO_FIPS', '<U3'), ('ST_FIPS', '<U2'), ('COMM_NO', '<U4'), ('CID', '<U6'), ('ANI_TF', '<U1'), ('ANI_FIRM', '<U6'), ('COM_NFO_ID', '<U25'), ('SOURCE_CIT', '<U11'), ('SHAPE_Length', '<f8'), ('SHAPE_Area', '<f8')], ('Base_Dataset', 'S_HUC_Ar'): [('OBJECTID', '<i4'), ('Shape', '<f8', (2,)), ('HUC_CODE', '<U14'), ('HUC_NAME', '<U80'), ('DIGITS', '<i4'), ('CASE_NO', '<U12'), ('VERSION_ID', '<U11'), ('SOURCE_CIT', '<U25'), ('Shape_Length', '<f8'), ('Shape_Area', '<f8')], ('CNMS_Dataset', 'S_UnMapped_Ln'): [('OBJECTID', '<i4'), ('SHAPE', '<f8', (2,)), ('UML_ID', '<U12'), ('CO_FIPS', '<U12'), ('CID', '<U12'), ('HUC8_KEY', '<U8'), ('MILES', '<f8'), ('SHAPE_Length', '<f8')], ('CNMS_Dataset', 'S_Studies_Ln'): [('OBJECTID', '<i4'), ('SHAPE', '<f8', (2,)), ('REACH_ID', '<U12'), ('STUDY_ID', '<U12'), ('CASE_NO', '<U12'), ('CO_FIPS', '<U12'), ('CID', '<U12'), ('WTR_NM', '<U100'), ('WTR_NM_1', '<U100'), ('FLD_ZONE', '<U60'), ('VALIDATION_STATUS', '<U50'), ('STATUS_TYP', '<U100'), ('MILES', '<f8'), ('SOURCE', '<U100'), ('STATUS_DATE', '<M8[us]'), ('FY_FUNDED', '<U4'), ('REASON', '<U255'), ('HUC8_KEY', '<U8'), ('STUDY_TYPE', '<U50'), ('TIER', '<U12'), ('FRP', '<U10'), ('LINE_TYPE', '<U40'), ('FBS_CMPLNT', '<U10'), ('FBS_CHKDT', '<M8[us]'), ('FBS_CTYP', '<U50'), ('DUPLICATE', '<U20'), ('POC_ID', '<U20'), ('DATE_RQST', '<M8[us]'), ('DATE_EFFECT', '<M8[us]'), ('HYDRO_MDL', '<U100'), ('HYDRO_MDL_CMT', '<U255'), ('HYDRA_MDL', '<U100'), ('HYDRA_MDL_CMT', '<U255'), ('HODIGFMT', '<U10'), ('HADIGFMT', '<U10'), ('HO_RUNMOD', '<U10'), ('HA_RUNMOD', '<U10'), ('C1_GAGE', '<i4'), ('C2_DISCH', '<i4'), ('C3_MODEL', '<i4'), ('C4_FCSTR', '<i4'), ('C5_CHANN', '<i4'), ('C6_HSTR', '<i4'), ('C7_SCOUR', '<i4'), ('S1_REGEQ', '<i4'), ('S2_REPLO', '<i4'), ('S3_IMPAR', '<i4'), ('S4_HSTR', '<i4'), ('S5_CHIMP', '<i4'), ('S6_TOPO', '<i4'), ('S7_VEGLU', '<i4'), ('S8_HWMS', '<i4'), ('S9_REGEQ', '<i4'), ('CE_TOTAL', '<i4'), ('SE_TOTAL', '<i4'), ('A1_TOPO', '<i4'), ('A2_HYDRO', '<i4'), ('A3_IMPAR', '<i4'), ('A4_TECH', '<i4'), ('A5_FOAPASS', '<i4'), ('COMMENT', '<U255'), ('BS_ZONE', '<U60'), ('BS_STDYTYP', '<U255'), ('BS_HYDRO_M', '<U100'), ('BS_HYDRO_CMT', '<U255'), ('BS_HYDRA_M', '<U100'), ('BS_HYDRA_CMT', '<U255'), ('BS_FY_FUND', '<U4'), ('BS_PRELIM_DATE', '<M8[us]'), ('BS_LFD_DATE', '<M8[us]'), ('EC1_UDEF', '<i4'), ('EC2_UDEF', '<i4'), ('ES1_UDEF', '<i4'), ('ES2_UDEF', '<i4'), ('ES3_UDEF', '<i4'), ('ES4_UDEF', '<i4'), ('E_ELEMDATE', '<M8[us]'), ('IS_URBAN', '<U10'), ('C01_CMT', '<U255'), ('C01_SRC', '<U255'), ('C01_URL', '<U255'), ('C02_CMT', '<U255'), ('C02_SRC', '<U255'), ('C02_URL', '<U255'), ('C03_CMT', '<U255'), ('C03_SRC', '<U255'), ('C03_URL', '<U255'), ('C04_CMT', '<U255'), ('C04_SRC', '<U255'), ('C04_URL', '<U255'), ('C05_CMT', '<U255'), ('C05_SRC', '<U255'), ('C05_URL', '<U255'), ('C06_CMT', '<U255'), ('C06_SRC', '<U255'), ('C06_URL', '<U255'), ('C07_CMT', '<U255'), ('C07_SRC', '<U255'), ('C07_URL', '<U255'), ('S01_CMT', '<U255'), ('S01_SRC', '<U255'), ('S01_URL', '<U255'), ('S02_CMT', '<U255'), ('S02_SRC', '<U255'), ('S02_URL', '<U255'), ('S03_CMT', '<U255'), ('S03_SRC', '<U255'), ('S03_URL', '<U255'), ('S04_CMT', '<U255'), ('S04_SRC', '<U255'), ('S04_URL', '<U255'), ('S05_CMT', '<U255'), ('S05_SRC', '<U255'), ('S05_URL', '<U255'), ('S06_CMT', '<U255'), ('S06_SRC', '<U255'), ('S06_URL', '<U255'), ('S07_CMT', '<U255'), ('S07_SRC', '<U255'), ('S07_URL', '<U255'), ('S08_CMT', '<U255'), ('S08_SRC', '<U255'), ('S08_URL', '<U255'), ('S09_CMT', '<U255'), ('S09_SRC', '<U255'), ('S09_URL', '<U255'), ('A1_CMT', '<U255'), ('A1_SRC', '<U255'), ('A1_URL', '<U255'), ('A2_CMT', '<U255'), ('A2_SRC', '<U255'), ('A2_URL', '<U255'), ('A3_CMT', '<U255'), ('A3_SRC', '<U255'), ('A3_URL', '<U255'), ('A4_CMT', '<U255'), ('A4_SRC', '<U255'), ('A4_URL', '<U255'), ('A5_CMT', '<U255'), ('A5_SRC', '<U255'), ('A5_URL', '<U255'), ('EC1_CMT', '<U255'), ('EC1_SRC', '<U255'), ('EC1_URL', '<U255'), ('EC2_CMT', '<U255'), ('EC2_SRC', '<U255'), ('EC2_URL', '<U255'), ('ES1_CMT', '<U255'), ('ES1_SRC', '<U255'), ('ES1_URL', '<U255'), ('ES2_CMT', '<U255'), ('ES2_SRC', '<U255'), ('ES2_URL', '<U255'), ('ES3_CMT', '<U255'), ('ES3_SRC', '<U255'), ('ES3_URL', '<U255'), ('ES4_CMT', '<U255'), ('ES4_SRC', '<U255'), ('ES4_URL', '<U255'), ('BS_Model_2D', '<U10'), ('BS_MIP_CASE_NUMBER', '<U12'), ('WSEL_AVAIL', '<U50'), ('DPTH_AVAIL', '<U50'), ('BLE', '<U20'), ('BLE_POC', '<U20'), ('BLE_DATE', '<M8[us]'), ('MODEL_2D', '<U10'), ('SHAPE_Length', '<f8')], ('NA', 'L_Source_Cit'): [('OBJECTID', '<i4'), ('SOURCE_CIT', '<U25'), ('DFIRM_ID', '<U6'), ('CITATION', '<U25'), ('PUBLISHER', '<U254'), ('TITLE', '<U254'), ('AUTHOR', '<U254'), ('PUB_PLACE', '<U100'), ('PUB_DATE', '<M8[us]'), ('WEBLINK', '<U128'), ('SRC_SCALE', '<U12'), ('MEDIA', '<U50'), ('CASE_NO', '<U12'), ('VERSION_ID', '<U11')]}
    control_attributes = {('EBFE_Dataset', 'TENPCT_FP'): ['OBJECTID', 'SHAPE', 'EST_ID', 'VERSION_ID', 'EST_AR_ID', 'V_DATUM', 'LEN_UNIT', 'SOURCE_CIT', 'EST_Risk', 'STUDY_TYP', 'SFHA_TF', 'ZONE_SUBTY', 'STATIC_BFE', 'DEPTH', 'VELOCITY', 'VEL_UNIT', 'AR_REVERT', 'AR_SUBTRV', 'BFE_REVERT', 'DEP_REVERT', 'DUAL_ZONE', 'FLD_ZONE', 'SHAPE_Length', 'SHAPE_Area'], 
                          ('EBFE_Dataset', 'FLD_HAZ_AR'): ['OBJECTID', 'SHAPE', 'EST_ID', 'VERSION_ID', 'EST_AR_ID', 'ZONE_SUBTY', 'V_DATUM', 'LEN_UNIT', 'SOURCE_CIT', 'EST_Risk', 'STUDY_TYP', 'SFHA_TF', 'STATIC_BFE', 'DEPTH', 'VELOCITY', 'VEL_UNIT', 'AR_REVERT', 'AR_SUBTRV', 'BFE_REVERT', 'DEP_REVERT', 'DUAL_ZONE', 'FLD_ZONE', 'SHAPE_Length', 'SHAPE_Area'], 
                          ('EBFE_Dataset', 'SUBBASINS'): ['OBJECTID', 'SHAPE', 'EST_ID', 'VERSION_ID', 'E_SUBAS_ID', 'HUC8_CODE', 'E_SUBAS_NM', 'EST_AREA', 'AREA_UNIT', 'US_1', 'US_2', 'US_3', 'US_4', 'DS_1', 'PRECIP_IN', 'MAINCHSLP', 'E_Q_10PCT', 'E_Q_04PCT', 'E_Q_02PCT', 'E_Q_01PCT', 'E_Q_01PLUS', 'E_Q_01MIN', 'E_Q_0_2PCT', 'SOURCE_CIT', 'WTR_NM', 'BASIN_DESC', 'NODE_ID', 'BASIN_TYP', 'SHAPE_Length', 'SHAPE_Area'], 
                          ('EBFE_Dataset', 'BFE_2D'): ['OBJECTID', 'SHAPE', 'EST_ID', 'VERSION_ID', 'EBFE_LN_ID', 'BLELEV1PCT', 'BFE_LN_TYP', 'LEN_UNIT', 'V_DATUM', 'SOURCE_CIT', 'SHAPE_Length'], 
                          ('EBFE_Dataset', 'WTR_LN'): ['OBJECTID', 'SHAPE', 'EST_ID', 'VERSION_ID', 'WTR_LN_ID', 'WTR_NM', 'SOURCE_CIT', 'SHOWN_FIRM', 'SHOWN_INDX', 'SHAPE_Length'], 
                          ('EBFE_Dataset', 'WTR_AR'): ['OBJECTID', 'SHAPE', 'EST_ID', 'VERSION_ID', 'WTR_AR_ID', 'WTR_NM', 'SOURCE_CIT', 'SHOWN_FIRM', 'SHOWN_INDX', 'SHAPE_Length', 'SHAPE_Area'], 
                          ('EBFE_Dataset', 'DTL_STUD_AR'): ['OBJECTID', 'SHAPE', 'DTL_AR_ID', 'VERSION_ID', 'EFF_DATE', 'FIRM_PAN', 'TYPE', 'CD_YN', 'CD_POC', 'CD_ADD1', 'CD_ADD2', 'CD_CTY', 'CD_STATE', 'CD_ZIP', 'CD_PHONE', 'CD_EMAIL', 'SOURCE_CIT', 'LOMR_ID', 'CASE_NO', 'SCALE', 'STATUS', 'SHAPE_Length', 'SHAPE_Area'], 
                          ('EBFE_Dataset', 'DTL_STUD_LN'): ['OBJECTID', 'SHAPE', 'DTL_LN_ID', 'VERSION_ID', 'EFF_DATE', 'FIRM_PAN', 'TYPE', 'CD_YN', 'CD_POC', 'CD_ADD1', 'CD_ADD2', 'CD_CTY', 'CD_STATE', 'CD_ZIP', 'CD_PHONE', 'CD_EMAIL', 'SOURCE_CIT', 'LOMR_ID', 'CASE_NO', 'SCALE', 'STATUS', 'SHAPE_Length'], 
                          ('EBFE_Dataset', 'XS_1D'): ['OBJECTID', 'SHAPE', 'EST_ID', 'VERSION_ID', 'XS_LN_ID', 'WTR_NM', 'STREAM_STN', 'START_ID', 'XS_LN_TYP', 'E_WSE_1PCT', 'V_DATUM', 'MODEL_ID', 'SOURCE_CIT', 'E_WSE_10PC', 'E_WSE_4PCT', 'E_WSE_2PCT', 'E_WSE_1PLU', 'E_WSE_1MIN', 'E_WSE_0_2P', 'E_Q_10PCT', 'E_Q_04PCT', 'E_Q_02PCT', 'E_Q_01PCT', 'E_Q_01PLUS', 'E_Q_01MIN', 'E_Q_0_2PCT', 'XS_LTR', 'STRMBED_EL', 'LEN_UNIT', 'SHAPE_Length'], 
                          ('Mit_Haz_Datasets', 'S_FRAC_Ar'): ['OBJECTID', 'SHAPE', 'CEN_BLK_ID', 'ARV_BG_TOT', 'ARV_CN_TOT', 'TOT_LOSS01', 'BL_TOT01', 'CL_TOT01', 'HAZARD_TYP', 'SCENAR_ID', 'TOT_LOSS10', 'BL_TOT10', 'CL_TOT10', 'TOT_LOSS04', 'BL_TOT04', 'CL_TOT04', 'TOT_LOSS02', 'BL_TOT02', 'CL_TOT02', 'TOT_LSS0_2', 'BL_TOT0_2', 'CL_TOT0_2', 'TOT_LSSAAL', 'BL_TOTAAL', 'CL_TOTAAL', 'HUC8_CODE', 'CASE_NO', 'VERSION_ID', 'SOURCE_CIT', 'SHAPE_Length', 'SHAPE_Area'], 
                          ('Mit_Haz_Datasets', 'S_AOMI_Ar'): ['OBJECTID', 'SHAPE', 'AOMI_ID', 'CID', 'POL_NAME1', 'AOMI_CLASS', 'AOMI_TYP', 'AOMI_INFO', 'HUC8_CODE', 'CASE_NO', 'VERSION_ID', 'SOURCE_CIT', 'SHAPE_Length', 'SHAPE_Area'], 
                          ('Mit_Haz_Datasets', 'S_AOMI_Pt'): ['OBJECTID', 'Shape', 'AOMI_ID', 'CID', 'POL_NAME1', 'AOMI_CLASS', 'AOMI_TYP', 'AOMI_CAT', 'AOMI_SRCE', 'AOMI_INFO', 'NOTES', 'HUC8_CODE', 'CASE_NO', 'VERSION_ID', 'SOURCE_CIT'], 
                          ('Base_Dataset', 'S_Pol_Ar'): ['OBJECTID', 'SHAPE', 'DFIRM_ID', 'VERSION_ID', 'POL_AR_ID', 'POL_NAME1', 'POL_NAME2', 'POL_NAME3', 'CO_FIPS', 'ST_FIPS', 'COMM_NO', 'CID', 'ANI_TF', 'ANI_FIRM', 'COM_NFO_ID', 'SOURCE_CIT', 'SHAPE_Length', 'SHAPE_Area'], 
                          ('Base_Dataset', 'S_HUC_Ar'): ['OBJECTID', 'Shape', 'HUC_CODE', 'HUC_NAME', 'DIGITS', 'CASE_NO', 'VERSION_ID', 'SOURCE_CIT', 'Shape_Length', 'Shape_Area'], 
                          ('CNMS_Dataset', 'S_UnMapped_Ln'): ['OBJECTID', 'SHAPE', 'UML_ID', 'CO_FIPS', 'CID', 'HUC8_KEY', 'MILES', 'SHAPE_Length'], 
                          ('CNMS_Dataset', 'S_Studies_Ln'): ['OBJECTID', 'SHAPE', 'REACH_ID', 'STUDY_ID', 'CASE_NO', 'CO_FIPS', 'CID', 'WTR_NM', 'WTR_NM_1', 'FLD_ZONE', 'VALIDATION_STATUS', 'STATUS_TYP', 'MILES', 'SOURCE', 'STATUS_DATE', 'FY_FUNDED', 'REASON', 'HUC8_KEY', 'STUDY_TYPE', 'TIER', 'FRP', 'LINE_TYPE', 'FBS_CMPLNT', 'FBS_CHKDT', 'FBS_CTYP', 'DUPLICATE', 'POC_ID', 'DATE_RQST', 'DATE_EFFECT', 'HYDRO_MDL', 'HYDRO_MDL_CMT', 'HYDRA_MDL', 'HYDRA_MDL_CMT', 'HODIGFMT', 'HADIGFMT', 'HO_RUNMOD', 'HA_RUNMOD', 'C1_GAGE', 'C2_DISCH', 'C3_MODEL', 'C4_FCSTR', 'C5_CHANN', 'C6_HSTR', 'C7_SCOUR', 'S1_REGEQ', 'S2_REPLO', 'S3_IMPAR', 'S4_HSTR', 'S5_CHIMP', 'S6_TOPO', 'S7_VEGLU', 'S8_HWMS', 'S9_REGEQ', 'CE_TOTAL', 'SE_TOTAL', 'A1_TOPO', 'A2_HYDRO', 'A3_IMPAR', 'A4_TECH', 'A5_FOAPASS', 'COMMENT', 'BS_ZONE', 'BS_STDYTYP', 'BS_HYDRO_M', 'BS_HYDRO_CMT', 'BS_HYDRA_M', 'BS_HYDRA_CMT', 'BS_FY_FUND', 'BS_PRELIM_DATE', 'BS_LFD_DATE', 'EC1_UDEF', 'EC2_UDEF', 'ES1_UDEF', 'ES2_UDEF', 'ES3_UDEF', 'ES4_UDEF', 'E_ELEMDATE', 'IS_URBAN', 'C01_CMT', 'C01_SRC', 'C01_URL', 'C02_CMT', 'C02_SRC', 'C02_URL', 'C03_CMT', 'C03_SRC', 'C03_URL', 'C04_CMT', 'C04_SRC', 'C04_URL', 'C05_CMT', 'C05_SRC', 'C05_URL', 'C06_CMT', 'C06_SRC', 'C06_URL', 'C07_CMT', 'C07_SRC', 'C07_URL', 'S01_CMT', 'S01_SRC', 'S01_URL', 'S02_CMT', 'S02_SRC', 'S02_URL', 'S03_CMT', 'S03_SRC', 'S03_URL', 'S04_CMT', 'S04_SRC', 'S04_URL', 'S05_CMT', 'S05_SRC', 'S05_URL', 'S06_CMT', 'S06_SRC', 'S06_URL', 'S07_CMT', 'S07_SRC', 'S07_URL', 'S08_CMT', 'S08_SRC', 'S08_URL', 'S09_CMT', 'S09_SRC', 'S09_URL', 'A1_CMT', 'A1_SRC', 'A1_URL', 'A2_CMT', 'A2_SRC', 'A2_URL', 'A3_CMT', 'A3_SRC', 'A3_URL', 'A4_CMT', 'A4_SRC', 'A4_URL', 'A5_CMT', 'A5_SRC', 'A5_URL', 'EC1_CMT', 'EC1_SRC', 'EC1_URL', 'EC2_CMT', 'EC2_SRC', 'EC2_URL', 'ES1_CMT', 'ES1_SRC', 'ES1_URL', 'ES2_CMT', 'ES2_SRC', 'ES2_URL', 'ES3_CMT', 'ES3_SRC', 'ES3_URL', 'ES4_CMT', 'ES4_SRC', 'ES4_URL', 'BS_Model_2D', 'BS_MIP_CASE_NUMBER', 'WSEL_AVAIL', 'DPTH_AVAIL', 'BLE', 'BLE_POC', 'BLE_DATE', 'MODEL_2D', 'SHAPE_Length'], 
                          ('NA', 'L_Source_Cit'): ['OBJECTID', 'SOURCE_CIT', 'DFIRM_ID', 'CITATION', 'PUBLISHER', 'TITLE', 'AUTHOR', 'PUB_PLACE', 'PUB_DATE', 'WEBLINK', 'SRC_SCALE', 'MEDIA', 'CASE_NO', 'VERSION_ID']}
    control_schema = {('EBFE_Dataset', 'TENPCT_FP'): ['<i4', '<f8', '<U20', '<U11', '<U25', '<U17', '<U16', '<U15', '<U30', '<U28', '<U1', '<U72', '<f8', '<f8', '<f8', '<U20', '<U17', '<U72', '<f8', '<f8', '<U1', '<U17', '<f8', '<f8'],
                      ('EBFE_Dataset', 'FLD_HAZ_AR'): ['<i4', '<f8', '<U20', '<U11', '<U25', '<U72', '<U17', '<U16', '<U15', '<U30', '<U28', '<U1', '<f8', '<f8', '<f8', '<U20', '<U17', '<U72', '<f8', '<f8', '<U1', '<U17', '<f8', '<f8'],
                      ('EBFE_Dataset', 'SUBBASINS'): ['<i4', '<f8', '<U20', '<U11', '<U20', '<U8', '<U50', '<f8', '<U50', '<U20', '<U20', '<U20', '<U20', '<U20', '<f8', '<f8', '<f8', '<f8', '<f8', '<f8', '<f8', '<f8', '<f8', '<U50', '<U100', '<U254', '<U25', '<U19', '<f8', '<f8'],
                      ('EBFE_Dataset', 'BFE_2D'): ['<i4', '<f8', '<U20', '<U11', '<U25', '<i4', '<U24', '<U16', '<U17', '<U11', '<f8'], 
                      ('EBFE_Dataset', 'WTR_LN'): ['<i4', '<f8', '<U20', '<U11', '<U25', '<U100', '<U11', '<U1', '<U1', '<f8'],
                      ('EBFE_Dataset', 'WTR_AR'): ['<i4', '<f8', '<U20', '<U11', '<U25', '<U100', '<U11', '<U1', '<U1', '<f8', '<f8'], 
                      ('EBFE_Dataset', 'DTL_STUD_AR'): ['<i4', '<f8', '<U8', '<U11', '<M8[us]', '<U15', '<U20', '<U10', '<U70', '<U150', '<U150', '<U100', '<U25', '<U10', '<U20', '<U100', '<U11', '<U25', '<U13', '<U5', '<U11', '<f8', '<f8'],
                      ('EBFE_Dataset', 'DTL_STUD_LN'): ['<i4', '<f8', '<U8', '<U11', '<M8[us]', '<U15', '<U20', '<U10', '<U70', '<U150', '<U150', '<U100', '<U25', '<U10', '<U20', '<U100', '<U11', '<U25', '<U13', '<U5', '<U11', '<f8'],
                      ('EBFE_Dataset', 'XS_1D'): ['<i4', '<f8', '<U20', '<U11', '<U25', '<U100', '<f8', '<U25', '<U24', '<f8', '<U14', '<U300', '<U11', '<f8', '<f8', '<f8', '<f8', '<f8', '<f8', '<f8', '<f8', '<f8', '<f8', '<f8', '<f8', '<f8', '<U12', '<f8', '<U16', '<f8'],
                      ('Mit_Haz_Datasets', 'S_FRAC_Ar'): ['<i4', '<f8', '<U17', '<f8', '<f8', '<f8', '<f8', '<f8', '<U4', '<U25', '<f8', '<f8', '<f8', '<f8', '<f8', '<f8', '<f8', '<f8', '<f8', '<f8', '<f8', '<f8', '<f8', '<f8', '<f8', '<U8', '<U12', '<U11', '<U25', '<f8', '<f8'],
                      ('Mit_Haz_Datasets', 'S_AOMI_Ar'): ['<i4', '<f8', '<U25', '<U6', '<U50', '<U4', '<U30', '<U1000', '<U8', '<U12', '<U11', '<U25', '<f8', '<f8'], 
                      ('Mit_Haz_Datasets', 'S_AOMI_Pt'): ['<i4', '<f8', '<U25', '<U6', '<U50', '<U30', '<U30', '<U25', '<U50', '<U254', '<U1000', '<U8', '<U12', '<U11', '<U25'],
                      ('Base_Dataset', 'S_Pol_Ar'): ['<i4', '<f8', '<U6', '<U11', '<U25', '<U50', '<U50', '<U50', '<U3', '<U2', '<U4', '<U6', '<U1', '<U6', '<U25', '<U11', '<f8', '<f8'],
                      ('Base_Dataset', 'S_HUC_Ar'): ['<i4', '<f8', '<U14', '<U80', '<i4', '<U12', '<U11', '<U25', '<f8', '<f8'],
                      ('CNMS_Dataset', 'S_UnMapped_Ln'): ['<i4', '<f8', '<U12', '<U12', '<U12', '<U8', '<f8', '<f8'],
                      ('CNMS_Dataset', 'S_Studies_Ln'): ['<i4', '<f8', '<U12', '<U12', '<U12', '<U12', '<U12', '<U100', '<U100', '<U60', '<U50', '<U100', '<f8', '<U100', '<M8[us]', '<U4', '<U255', '<U8', '<U50', '<U12', '<U10', '<U40', '<U10', '<M8[us]', '<U50', '<U20', '<U20', '<M8[us]', '<M8[us]', '<U100', '<U255', '<U100', '<U255', '<U10', '<U10', '<U10', '<U10', '<i4', '<i4', '<i4', '<i4', '<i4', '<i4', '<i4', '<i4', '<i4', '<i4', '<i4', '<i4', '<i4', '<i4', '<i4', '<i4', '<i4', '<i4', '<i4', '<i4', '<i4', '<i4', '<i4', '<U255', '<U60', '<U255', '<U100', '<U255', '<U100', '<U255', '<U4', '<M8[us]', '<M8[us]', '<i4', '<i4', '<i4', '<i4', '<i4', '<i4', '<M8[us]', '<U10', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U255', '<U10', '<U12', '<U50', '<U50', '<U20', '<U20', '<M8[us]', '<U10', '<f8'], 
                      ('NA', 'L_Source_Cit'): ['<i4', '<U25', '<U6', '<U25', '<U254', '<U254', '<U254', '<U100', '<M8[us]', '<U128', '<U12', '<U50', '<U12', '<U11']}
    arcpy.SetProgressorLabel("Performing feature and schema check....")
    arcpy.AddMessage("Performing feature and schema check....")
    not_in_db = list(set(control_items) - set(all_db_items))
    extra_in_db = list(set(all_db_items) - set(control_items))
    
    null_values = {}
    db_items = {}
    for i in features:
        print(i[0],'\\', i[1])
        fc = os.path.join(in_gdb, i[0], i[1])
        try:
            arr = arcpy.da.FeatureClassToNumPyArray(fc, "*")
            db_items[i] = arr.dtype.descr
        except:
            print(i[0] + '\\' + i[1] + ' has null values and could not be processed')
            arr = arcpy.da.FeatureClassToNumPyArray(fc, "*", skip_nulls=True)
            db_items[i] = arr.dtype.descr
            null_values[i] = arr.dtype.descr
    for i in tables:
        print(i[0],'\\', i[1])
        table = os.path.join(in_gdb, i[1])
        try:
            arr = arcpy.da.TableToNumPyArray(table, "*")
            db_items[i] = arr.dtype.descr
        except:
            print(i[0] + '\\' + i[1] + ' is has null values and could not be processed')
            arr = arcpy.da.TableToNumPyArray(table, "*", skip_nulls=True)
            db_items[i] = arr.dtype.descr
            null_values[i] = arr.dtype.descr
            
    db_attributes = {}
    db_schema = {}
    for key, value in db_items.items():
        #print(control_attributes[key])
        attributes = [attribute[0] for attribute in db_items[key]]
        db_attributes[key] = attributes
        schema = [attribute[1] for attribute in db_items[key]]
        db_schema[key] = schema
        
    df = pd.DataFrame(control_items, columns=['Dataset', 'Item Name'])
    df['Present'] = "Yes"
    df['Missing Attributes'] = "No"
    df['Extra Attributes'] = "No"
    df['Schema Correct'] = 'Yes'
    df['None Acceptable Values'] = 'No'
    df['Clipped to HUC8 Boundary'] = 'NA'
    df.loc[df['Item Name'].isin([i[1] for i in rasters]), ["Missing Attributes", "Extra Attributes", "Schema Correct", "None Acceptable Values"]] = "NA"
    
    key_error = []
    for key, value in control.items():
        try:
            missing_attributes = list(set(control_attributes[key]) - set(db_attributes[key]))
            extra_attributes = list(set(db_attributes[key]) - set(control_attributes[key]))
            schema_error = list(set(control_schema[key]) - set(db_schema[key]))
        except KeyError as ke:
            key_error.append(ke.args[0])
            print(key_error)
        try:
            if len(missing_attributes) == 1:
                print(f'There is {len(missing_attributes)} attribute missing in the {key[1]} feature class')
                print(missing_attributes[0]) #missing attribute
                df["Missing Attributes"][df['Item Name'] == key[1]] = missing_attributes[0]
            elif len(missing_attributes) > 1:
                print(f'There are {len(missing_attributes)} attributes missing in the {key[1]} feature class')
                print(', '.join([attribute for attribute in missing_attributes]))
                df["Missing Attributes"][df['Item Name'] == key[1]] = ', '.join([attribute for attribute in missing_attributes])
            if len(extra_attributes) == 1:
                print(f'There is {len(extra_attributes)} attribute extra in the {key[1]} feature class')
                print(extra_attributes[0]) #extra attribute
                df["Extra Attributes"][df['Item Name'] == key[1]] = extra_attributes[0]
            elif len(extra_attributes) > 1:
                print(f'There are {len(extra_attributes)} attributes extra in the {key[1]} feature class')
                print(', '.join([attribute for attribute in extra_attributes]))
                df["Extra Attributes"][df['Item Name'] == key[1]] = ', '.join([attribute for attribute in extra_attributes])
            if len(schema_error) == 1:
                print(f'There is {len(schema_error)} schema error in the {key[1]} feature class')
                df["Schema Correct"][df['Item Name'] == key[1]] = 'No'
            elif len(schema_error) > 1:
                print(f'There are {len(schema_error)} schema errors in the {key[1]} feature class')
                df["Schema Correct"][df['Item Name'] == key[1]] = 'No'
        except:
            msg = "Oops...Something went wrong. Contact support"
            arcpy.AddError(msg)
            sys.exit(msg)       
    if len(not_in_db) > 1:
        print(f'There are {len(not_in_db)} items missing in the database\n')
        df["Present"][df['Item Name'].isin([i[1] for i in not_in_db])] = 'No'
    elif len(not_in_db) == 1:
        print(f'There is {len(not_in_db)} item missing in the database')
        df["Present"][df['Item Name'] == not_in_db[0][1]] = 'No'
    if len(key_error) > 0:
        for i in key_error:
            df.loc[(df["Present"] == "Yes") & (df["Item Name"] == i[1]), ["Missing Attributes", "Extra Attributes", "Schema Correct", "None Acceptable Values"]] = "Feature class could not be read" # rows with errors
            df.loc[(df["Present"] == "No") & (df["Item Name"] == i[1]), ["Missing Attributes", "Extra Attributes", "Schema Correct", "None Acceptable Values"]] = "NA"
            df.loc[(df["Present"] == "No") & (df["Item Name"] == i[1]), ["Missing Attributes", "Extra Attributes", "Schema Correct", "None Acceptable Values"]] = "NA"
    if len(null_values) > 0:
        for i in null_values:
            df.loc[(df["Present"] == "Yes") & (df["Item Name"] == i[1]), ["None Acceptable Values"]] = "Yes"
        
    if 'S_HUC_Ar' in [i[1] for i in features]:
        arcpy.SetProgressorLabel("Performing spatial check....")
        arcpy.AddMessage("Performing spatial check....")
        huc8_index = [i[1] for i in features].index('S_HUC_Ar')
        test_feature = os.path.join(in_gdb, features[huc8_index][0], features[huc8_index][1])
        huc_sr = arcpy.Describe(test_feature).spatialReference
        wbdhu8 = os.path.join(unzip_data(fema_portal, item_id), 'WBDHU8')
        huc8_layer = arcpy.MakeFeatureLayer_management(wbdhu8, "WBDHU8")
        huc8_layer = arcpy.management.SelectLayerByLocation(huc8_layer.getOutput(0), "HAVE_THEIR_CENTER_IN", test_feature, "-1 Miles", "NEW_SELECTION", "NOT_INVERT")
        with arcpy.EnvManager(outputCoordinateSystem=huc_sr):
            base_feature = arcpy.conversion.FeatureClassToFeatureClass(huc8_layer.getOutput(0), scratch_gdb, "HUC8_BaseFeatureX")
        for i in features:
            if i[1] in [i[1] for i in control_items]:
                fc = os.path.join(in_gdb, i[0], i[1])
                fc_type = arcpy.Describe(fc).shapeType
                if fc_type == 'Point':
                    fc_layer = arcpy.MakeFeatureLayer_management(fc, i[1])
                    fc_layer = arcpy.management.SelectLayerByLocation(fc_layer.getOutput(0), "COMPLETELY_WITHIN", base_feature, None, "NEW_SELECTION", "INVERT")
                    not_clipped = fc_layer.getOutput(0).getSelectionSet()
                else:
                    fc_layer = arcpy.MakeFeatureLayer_management(fc, i[1])
                    fc_layer = arcpy.management.SelectLayerByLocation(fc_layer.getOutput(0), "CROSSED_BY_THE_OUTLINE_OF", base_feature, None, "NEW_SELECTION", "NOT_INVERT")
                    not_clipped = fc_layer.getOutput(0).getSelectionSet()
                if not_clipped:
                    print(i[1] + ' has unclipped features')
                    df['Clipped to HUC8 Boundary'][df['Item Name'] == i[1]] = 'No'
                else: df['Clipped to HUC8 Boundary'][df['Item Name'] == i[1]] = 'Yes'
        huc_compare = arcpy.management.FeatureCompare(base_feature, test_feature, "OBJECTID", "GEOMETRY_ONLY", "IGNORE_M;IGNORE_Z;IGNORE_POINTID;IGNORE_EXTENSION_PROPERTIES;IGNORE_SUBTYPES;IGNORE_RELATIONSHIPCLASSES;IGNORE_REPRESENTATIONCLASSES;IGNORE_FIELDALIAS", "0.000000784415 DecimalDegrees", 0.001, 0.003280833333, None, None, "CONTINUE_COMPARE")
        message = huc_compare.getMessages(1)
        if 'Geometries are different' in message:
            print('S_HUC_AR does not align to USGS HUC8 Boundary')
            huc_compare = 'S_HUC_AR does not align to USGS HUC8 Boundary'
            df['Clipped to HUC8 Boundary'][df['Item Name'] == 'S_HUC_Ar'] = 'No'
        else: 
            print('S_HUC_AR aligns to USGS HUC8 Boundary')
            huc_compare = 'S_HUC_AR aligns to USGS HUC8 Boundary'
            df['Clipped to HUC8 Boundary'][df['Item Name'] == 'S_HUC_Ar'] = 'Yes'
        df.to_csv(report_file, sep='\t', index=False)
        with open(report_file, "a") as report:
            report.write('-----------------------------------------------\nTool 1 - Results:\n-----------------------------------------------')
            report.write(f'\n{huc_compare}')
        arcpy.management.Delete(base_feature)
   
    if len(not_in_db) > 1:
        #df.to_csv(report_file, sep='\t', index=False)
        with open(report_file, "a") as report:
            report.write(f'\nThere are {len(not_in_db)} items missing in the database:\n' +
                        '\n'.join(['/'.join(item) for item in not_in_db]))
    elif len(not_in_db) == 1:
        #df.to_csv(report_file, sep='\t', index=False)
        with open(report_file, "a") as report:
            report.write(f'\nThere is {len(not_in_db)} item missing in the database:\n' +
                        '\n'.join(['/'.join(item) for item in not_in_db]))
    elif len(not_in_db) == 0:
        
        with open(report_file, "a") as report:
            report.write(f'\nThere are {len(not_in_db)} items missing in the database\n')
    if len(extra_in_db) == 1:
        with open(report_file, "a") as report:
            report.write(f'\nThere is {len(extra_in_db)} extra item in the database:\n' +
                        '\n'.join(['/'.join(item) for item in extra_in_db]))
    elif len(extra_in_db) > 0:
        with open(report_file, "a") as report:
            report.write(f'\nThere are {len(extra_in_db)} extra items in the database:\n' +
                        '\n'.join(['/'.join(item) for item in extra_in_db]))
    if len(null_values) > 0:
        for i in null_values:
            if i[1] in [i[1] for i in control_items]:
                with open(report_file, "a") as report:
                    report.write(f'\n{i[1]} has null values')
    return features
if __name__ == '__main__':
    
    in_gdb = arcpy.GetParameterAsText(0)
    out_folder = arcpy.GetParameterAsText(1)
    report_name = 'QAQC_Report_' + os.path.basename(in_gdb).split('.')[0][8:] + '.txt'
    report_file = os.path.join(out_folder, report_name)
    fema_portal = r"https://fema.maps.arcgis.com/"
    item_id = '491035bd63624dd6b7181016736c4da6'  
    arcpy.env.workspace = in_gdb
    scratch_gdb = arcpy.env.scratchWorkspace
    frd_check(report_file)
    arcpy.SetParameterAsText(2, report_file)
    arcpy.AddMessage("Feature, schema check is complete....")
    
