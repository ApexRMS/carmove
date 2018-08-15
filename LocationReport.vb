'*********************************************************************************************
' Caribou Movement: A SyncroSim Module for simulating movement patterns of caribou populations
' and their interaction with industrial developments.
'
' Copyright © 2007-2018 Apex Resource Management Solution Ltd. (ApexRMS). All rights reserved.
'*********************************************************************************************

Imports SyncroSim.Core.Forms
Imports System.Globalization

Class LocationReport
    Inherits ExportTransformer

    Protected Overrides Sub Export(location As String, exportType As ExportType)

        Dim query As String = Me.CreateReportQuery()
        Dim columns As ExportColumnCollection = Me.CreateColumnCollection()

        If (exportType = ExportType.ExcelFile) Then
            Me.ExcelExport(location, columns, query, "Location Data")
        Else

            Me.CSVExport(location, columns, query)
            Utilities.InformationMessageBox("Data saved to '{0}'.", location)

        End If

    End Sub

    Private Function CreateColumnCollection() As ExportColumnCollection

        Dim c As New ExportColumnCollection()

        Dim slx As String = Nothing
        Dim sly As String = Nothing
        Dim slz As String = Nothing
        Dim tsu As String = Nothing

        GetTerminology(Me.Project, slx, sly, slz, tsu)

        c.Add(New ExportColumn("ScenarioID", "Scenario ID"))
        c.Add(New ExportColumn("ScenarioName", "Scenario"))
        c.Add(New ExportColumn("Iteration", "Iteration"))
        c.Add(New ExportColumn("Timestep", tsu))
        c.Add(New ExportColumn("JulianDay", "Julian Day"))
        c.Add(New ExportColumn("StratumName", "Stratum"))
        c.Add(New ExportColumn("StratumLabelXName", slx))
        c.Add(New ExportColumn("StratumLabelYName", sly))
        c.Add(New ExportColumn("StratumLabelZName", slz))
        c.Add(New ExportColumn("HarvestZone", "Harvest Zone"))
        c.Add(New ExportColumn("Latitude", "Latitude"))
        c.Add(New ExportColumn("Longitude", "Longitude"))
        c.Add(New ExportColumn("OutOfBounds", "Out Of Bounds"))
        c.Add(New ExportColumn("DistanceFromPrevious", "Distance From Previous"))
        c.Add(New ExportColumn("RelationToZOI", "Relation To ZOI"))
        c.Add(New ExportColumn("RangeAssessmentArea", "Range Assessment Area"))

        Return c

    End Function

    Private Function CreateReportQuery() As String

        Dim Query As String = String.Format(CultureInfo.InvariantCulture,
            "SELECT CM_OutputLocation.ScenarioID, " &
            "SSim_Scenario.Name as ScenarioName, " &
            "Iteration, " &
            "Timestep, " &
            "JulianDay, " &
            "CM_Stratum.Name as StratumName, " &
            "CM_StratumLabelX.Name as StratumLabelXName, " &
            "CM_StratumLabelY.Name as StratumLabelYName, " &
            "CM_StratumLabelZ.Name as StratumLabelZName, " &
            "CASE WHEN HarvestZone=0 THEN 'No' ELSE 'Yes' END AS HarvestZone, " &
            "Latitude, " &
            "Longitude, " &
            "CASE WHEN OutOfBounds=0 THEN 'No' ELSE 'Yes' END AS OutOfBounds, " &
            "DistanceFromPrevious, " &
            "RelationToZOI, " &
            "RangeAssessmentArea " &
            "FROM CM_OutputLocation " &
            "INNER JOIN SSim_Scenario ON CM_OutputLocation.ScenarioID = SSim_Scenario.ScenarioID " &
            "INNER JOIN  CM_Stratum ON CM_OutputLocation.StratumID = CM_Stratum.StratumID " &
            "INNER JOIN CM_StratumLabelX ON CM_Stratum.StratumLabelXID=CM_StratumLabelX.StratumLabelXID " &
            "INNER JOIN CM_StratumLabelY ON CM_Stratum.StratumLabelYID=CM_StratumLabelY.StratumLabelYID " &
            "INNER JOIN CM_StratumLabelZ ON CM_Stratum.StratumLabelZID=CM_StratumLabelZ.StratumLabelZID " &
            "WHERE CM_OutputLocation.ScenarioID IN ({0}) " &
            "ORDER BY CM_OutputLocation.ScenarioID, Iteration, Timestep, JulianDay, CM_Stratum.Name, HarvestZone, Latitude, Longitude, OutOfBounds, DistanceFromPrevious",
            Me.CreateActiveResultScenarioFilter())

        Return Query

    End Function

End Class
