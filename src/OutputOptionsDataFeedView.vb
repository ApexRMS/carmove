'*********************************************************************************************
' carmove: SyncroSim Base Package for simulating the movement of caribou across a landscape.
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
