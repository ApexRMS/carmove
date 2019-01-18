'*********************************************************************************************
' Caribou Movement: A SyncroSim Package for simulating movement patterns of caribou populations
' and their interaction with industrial developments.
'
' Copyright © 2007-2018 Apex Resource Management Solution Ltd. (ApexRMS). All rights reserved.
'*********************************************************************************************

Imports SyncroSim.Core
Imports System.Globalization

Class RunControlDataFeedView

    Public Overrides Sub LoadDataFeed(dataFeed As Core.DataFeed)

        MyBase.LoadDataFeed(dataFeed)

        Me.SetTextBoxBinding(Me.TextBoxStartJulianDay, "StartJulianDay")
        Me.SetTextBoxBinding(Me.TextBoxEndYear, "EndYear")
        Me.SetTextBoxBinding(Me.TextBoxCalvingPeakJulianDay, "CalvingPeakJulianDay")
        Me.SetTextBoxBinding(Me.TextBoxTotalIterations, "TotalIterations")

        Me.RefreshBoundControls()

        Me.MonitorDataSheet(
          "CM_Terminology",
          AddressOf Me.OnTerminologyChanged,
          True)

    End Sub

    Private Sub OnTerminologyChanged(ByVal e As DataSheetMonitorEventArgs)

        Dim t As String = CStr(e.GetValue(
            "TimestepUnits",
            "Timestep")).ToLower(CultureInfo.CurrentCulture)

        Me.LabelEndYear.Text = String.Format(CultureInfo.CurrentCulture, "Number of {0}:", t)

    End Sub

    Private Sub ButtonClearAll_Click(sender As Object, e As EventArgs) Handles ButtonClearAll.Click

        Me.ResetBoundControls()
        Me.ClearDataSheets()

    End Sub

End Class
