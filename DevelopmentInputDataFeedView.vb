'*********************************************************************************************
' Caribou Movement: A SyncroSim Package for simulating movement patterns of caribou populations
' and their interaction with industrial developments.
'
' Copyright © 2007-2018 Apex Resource Management Solution Ltd. (ApexRMS). All rights reserved.
'*********************************************************************************************

Class DevelopmentInputDataFeedView

    Public Overrides Sub LoadDataFeed(dataFeed As Core.DataFeed)

        MyBase.LoadDataFeed(dataFeed)

        Me.SetTextBoxBinding(Me.TextBoxZoneOfInfluenceBufferWidthDev, "ZoneOfInfluenceBufferWidthDev")
        Me.SetTextBoxBinding(Me.TextBoxZoneOfInfluenceBufferWidthRoads, "ZoneOfInfluenceBufferWidthRoads")
        Me.SetTextBoxBinding(Me.TextBoxHarvestZoneBufferWidthRoadsAndDev, "HarvestZoneBufferWidthRoadsAndDev")
        Me.SetTextBoxBinding(Me.TextBoxNumNewDev, "NumNewDev")
        Me.SetTextBoxBinding(Me.TextBoxNearRadiusFromExistingDev, "NearRadiusFromExistingDev")
        Me.SetTextBoxBinding(Me.TextBoxRelProbOutsideNearRadius, "RelProbOutsideNearRadius")
        Me.SetTextBoxBinding(Me.TextBoxFarRadiusFromExistingDev, "FarRadiusFromExistingDev")
        Me.SetTextBoxBinding(Me.TextBoxRelProbOutsideFarRadius, "RelProbOutsideFarRadius")
        Me.SetTextBoxBinding(Me.TextBoxMinimumNewDevRadius, "MinimumNewDevRadius")
        Me.SetTextBoxBinding(Me.TextBoxMaximumNewDevRadius, "MaximumNewDevRadius")

        Me.RefreshBoundControls()

    End Sub

    Private Sub ButtonClearAll_Click(sender As Object, e As EventArgs) Handles ButtonClearAll.Click

        Me.ResetBoundControls()
        Me.ClearDataSheets()

    End Sub

End Class
