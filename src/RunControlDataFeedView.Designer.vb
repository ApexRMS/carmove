<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class RunControlDataFeedView
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
        Me.TableLayoutPanelMain = New System.Windows.Forms.TableLayoutPanel()
        Me.LabelTotalIterations = New System.Windows.Forms.Label()
        Me.ButtonClearAll = New System.Windows.Forms.Button()
        Me.TextBoxEndYear = New System.Windows.Forms.TextBox()
        Me.LabelStartJulianDay = New System.Windows.Forms.Label()
        Me.TextBoxStartJulianDay = New System.Windows.Forms.TextBox()
        Me.LabelEndYear = New System.Windows.Forms.Label()
        Me.LabelCalvingPeakJulianDay = New System.Windows.Forms.Label()
        Me.TextBoxCalvingPeakJulianDay = New System.Windows.Forms.TextBox()
        Me.TextBoxTotalIterations = New System.Windows.Forms.TextBox()
        Me.TableLayoutPanelMain.SuspendLayout()
        Me.SuspendLayout()
        '
        'TableLayoutPanelMain
        '
        Me.TableLayoutPanelMain.ColumnCount = 2
        Me.TableLayoutPanelMain.ColumnStyles.Add(New System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 36.5285!))
        Me.TableLayoutPanelMain.ColumnStyles.Add(New System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 63.4715!))
        Me.TableLayoutPanelMain.Controls.Add(Me.LabelTotalIterations, 0, 3)
        Me.TableLayoutPanelMain.Controls.Add(Me.ButtonClearAll, 1, 4)
        Me.TableLayoutPanelMain.Controls.Add(Me.TextBoxEndYear, 1, 1)
        Me.TableLayoutPanelMain.Controls.Add(Me.LabelStartJulianDay, 0, 0)
        Me.TableLayoutPanelMain.Controls.Add(Me.TextBoxStartJulianDay, 1, 0)
        Me.TableLayoutPanelMain.Controls.Add(Me.LabelEndYear, 0, 1)
        Me.TableLayoutPanelMain.Controls.Add(Me.LabelCalvingPeakJulianDay, 0, 2)
        Me.TableLayoutPanelMain.Controls.Add(Me.TextBoxCalvingPeakJulianDay, 1, 2)
        Me.TableLayoutPanelMain.Controls.Add(Me.TextBoxTotalIterations, 1, 3)
        Me.TableLayoutPanelMain.GrowStyle = System.Windows.Forms.TableLayoutPanelGrowStyle.FixedSize
        Me.TableLayoutPanelMain.Location = New System.Drawing.Point(12, 13)
        Me.TableLayoutPanelMain.Name = "TableLayoutPanelMain"
        Me.TableLayoutPanelMain.RowCount = 5
        Me.TableLayoutPanelMain.RowStyles.Add(New System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 20.0!))
        Me.TableLayoutPanelMain.RowStyles.Add(New System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 20.0!))
        Me.TableLayoutPanelMain.RowStyles.Add(New System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 20.0!))
        Me.TableLayoutPanelMain.RowStyles.Add(New System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 20.0!))
        Me.TableLayoutPanelMain.RowStyles.Add(New System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 20.0!))
        Me.TableLayoutPanelMain.Size = New System.Drawing.Size(386, 147)
        Me.TableLayoutPanelMain.TabIndex = 2
        '
        'LabelTotalIterations
        '
        Me.LabelTotalIterations.Anchor = CType((System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Right), System.Windows.Forms.AnchorStyles)
        Me.LabelTotalIterations.AutoSize = True
        Me.LabelTotalIterations.Location = New System.Drawing.Point(34, 92)
        Me.LabelTotalIterations.Margin = New System.Windows.Forms.Padding(3, 5, 3, 0)
        Me.LabelTotalIterations.Name = "LabelTotalIterations"
        Me.LabelTotalIterations.Size = New System.Drawing.Size(104, 13)
        Me.LabelTotalIterations.TabIndex = 6
        Me.LabelTotalIterations.Text = "Number of iterations:"
        Me.LabelTotalIterations.TextAlign = System.Drawing.ContentAlignment.MiddleRight
        '
        'ButtonClearAll
        '
        Me.ButtonClearAll.Location = New System.Drawing.Point(144, 119)
        Me.ButtonClearAll.Name = "ButtonClearAll"
        Me.ButtonClearAll.Size = New System.Drawing.Size(117, 23)
        Me.ButtonClearAll.TabIndex = 8
        Me.ButtonClearAll.Text = "Clear All"
        Me.ButtonClearAll.UseVisualStyleBackColor = True
        '
        'TextBoxEndYear
        '
        Me.TextBoxEndYear.Location = New System.Drawing.Point(144, 32)
        Me.TextBoxEndYear.Name = "TextBoxEndYear"
        Me.TextBoxEndYear.Size = New System.Drawing.Size(117, 20)
        Me.TextBoxEndYear.TabIndex = 3
        Me.TextBoxEndYear.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
        '
        'LabelStartJulianDay
        '
        Me.LabelStartJulianDay.Anchor = CType((System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Right), System.Windows.Forms.AnchorStyles)
        Me.LabelStartJulianDay.AutoSize = True
        Me.LabelStartJulianDay.Location = New System.Drawing.Point(59, 5)
        Me.LabelStartJulianDay.Margin = New System.Windows.Forms.Padding(3, 5, 3, 0)
        Me.LabelStartJulianDay.Name = "LabelStartJulianDay"
        Me.LabelStartJulianDay.Size = New System.Drawing.Size(79, 13)
        Me.LabelStartJulianDay.TabIndex = 0
        Me.LabelStartJulianDay.Text = "Start julian day:"
        Me.LabelStartJulianDay.TextAlign = System.Drawing.ContentAlignment.MiddleRight
        '
        'TextBoxStartJulianDay
        '
        Me.TextBoxStartJulianDay.Location = New System.Drawing.Point(144, 3)
        Me.TextBoxStartJulianDay.Name = "TextBoxStartJulianDay"
        Me.TextBoxStartJulianDay.Size = New System.Drawing.Size(117, 20)
        Me.TextBoxStartJulianDay.TabIndex = 1
        Me.TextBoxStartJulianDay.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
        '
        'LabelEndYear
        '
        Me.LabelEndYear.Anchor = CType((System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Right), System.Windows.Forms.AnchorStyles)
        Me.LabelEndYear.AutoSize = True
        Me.LabelEndYear.Location = New System.Drawing.Point(51, 34)
        Me.LabelEndYear.Margin = New System.Windows.Forms.Padding(3, 5, 3, 0)
        Me.LabelEndYear.Name = "LabelEndYear"
        Me.LabelEndYear.Size = New System.Drawing.Size(87, 13)
        Me.LabelEndYear.TabIndex = 2
        Me.LabelEndYear.Text = "Number of years:"
        Me.LabelEndYear.TextAlign = System.Drawing.ContentAlignment.MiddleRight
        '
        'LabelCalvingPeakJulianDay
        '
        Me.LabelCalvingPeakJulianDay.Anchor = CType((System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Right), System.Windows.Forms.AnchorStyles)
        Me.LabelCalvingPeakJulianDay.AutoSize = True
        Me.LabelCalvingPeakJulianDay.Location = New System.Drawing.Point(19, 63)
        Me.LabelCalvingPeakJulianDay.Margin = New System.Windows.Forms.Padding(3, 5, 3, 0)
        Me.LabelCalvingPeakJulianDay.Name = "LabelCalvingPeakJulianDay"
        Me.LabelCalvingPeakJulianDay.Size = New System.Drawing.Size(119, 13)
        Me.LabelCalvingPeakJulianDay.TabIndex = 4
        Me.LabelCalvingPeakJulianDay.Text = "Calving peak julian day:"
        Me.LabelCalvingPeakJulianDay.TextAlign = System.Drawing.ContentAlignment.MiddleRight
        '
        'TextBoxCalvingPeakJulianDay
        '
        Me.TextBoxCalvingPeakJulianDay.Location = New System.Drawing.Point(144, 61)
        Me.TextBoxCalvingPeakJulianDay.Name = "TextBoxCalvingPeakJulianDay"
        Me.TextBoxCalvingPeakJulianDay.Size = New System.Drawing.Size(117, 20)
        Me.TextBoxCalvingPeakJulianDay.TabIndex = 5
        Me.TextBoxCalvingPeakJulianDay.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
        '
        'TextBoxTotalIterations
        '
        Me.TextBoxTotalIterations.Location = New System.Drawing.Point(144, 90)
        Me.TextBoxTotalIterations.Name = "TextBoxTotalIterations"
        Me.TextBoxTotalIterations.Size = New System.Drawing.Size(117, 20)
        Me.TextBoxTotalIterations.TabIndex = 7
        Me.TextBoxTotalIterations.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
        '
        'RunControlDataFeedView
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(6.0!, 13.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.Controls.Add(Me.TableLayoutPanelMain)
        Me.Name = "RunControlDataFeedView"
        Me.Size = New System.Drawing.Size(409, 172)
        Me.TableLayoutPanelMain.ResumeLayout(False)
        Me.TableLayoutPanelMain.PerformLayout()
        Me.ResumeLayout(False)

    End Sub

    Friend WithEvents TableLayoutPanelMain As Windows.Forms.TableLayoutPanel
    Friend WithEvents LabelTotalIterations As Windows.Forms.Label
    Friend WithEvents ButtonClearAll As Windows.Forms.Button
    Friend WithEvents TextBoxEndYear As Windows.Forms.TextBox
    Friend WithEvents LabelStartJulianDay As Windows.Forms.Label
    Friend WithEvents TextBoxStartJulianDay As Windows.Forms.TextBox
    Friend WithEvents LabelEndYear As Windows.Forms.Label
    Friend WithEvents LabelCalvingPeakJulianDay As Windows.Forms.Label
    Friend WithEvents TextBoxCalvingPeakJulianDay As Windows.Forms.TextBox
    Friend WithEvents TextBoxTotalIterations As Windows.Forms.TextBox
End Class
