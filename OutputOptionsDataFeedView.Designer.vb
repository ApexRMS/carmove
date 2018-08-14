<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class OutputOptionsDataFeedView
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
        Me.CheckBoxDevAndRoads = New System.Windows.Forms.CheckBox()
        Me.CheckBoxHarvestZone = New System.Windows.Forms.CheckBox()
        Me.CheckBoxZoneOfInfluence = New System.Windows.Forms.CheckBox()
        Me.GroupBox1 = New System.Windows.Forms.GroupBox()
        Me.GroupBox1.SuspendLayout()
        Me.SuspendLayout()
        '
        'CheckBoxDevAndRoads
        '
        Me.CheckBoxDevAndRoads.AutoSize = True
        Me.CheckBoxDevAndRoads.Location = New System.Drawing.Point(17, 33)
        Me.CheckBoxDevAndRoads.Name = "CheckBoxDevAndRoads"
        Me.CheckBoxDevAndRoads.Size = New System.Drawing.Size(142, 17)
        Me.CheckBoxDevAndRoads.TabIndex = 0
        Me.CheckBoxDevAndRoads.Text = "Roads and development"
        Me.CheckBoxDevAndRoads.UseVisualStyleBackColor = True
        '
        'CheckBoxHarvestZone
        '
        Me.CheckBoxHarvestZone.AutoSize = True
        Me.CheckBoxHarvestZone.Location = New System.Drawing.Point(17, 79)
        Me.CheckBoxHarvestZone.Name = "CheckBoxHarvestZone"
        Me.CheckBoxHarvestZone.Size = New System.Drawing.Size(89, 17)
        Me.CheckBoxHarvestZone.TabIndex = 2
        Me.CheckBoxHarvestZone.Text = "Harvest zone"
        Me.CheckBoxHarvestZone.UseVisualStyleBackColor = True
        '
        'CheckBoxZoneOfInfluence
        '
        Me.CheckBoxZoneOfInfluence.AutoSize = True
        Me.CheckBoxZoneOfInfluence.Location = New System.Drawing.Point(17, 56)
        Me.CheckBoxZoneOfInfluence.Name = "CheckBoxZoneOfInfluence"
        Me.CheckBoxZoneOfInfluence.Size = New System.Drawing.Size(109, 17)
        Me.CheckBoxZoneOfInfluence.TabIndex = 1
        Me.CheckBoxZoneOfInfluence.Text = "Zone of influence"
        Me.CheckBoxZoneOfInfluence.UseVisualStyleBackColor = True
        '
        'GroupBox1
        '
        Me.GroupBox1.Controls.Add(Me.CheckBoxDevAndRoads)
        Me.GroupBox1.Controls.Add(Me.CheckBoxHarvestZone)
        Me.GroupBox1.Controls.Add(Me.CheckBoxZoneOfInfluence)
        Me.GroupBox1.Location = New System.Drawing.Point(14, 13)
        Me.GroupBox1.Name = "GroupBox1"
        Me.GroupBox1.Size = New System.Drawing.Size(204, 116)
        Me.GroupBox1.TabIndex = 1
        Me.GroupBox1.TabStop = False
        Me.GroupBox1.Text = "Spatial"
        '
        'OutputOptionsDataFeedView
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(6.0!, 13.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.Controls.Add(Me.GroupBox1)
        Me.Name = "OutputOptionsDataFeedView"
        Me.Size = New System.Drawing.Size(234, 144)
        Me.GroupBox1.ResumeLayout(False)
        Me.GroupBox1.PerformLayout()
        Me.ResumeLayout(False)

    End Sub

    Friend WithEvents CheckBoxDevAndRoads As Windows.Forms.CheckBox
    Friend WithEvents CheckBoxHarvestZone As Windows.Forms.CheckBox
    Friend WithEvents CheckBoxZoneOfInfluence As Windows.Forms.CheckBox
    Friend WithEvents GroupBox1 As Windows.Forms.GroupBox
End Class
