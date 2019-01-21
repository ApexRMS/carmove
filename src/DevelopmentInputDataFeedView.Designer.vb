<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class DevelopmentInputDataFeedView
    Inherits SyncroSim.Core.Forms.DataFeedView

    'UserControl overrides dispose to clean up the component list.
    <System.Diagnostics.DebuggerNonUserCode()> _
    Protected Overrides Sub Dispose(ByVal disposing As Boolean)
        Try
            If disposing AndAlso components IsNot Nothing Then
                components.Dispose()
            End If
        Finally
            MyBase.Dispose(disposing)
        End Try
    End Sub

    'Required by the Windows Form Designer
    Private components As System.ComponentModel.IContainer

    'NOTE: The following procedure is required by the Windows Form Designer
    'It can be modified using the Windows Form Designer.  
    'Do not modify it using the code editor.
    <System.Diagnostics.DebuggerStepThrough()> _
    Private Sub InitializeComponent()
        Me.ButtonClearAll = New System.Windows.Forms.Button()
        Me.LabelTotalIterations = New System.Windows.Forms.Label()
        Me.TextBoxZoneOfInfluenceBufferWidthRoads = New System.Windows.Forms.TextBox()
        Me.Label3 = New System.Windows.Forms.Label()
        Me.TextBoxMaximumNewDevRadius = New System.Windows.Forms.TextBox()
        Me.TextBoxFarRadiusFromExistingDev = New System.Windows.Forms.TextBox()
        Me.TextBoxMinimumNewDevRadius = New System.Windows.Forms.TextBox()
        Me.Label6 = New System.Windows.Forms.Label()
        Me.Label5 = New System.Windows.Forms.Label()
        Me.LabelStartJulianDay = New System.Windows.Forms.Label()
        Me.TextBoxZoneOfInfluenceBufferWidthDev = New System.Windows.Forms.TextBox()
        Me.LabelEndYear = New System.Windows.Forms.Label()
        Me.LabelCalvingPeakJulianDay = New System.Windows.Forms.Label()
        Me.TextBoxHarvestZoneBufferWidthRoadsAndDev = New System.Windows.Forms.TextBox()
        Me.TextBoxNumNewDev = New System.Windows.Forms.TextBox()
        Me.TextBoxRelProbOutsideFarRadius = New System.Windows.Forms.TextBox()
        Me.Label4 = New System.Windows.Forms.Label()
        Me.TextBoxNearRadiusFromExistingDev = New System.Windows.Forms.TextBox()
        Me.Label1 = New System.Windows.Forms.Label()
        Me.Label2 = New System.Windows.Forms.Label()
        Me.TextBoxRelProbOutsideNearRadius = New System.Windows.Forms.TextBox()
        Me.TableLayoutPanelMain = New System.Windows.Forms.TableLayoutPanel()
        Me.TableLayoutPanelMain.SuspendLayout()
        Me.SuspendLayout()
        '
        'ButtonClearAll
        '
        Me.ButtonClearAll.Location = New System.Drawing.Point(338, 284)
        Me.ButtonClearAll.Name = "ButtonClearAll"
        Me.ButtonClearAll.Size = New System.Drawing.Size(117, 23)
        Me.ButtonClearAll.TabIndex = 5
        Me.ButtonClearAll.Text = "Clear All"
        Me.ButtonClearAll.UseVisualStyleBackColor = True
        '
        'LabelTotalIterations
        '
        Me.LabelTotalIterations.Anchor = CType((System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Right), System.Windows.Forms.AnchorStyles)
        Me.LabelTotalIterations.AutoSize = True
        Me.LabelTotalIterations.Location = New System.Drawing.Point(167, 83)
        Me.LabelTotalIterations.Margin = New System.Windows.Forms.Padding(3, 5, 3, 0)
        Me.LabelTotalIterations.Name = "LabelTotalIterations"
        Me.LabelTotalIterations.Size = New System.Drawing.Size(151, 13)
        Me.LabelTotalIterations.TabIndex = 6
        Me.LabelTotalIterations.Text = "Number of new developments:"
        Me.LabelTotalIterations.TextAlign = System.Drawing.ContentAlignment.MiddleRight
        '
        'TextBoxZoneOfInfluenceBufferWidthRoads
        '
        Me.TextBoxZoneOfInfluenceBufferWidthRoads.Location = New System.Drawing.Point(324, 29)
        Me.TextBoxZoneOfInfluenceBufferWidthRoads.Name = "TextBoxZoneOfInfluenceBufferWidthRoads"
        Me.TextBoxZoneOfInfluenceBufferWidthRoads.Size = New System.Drawing.Size(117, 20)
        Me.TextBoxZoneOfInfluenceBufferWidthRoads.TabIndex = 3
        Me.TextBoxZoneOfInfluenceBufferWidthRoads.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
        '
        'Label3
        '
        Me.Label3.Anchor = CType((System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Right), System.Windows.Forms.AnchorStyles)
        Me.Label3.AutoSize = True
        Me.Label3.Location = New System.Drawing.Point(109, 187)
        Me.Label3.Margin = New System.Windows.Forms.Padding(3, 5, 3, 0)
        Me.Label3.Name = "Label3"
        Me.Label3.Size = New System.Drawing.Size(209, 13)
        Me.Label3.TabIndex = 14
        Me.Label3.Text = "Far radius from existing developments (km):"
        Me.Label3.TextAlign = System.Drawing.ContentAlignment.MiddleRight
        '
        'TextBoxMaximumNewDevRadius
        '
        Me.TextBoxMaximumNewDevRadius.Location = New System.Drawing.Point(324, 133)
        Me.TextBoxMaximumNewDevRadius.Name = "TextBoxMaximumNewDevRadius"
        Me.TextBoxMaximumNewDevRadius.Size = New System.Drawing.Size(117, 20)
        Me.TextBoxMaximumNewDevRadius.TabIndex = 11
        Me.TextBoxMaximumNewDevRadius.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
        '
        'TextBoxFarRadiusFromExistingDev
        '
        Me.TextBoxFarRadiusFromExistingDev.Location = New System.Drawing.Point(324, 185)
        Me.TextBoxFarRadiusFromExistingDev.Name = "TextBoxFarRadiusFromExistingDev"
        Me.TextBoxFarRadiusFromExistingDev.Size = New System.Drawing.Size(117, 20)
        Me.TextBoxFarRadiusFromExistingDev.TabIndex = 15
        Me.TextBoxFarRadiusFromExistingDev.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
        '
        'TextBoxMinimumNewDevRadius
        '
        Me.TextBoxMinimumNewDevRadius.Location = New System.Drawing.Point(324, 107)
        Me.TextBoxMinimumNewDevRadius.Name = "TextBoxMinimumNewDevRadius"
        Me.TextBoxMinimumNewDevRadius.Size = New System.Drawing.Size(117, 20)
        Me.TextBoxMinimumNewDevRadius.TabIndex = 9
        Me.TextBoxMinimumNewDevRadius.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
        '
        'Label6
        '
        Me.Label6.Anchor = CType((System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Right), System.Windows.Forms.AnchorStyles)
        Me.Label6.AutoSize = True
        Me.Label6.Location = New System.Drawing.Point(129, 135)
        Me.Label6.Margin = New System.Windows.Forms.Padding(3, 5, 3, 0)
        Me.Label6.Name = "Label6"
        Me.Label6.Size = New System.Drawing.Size(189, 13)
        Me.Label6.TabIndex = 10
        Me.Label6.Text = "Maximum new development radius (m):"
        Me.Label6.TextAlign = System.Drawing.ContentAlignment.MiddleRight
        '
        'Label5
        '
        Me.Label5.Anchor = CType((System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Right), System.Windows.Forms.AnchorStyles)
        Me.Label5.AutoSize = True
        Me.Label5.Location = New System.Drawing.Point(132, 109)
        Me.Label5.Margin = New System.Windows.Forms.Padding(3, 5, 3, 0)
        Me.Label5.Name = "Label5"
        Me.Label5.Size = New System.Drawing.Size(186, 13)
        Me.Label5.TabIndex = 8
        Me.Label5.Text = "Minimum new development radius (m):"
        Me.Label5.TextAlign = System.Drawing.ContentAlignment.MiddleRight
        '
        'LabelStartJulianDay
        '
        Me.LabelStartJulianDay.Anchor = CType((System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Right), System.Windows.Forms.AnchorStyles)
        Me.LabelStartJulianDay.AutoSize = True
        Me.LabelStartJulianDay.Location = New System.Drawing.Point(78, 5)
        Me.LabelStartJulianDay.Margin = New System.Windows.Forms.Padding(3, 5, 3, 0)
        Me.LabelStartJulianDay.Name = "LabelStartJulianDay"
        Me.LabelStartJulianDay.Size = New System.Drawing.Size(240, 13)
        Me.LabelStartJulianDay.TabIndex = 0
        Me.LabelStartJulianDay.Text = "Zone of influence buffer width (m): developments:"
        Me.LabelStartJulianDay.TextAlign = System.Drawing.ContentAlignment.MiddleRight
        '
        'TextBoxZoneOfInfluenceBufferWidthDev
        '
        Me.TextBoxZoneOfInfluenceBufferWidthDev.Location = New System.Drawing.Point(324, 3)
        Me.TextBoxZoneOfInfluenceBufferWidthDev.Name = "TextBoxZoneOfInfluenceBufferWidthDev"
        Me.TextBoxZoneOfInfluenceBufferWidthDev.Size = New System.Drawing.Size(117, 20)
        Me.TextBoxZoneOfInfluenceBufferWidthDev.TabIndex = 1
        Me.TextBoxZoneOfInfluenceBufferWidthDev.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
        '
        'LabelEndYear
        '
        Me.LabelEndYear.Anchor = CType((System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Right), System.Windows.Forms.AnchorStyles)
        Me.LabelEndYear.AutoSize = True
        Me.LabelEndYear.Location = New System.Drawing.Point(118, 31)
        Me.LabelEndYear.Margin = New System.Windows.Forms.Padding(3, 5, 3, 0)
        Me.LabelEndYear.Name = "LabelEndYear"
        Me.LabelEndYear.Size = New System.Drawing.Size(200, 13)
        Me.LabelEndYear.TabIndex = 2
        Me.LabelEndYear.Text = "Zone of influence buffer width (m): roads:"
        Me.LabelEndYear.TextAlign = System.Drawing.ContentAlignment.MiddleRight
        '
        'LabelCalvingPeakJulianDay
        '
        Me.LabelCalvingPeakJulianDay.Anchor = CType((System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Right), System.Windows.Forms.AnchorStyles)
        Me.LabelCalvingPeakJulianDay.AutoSize = True
        Me.LabelCalvingPeakJulianDay.Location = New System.Drawing.Point(45, 57)
        Me.LabelCalvingPeakJulianDay.Margin = New System.Windows.Forms.Padding(3, 5, 3, 0)
        Me.LabelCalvingPeakJulianDay.Name = "LabelCalvingPeakJulianDay"
        Me.LabelCalvingPeakJulianDay.Size = New System.Drawing.Size(273, 13)
        Me.LabelCalvingPeakJulianDay.TabIndex = 4
        Me.LabelCalvingPeakJulianDay.Text = "Harvest zone buffer width (m):  developments and roads:"
        Me.LabelCalvingPeakJulianDay.TextAlign = System.Drawing.ContentAlignment.MiddleRight
        '
        'TextBoxHarvestZoneBufferWidthRoadsAndDev
        '
        Me.TextBoxHarvestZoneBufferWidthRoadsAndDev.Location = New System.Drawing.Point(324, 55)
        Me.TextBoxHarvestZoneBufferWidthRoadsAndDev.Name = "TextBoxHarvestZoneBufferWidthRoadsAndDev"
        Me.TextBoxHarvestZoneBufferWidthRoadsAndDev.Size = New System.Drawing.Size(117, 20)
        Me.TextBoxHarvestZoneBufferWidthRoadsAndDev.TabIndex = 5
        Me.TextBoxHarvestZoneBufferWidthRoadsAndDev.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
        '
        'TextBoxNumNewDev
        '
        Me.TextBoxNumNewDev.Location = New System.Drawing.Point(324, 81)
        Me.TextBoxNumNewDev.Name = "TextBoxNumNewDev"
        Me.TextBoxNumNewDev.Size = New System.Drawing.Size(117, 20)
        Me.TextBoxNumNewDev.TabIndex = 7
        Me.TextBoxNumNewDev.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
        '
        'TextBoxRelProbOutsideFarRadius
        '
        Me.TextBoxRelProbOutsideFarRadius.Location = New System.Drawing.Point(324, 237)
        Me.TextBoxRelProbOutsideFarRadius.Name = "TextBoxRelProbOutsideFarRadius"
        Me.TextBoxRelProbOutsideFarRadius.Size = New System.Drawing.Size(117, 20)
        Me.TextBoxRelProbOutsideFarRadius.TabIndex = 19
        Me.TextBoxRelProbOutsideFarRadius.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
        '
        'Label4
        '
        Me.Label4.Anchor = CType((System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Right), System.Windows.Forms.AnchorStyles)
        Me.Label4.AutoSize = True
        Me.Label4.Location = New System.Drawing.Point(48, 239)
        Me.Label4.Margin = New System.Windows.Forms.Padding(3, 5, 3, 0)
        Me.Label4.Name = "Label4"
        Me.Label4.Size = New System.Drawing.Size(270, 13)
        Me.Label4.TabIndex = 18
        Me.Label4.Text = "Relative probability of development outside of far radius:"
        Me.Label4.TextAlign = System.Drawing.ContentAlignment.MiddleRight
        '
        'TextBoxNearRadiusFromExistingDev
        '
        Me.TextBoxNearRadiusFromExistingDev.Location = New System.Drawing.Point(324, 159)
        Me.TextBoxNearRadiusFromExistingDev.Name = "TextBoxNearRadiusFromExistingDev"
        Me.TextBoxNearRadiusFromExistingDev.Size = New System.Drawing.Size(117, 20)
        Me.TextBoxNearRadiusFromExistingDev.TabIndex = 13
        Me.TextBoxNearRadiusFromExistingDev.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
        '
        'Label1
        '
        Me.Label1.Anchor = CType((System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Right), System.Windows.Forms.AnchorStyles)
        Me.Label1.AutoSize = True
        Me.Label1.Location = New System.Drawing.Point(101, 161)
        Me.Label1.Margin = New System.Windows.Forms.Padding(3, 5, 3, 0)
        Me.Label1.Name = "Label1"
        Me.Label1.Size = New System.Drawing.Size(217, 13)
        Me.Label1.TabIndex = 12
        Me.Label1.Text = "Near radius from existing developments (km):"
        Me.Label1.TextAlign = System.Drawing.ContentAlignment.MiddleRight
        '
        'Label2
        '
        Me.Label2.Anchor = CType((System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Right), System.Windows.Forms.AnchorStyles)
        Me.Label2.AutoSize = True
        Me.Label2.Location = New System.Drawing.Point(39, 213)
        Me.Label2.Margin = New System.Windows.Forms.Padding(3, 5, 3, 0)
        Me.Label2.Name = "Label2"
        Me.Label2.Size = New System.Drawing.Size(279, 13)
        Me.Label2.TabIndex = 16
        Me.Label2.Text = "Relative probability of development outside of near radius:"
        Me.Label2.TextAlign = System.Drawing.ContentAlignment.MiddleRight
        '
        'TextBoxRelProbOutsideNearRadius
        '
        Me.TextBoxRelProbOutsideNearRadius.Location = New System.Drawing.Point(324, 211)
        Me.TextBoxRelProbOutsideNearRadius.Name = "TextBoxRelProbOutsideNearRadius"
        Me.TextBoxRelProbOutsideNearRadius.Size = New System.Drawing.Size(117, 20)
        Me.TextBoxRelProbOutsideNearRadius.TabIndex = 17
        Me.TextBoxRelProbOutsideNearRadius.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
        '
        'TableLayoutPanelMain
        '
        Me.TableLayoutPanelMain.ColumnCount = 2
        Me.TableLayoutPanelMain.ColumnStyles.Add(New System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 58.79121!))
        Me.TableLayoutPanelMain.ColumnStyles.Add(New System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 41.20879!))
        Me.TableLayoutPanelMain.Controls.Add(Me.LabelTotalIterations, 0, 3)
        Me.TableLayoutPanelMain.Controls.Add(Me.TextBoxZoneOfInfluenceBufferWidthRoads, 1, 1)
        Me.TableLayoutPanelMain.Controls.Add(Me.Label3, 0, 7)
        Me.TableLayoutPanelMain.Controls.Add(Me.TextBoxMaximumNewDevRadius, 1, 5)
        Me.TableLayoutPanelMain.Controls.Add(Me.TextBoxFarRadiusFromExistingDev, 1, 7)
        Me.TableLayoutPanelMain.Controls.Add(Me.TextBoxMinimumNewDevRadius, 1, 4)
        Me.TableLayoutPanelMain.Controls.Add(Me.Label6, 0, 5)
        Me.TableLayoutPanelMain.Controls.Add(Me.Label5, 0, 4)
        Me.TableLayoutPanelMain.Controls.Add(Me.LabelStartJulianDay, 0, 0)
        Me.TableLayoutPanelMain.Controls.Add(Me.TextBoxZoneOfInfluenceBufferWidthDev, 1, 0)
        Me.TableLayoutPanelMain.Controls.Add(Me.LabelEndYear, 0, 1)
        Me.TableLayoutPanelMain.Controls.Add(Me.LabelCalvingPeakJulianDay, 0, 2)
        Me.TableLayoutPanelMain.Controls.Add(Me.TextBoxHarvestZoneBufferWidthRoadsAndDev, 1, 2)
        Me.TableLayoutPanelMain.Controls.Add(Me.TextBoxNumNewDev, 1, 3)
        Me.TableLayoutPanelMain.Controls.Add(Me.TextBoxRelProbOutsideFarRadius, 1, 9)
        Me.TableLayoutPanelMain.Controls.Add(Me.Label4, 0, 9)
        Me.TableLayoutPanelMain.Controls.Add(Me.TextBoxNearRadiusFromExistingDev, 1, 6)
        Me.TableLayoutPanelMain.Controls.Add(Me.Label1, 0, 6)
        Me.TableLayoutPanelMain.Controls.Add(Me.Label2, 0, 8)
        Me.TableLayoutPanelMain.Controls.Add(Me.TextBoxRelProbOutsideNearRadius, 1, 8)
        Me.TableLayoutPanelMain.GrowStyle = System.Windows.Forms.TableLayoutPanelGrowStyle.FixedSize
        Me.TableLayoutPanelMain.Location = New System.Drawing.Point(14, 14)
        Me.TableLayoutPanelMain.Name = "TableLayoutPanelMain"
        Me.TableLayoutPanelMain.RowCount = 10
        Me.TableLayoutPanelMain.RowStyles.Add(New System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10.0!))
        Me.TableLayoutPanelMain.RowStyles.Add(New System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10.0!))
        Me.TableLayoutPanelMain.RowStyles.Add(New System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10.0!))
        Me.TableLayoutPanelMain.RowStyles.Add(New System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10.0!))
        Me.TableLayoutPanelMain.RowStyles.Add(New System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10.0!))
        Me.TableLayoutPanelMain.RowStyles.Add(New System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10.0!))
        Me.TableLayoutPanelMain.RowStyles.Add(New System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10.0!))
        Me.TableLayoutPanelMain.RowStyles.Add(New System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10.0!))
        Me.TableLayoutPanelMain.RowStyles.Add(New System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10.0!))
        Me.TableLayoutPanelMain.RowStyles.Add(New System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10.0!))
        Me.TableLayoutPanelMain.Size = New System.Drawing.Size(546, 264)
        Me.TableLayoutPanelMain.TabIndex = 4
        '
        'DevelopmentInputDataFeedView
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(6.0!, 13.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.Controls.Add(Me.ButtonClearAll)
        Me.Controls.Add(Me.TableLayoutPanelMain)
        Me.Name = "DevelopmentInputDataFeedView"
        Me.Size = New System.Drawing.Size(573, 317)
        Me.TableLayoutPanelMain.ResumeLayout(False)
        Me.TableLayoutPanelMain.PerformLayout()
        Me.ResumeLayout(False)

    End Sub

    Friend WithEvents ButtonClearAll As Windows.Forms.Button
    Friend WithEvents LabelTotalIterations As Windows.Forms.Label
    Friend WithEvents TextBoxZoneOfInfluenceBufferWidthRoads As Windows.Forms.TextBox
    Friend WithEvents Label3 As Windows.Forms.Label
    Friend WithEvents TextBoxMaximumNewDevRadius As Windows.Forms.TextBox
    Friend WithEvents TextBoxFarRadiusFromExistingDev As Windows.Forms.TextBox
    Friend WithEvents TextBoxMinimumNewDevRadius As Windows.Forms.TextBox
    Friend WithEvents Label6 As Windows.Forms.Label
    Friend WithEvents Label5 As Windows.Forms.Label
    Friend WithEvents LabelStartJulianDay As Windows.Forms.Label
    Friend WithEvents TextBoxZoneOfInfluenceBufferWidthDev As Windows.Forms.TextBox
    Friend WithEvents LabelEndYear As Windows.Forms.Label
    Friend WithEvents LabelCalvingPeakJulianDay As Windows.Forms.Label
    Friend WithEvents TextBoxHarvestZoneBufferWidthRoadsAndDev As Windows.Forms.TextBox
    Friend WithEvents TextBoxNumNewDev As Windows.Forms.TextBox
    Friend WithEvents TextBoxRelProbOutsideFarRadius As Windows.Forms.TextBox
    Friend WithEvents Label4 As Windows.Forms.Label
    Friend WithEvents TextBoxNearRadiusFromExistingDev As Windows.Forms.TextBox
    Friend WithEvents Label1 As Windows.Forms.Label
    Friend WithEvents Label2 As Windows.Forms.Label
    Friend WithEvents TextBoxRelProbOutsideNearRadius As Windows.Forms.TextBox
    Friend WithEvents TableLayoutPanelMain As Windows.Forms.TableLayoutPanel
End Class
