
Imports SyncroSim.Core.Forms

Class ZOIMap
    Inherits ExportTransformer

    Protected Overrides Sub Export(location As String, exportType As ExportType)

        'DEVNOTE: Because shapefile, use * for file extension, as copying shp,shx,dbf,...
        Dim fileFilterRegex As String = ".*" & SPATIAL_MAP_ZONE_OF_INF_VARIABLE_NAME & "\..*$"
        CopyRasterFiles(Me.GetActiveResultScenarios(), fileFilterRegex, location, AddressOf CreateExportFilename)

    End Sub

    ''' <summary>
    ''' Rename the Spatial Export File, from the short form name generated during Model run, to the user friendly Export name  
    ''' </summary>
    ''' <param name="sourceName">The short form filename, as created during Model run spatial output</param>
    ''' <returns>The long form user-friendly Export filename</returns>
    ''' <remarks></remarks>
    Private Function CreateExportFilename(sourceName As String) As String
        Return sourceName.Replace(SPATIAL_MAP_ZONE_OF_INF_VARIABLE_NAME, SPATIAL_MAP_EXPORT_ZONE_OF_INF_VARIABLE_NAME)
    End Function

End Class

