'*********************************************************************************************
' Caribou Movement: A SyncroSim Package for simulating movement patterns of caribou populations
' and their interaction with industrial developments.
'
' Copyright © 2007-2019 Apex Resource Management Solution Ltd. (ApexRMS). All rights reserved.
'*********************************************************************************************

Module Constants

    'Terminology
    Public Const TERMINOLOGY_DATA_SHEET_NAME As String = "CM_Terminology"
    Public Const TERMINOLOGY_STRATUM_LABEL_X_COLUMN_NAME As String = "StratumLabelX"
    Public Const TERMINOLOGY_STRATUM_LABEL_Y_COLUMN_NAME As String = "StratumLabelY"
    Public Const TERMINOLOGY_STRATUM_LABEL_Z_COLUMN_NAME As String = "StratumLabelZ"
    Public Const TERMINOLOGY_TIMESTEP_UNITS_COLUMN_NAME As String = "TimestepUnits"

    ' Corresponds with MERGED_ROADS_DEV_FILENAME in the Python caribouConstants.py file 
    '    MERGED_ROADS_DEV_FILENAME = "It{0:04d}_roads_dev.shp"
    Public Const SPATIAL_MAP_ROADS_AND_DEV_VARIABLE_NAME As String = "roads_dev"
    Public Const SPATIAL_MAP_EXPORT_ROADS_AND_DEV_VARIABLE_NAME As String = "roads_dev"

    ' Corresponds with ZOI_FILENAME in the Python caribouConstants.py file 
    '    ZOI_FILENAME = "It{0:04d}_zoi.shp"
    Public Const SPATIAL_MAP_ZONE_OF_INF_VARIABLE_NAME As String = "zoi"
    Public Const SPATIAL_MAP_EXPORT_ZONE_OF_INF_VARIABLE_NAME As String = "zone_of_influence"

    ' Corresponds with MERGED_HARVEST_ZONE_FILENAME in the Python caribouConstants.py file 
    'It{0:04d}_harvest_zone.shp
    Public Const SPATIAL_MAP_HARVEST_ZONE_VARIABLE_NAME As String = "harvest_zone"
    Public Const SPATIAL_MAP_EXPORT_HARVEST_ZONE_VARIABLE_NAME As String = "harvest_zone"

    '     Final Collar Points Daily Shapefile
    ' Corresponds with COLLAR_VALUES_SHAPEFILE_FILENAME in the Python caribouConstants.py file 
    'It{0:04d}_Ts{1:04d}_location.shp
    Public Const SPATIAL_MAP_LOCATION_NAME As String = "location"
    Public Const SPATIAL_MAP_EXPORT_LOCATION_NAME As String = "location"

End Module
