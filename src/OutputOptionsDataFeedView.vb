'*********************************************************************************************
' Caribou Movement: A SyncroSim Package for simulating movement patterns of caribou populations
' and their interaction with industrial developments.
'
' Copyright © 2007-2019 Apex Resource Management Solution Ltd. (ApexRMS). All rights reserved.
'*********************************************************************************************

Class OutputOptionsDataFeedView

    Public Overrides Sub LoadDataFeed(dataFeed As Core.DataFeed)

        MyBase.LoadDataFeed(dataFeed)

        Me.SetCheckBoxBinding(Me.CheckBoxDevAndRoads, "DevAndRoads")
        Me.SetCheckBoxBinding(Me.CheckBoxZoneOfInfluence, "ZoneOfInfluence")
        Me.SetCheckBoxBinding(Me.CheckBoxHarvestZone, "HarvestZone")

        Me.RefreshBoundControls()

    End Sub

End Class
