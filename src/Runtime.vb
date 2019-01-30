'*********************************************************************************************
' Caribou Movement: A SyncroSim Package for simulating movement patterns of caribou populations
' and their interaction with industrial developments.
'
' Copyright © 2007-2019 Apex Resource Management Solution Ltd. (ApexRMS). All rights reserved.
'*********************************************************************************************

Imports System.IO
Imports SyncroSim.Core
Imports System.Globalization
Imports SyncroSim.StochasticTime

Class Runtime
    Inherits StochasticTimeTransformer

    Public Overrides Sub Configure()

        MyBase.Configure()
        Me.NormalizeRunControl()

    End Sub

    Public Overrides Sub Transform()

        Dim libName As String = Me.Library.Connection.ConnectionString
        Dim app As String = Path.Combine(Me.PackageLocation, "scripts\caribouMovement.bat")
        Dim args As String = String.Format(CultureInfo.InvariantCulture, """{0}"" {1}", libName, Me.ResultScenario.Id)

        Try
            Me.ExecuteProcess(app, args, False, Nothing)
        Catch ex As Exception

            Dim sMsg As String = String.Format(CultureInfo.CurrentCulture, "Error executing external script file '{0}'.", app)
            Me.RecordStatus(StatusType.Failure, sMsg)
            sMsg = String.Format(CultureInfo.CurrentCulture, "Error Log file is '{0}\scripts\caribouMovement.log'", Me.PackageLocation)
            Me.RecordStatus(StatusType.Failure, sMsg)

            Throw

        End Try

    End Sub

    Public Sub NormalizeRunControl()

        Dim ValuesAdded As Boolean = False
        Dim ds As DataSheet = Me.ResultScenario.GetDataSheet("CM_RunControl")
        Dim dr As DataRow = ds.GetDataRow()

        If (dr Is Nothing) Then
            dr = ds.GetData().Rows.Add()
            ValuesAdded = True
        End If

        If (dr("StartJulianDay") Is DBNull.Value) Then
            dr("StartJulianDay") = 1
            ValuesAdded = True
        End If

        If (dr("EndYear") Is DBNull.Value) Then
            dr("EndYear") = 1
            ValuesAdded = True
        End If

        If (dr("CalvingPeakJulianDay") Is DBNull.Value) Then
            dr("CalvingPeakJulianDay") = 1
            ValuesAdded = True
        End If

        If (dr("TotalIterations") Is DBNull.Value) Then
            dr("TotalIterations") = 1
            ValuesAdded = True
        End If

        dr("MinimumIteration") = 1
        dr("MaximumIteration") = dr("TotalIterations")
        dr("MinimumTimestep") = 1
        dr("MaximumTimestep") = dr("EndYear")

        If (ValuesAdded) Then
            Me.RecordStatus(StatusType.Warning, "Run control missing values.  Using defaults.")
        End If

    End Sub

End Class
