
Class OutputOptionsDataFeedView

    Public Overrides Sub LoadDataFeed(dataFeed As Core.DataFeed)

        MyBase.LoadDataFeed(dataFeed)

        Me.SetCheckBoxBinding(Me.CheckBoxDevAndRoads, "DevAndRoads")
        Me.SetCheckBoxBinding(Me.CheckBoxZoneOfInfluence, "ZoneOfInfluence")
        Me.SetCheckBoxBinding(Me.CheckBoxHarvestZone, "HarvestZone")

        Me.RefreshBoundControls()

    End Sub

End Class
