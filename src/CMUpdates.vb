'*********************************************************************************************
' carmove: SyncroSim Base Package for simulating the movement of caribou across a landscape.
'
' Copyright © 2007-2019 Apex Resource Management Solution Ltd. (ApexRMS). All rights reserved.
'*********************************************************************************************

Imports SyncroSim.Core

Class CMUpdates
    Inherits UpdateProvider

    ''' <summary>
    ''' Performs the database updates for Caribou Movement
    ''' </summary>
    ''' <param name="store"></param>
    ''' <param name="currentSchemaVersion"></param>
    ''' <remarks>
    ''' </remarks>
    Public Overrides Sub PerformUpdate(store As DataStore, currentSchemaVersion As Integer)

        If (currentSchemaVersion < 1) Then
            CM0000001(store)
        End If

        If (currentSchemaVersion < 2) Then
            CM0000002(store)
        End If

    End Sub

    ''' <summary>
    ''' SF0000005
    ''' </summary>
    ''' <param name="store"></param>
    ''' <remarks>
    ''' Adds fields to the following tables:
    ''' 
    ''' CM_SpatialFiles
    ''' CM_OutputLocation
    ''' 
    ''' </remarks>
    Private Shared Sub CM0000001(ByVal store As DataStore)

        If (store.TableExists("CM_SpatialFiles")) Then
            ' Add support for Range Assessment Area Shapefile 
            store.ExecuteNonQuery("Alter table CM_SpatialFiles add column RangeAssessmentAreaShapeFile TEXT")
            store.ExecuteNonQuery("Alter table CM_SpatialFiles add column RangeAssessmentAreaShapeFileShx TEXT")
            store.ExecuteNonQuery("Alter table CM_SpatialFiles add column RangeAssessmentAreaShapeFileDbf TEXT")
            store.ExecuteNonQuery("Alter table CM_SpatialFiles add column RangeAssessmentAreaShapeFilePrj TEXT")
        End If

        If (store.TableExists("CM_OutputLocation")) Then
            ' Add support for Range Assessment Area and Relative to ZOI
            store.ExecuteNonQuery("Alter table CM_OutputLocation add column RelationToZOI TEXT")
            store.ExecuteNonQuery("Alter table CM_OutputLocation add column RangeAssessmentArea TEXT")
        End If

    End Sub

    ''' <summary>
    ''' Option to systematically run all collar years
    ''' </summary>
    ''' <param name="store"></param>
    ''' <remarks>
    ''' Adds fields to the following tables:
    ''' 
    ''' CM_SpatialFiles
    ''' 
    ''' </remarks>
    Private Shared Sub CM0000002(ByVal store As DataStore)

        If (store.TableExists("CM_SpatialFiles")) Then
            ' Add support for Option to systematically run all collar years
            store.ExecuteNonQuery("Alter table CM_SpatialFiles add column SampleRandomCollarYear Integer")
            store.ExecuteNonQuery("Update CM_SpatialFiles Set SampleRandomCollarYear=-1")
        End If

    End Sub

End Class
