'*********************************************************************************************
' Caribou Movement: A SyncroSim Package for simulating movement patterns of caribou populations
' and their interaction with industrial developments.
'
' Copyright © 2007-2019 Apex Resource Management Solution Ltd. (ApexRMS). All rights reserved.
'*********************************************************************************************

Imports SyncroSim.Core.Forms

Class HarvestZoneMap
    Inherits ExportTransformer

    Protected Overrides Sub Export(location As String, exportType As ExportType)

        'DEVNOTE: Because shapefile, use * for file extension, as copying shp,shx,dbf,...
        Dim fileFilterRegex As String = ".*" & SPATIAL_MAP_HARVEST_ZONE_VARIABLE_NAME & "\..*$"
        CopyRasterFiles(Me.GetActiveResultScenarios(), fileFilterRegex, location, AddressOf CreateExportFilename)

    End Sub

    ''' <summary>
    ''' Rename the Spatial Export File, from the short form name generated during Model run, to the user friendly Export name  
    ''' </summary>
    ''' <param name="sourceName">The short form filename, as created during Model run spatial output</param>
    ''' <returns>The long form user-friendly Export filename</returns>
    ''' <remarks></remarks>
    Private Function CreateExportFilename(sourceName As String) As String
        Return sourceName.Replace(SPATIAL_MAP_HARVEST_ZONE_VARIABLE_NAME, SPATIAL_MAP_EXPORT_HARVEST_ZONE_VARIABLE_NAME)
    End Function

End Class

