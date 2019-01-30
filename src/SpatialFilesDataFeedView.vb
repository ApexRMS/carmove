'*********************************************************************************************
' Caribou Movement: A SyncroSim Package for simulating movement patterns of caribou populations
' and their interaction with industrial developments.
'
' Copyright © 2007-2019 Apex Resource Management Solution Ltd. (ApexRMS). All rights reserved.
'*********************************************************************************************

Imports System.IO
Imports SyncroSim.Core
Imports System.Windows.Forms

Class SpatialFilesDataFeedView

    Private Function GetDataSheet() As DataSheet
        Return Me.DataFeed.GetDataSheet("CM_SpatialFiles")
    End Function

    Public Overrides Sub LoadDataFeed(dataFeed As Core.DataFeed)

        MyBase.LoadDataFeed(dataFeed)

        SetCheckBoxBinding(CheckBoxSampleRandomCollar, "SampleRandomCollarYear")

        Me.TextBoxCollarFile.Text = Nothing
        Me.TextBoxExistingDevStatusShapeFile.Text = Nothing
        Me.TextBoxExistingRoadsShapeFile.Text = Nothing
        Me.TextBoxStratumLabelXRasterFile.Text = Nothing
        Me.TextBoxStratumLabelYShapeFile.Text = Nothing
        Me.TextBoxHarvestZoneShapeFile.Text = Nothing
        Me.TextBoxRangeAssessmentAreaShapeFile.Text = Nothing

        Dim dr As DataRow = Me.GetDataSheet.GetDataRow()

        If (dr IsNot Nothing) Then

            Me.TextBoxCollarFile.Text = Utilities.GetDataStr(dr, "CollarDataFile")
            Me.TextBoxExistingDevStatusShapeFile.Text = Utilities.GetDataStr(dr, "ExistingStratumLabelZShapeFile")
            Me.TextBoxExistingRoadsShapeFile.Text = Utilities.GetDataStr(dr, "ExistingRoadsShapeFile")
            Me.TextBoxStratumLabelXRasterFile.Text = Utilities.GetDataStr(dr, "StratumLabelXRasterFile")
            Me.TextBoxStratumLabelYShapeFile.Text = Utilities.GetDataStr(dr, "StratumLabelYShapeFile")
            Me.TextBoxHarvestZoneShapeFile.Text = Utilities.GetDataStr(dr, "HarvestZoneShapeFile")
            Me.TextBoxRangeAssessmentAreaShapeFile.Text = Utilities.GetDataStr(dr, "RangeAssessmentAreaShapeFile")

        End If

    End Sub

    Private Sub ChangeFile(ByVal tb As TextBox, ByVal columnName As String, ByVal fileName As String)

        Dim f As String = Path.GetFileName(fileName)

        tb.Text = f
        Me.GetDataSheet.SetSingleRowData(columnName, f)
        Me.GetDataSheet.AddExternalInputFile(fileName)

    End Sub

    Private Sub ChangeShapeFile(ByVal tb As TextBox, ByVal columnName As String, ByVal fileName As String)

        Dim ds As DataSheet = Me.GetDataSheet()
        Dim dirname As String = Path.GetDirectoryName(fileName)
        Dim namenoext As String = Path.GetFileNameWithoutExtension(fileName)

        Dim shpfile As String = fileName
        Dim shxfile As String = Path.Combine(dirname, namenoext) & ".shx"
        Dim dbffile As String = Path.Combine(dirname, namenoext) & ".dbf"
        Dim prjfile As String = Path.Combine(dirname, namenoext) & ".prj"

        Dim shpfileNameOnly As String = Path.GetFileName(shpfile)
        Dim shxfileNameOnly As String = Path.GetFileName(shxfile)
        Dim dbffileNameOnly As String = Path.GetFileName(dbffile)
        Dim prjfileNameOnly As String = Path.GetFileName(prjfile)

        tb.Text = shpfileNameOnly

        ds.AddExternalInputFile(shpfile)
        ds.SetSingleRowData(columnName, shpfileNameOnly)

        ds.BeginModifyRows()

        If (File.Exists(shxfile)) Then
            ds.AddExternalInputFile(shxfile)
            ds.SetSingleRowData(columnName & "Shx", shxfileNameOnly)
        End If

        If (File.Exists(dbffile)) Then
            ds.AddExternalInputFile(dbffile)
            ds.SetSingleRowData(columnName & "Dbf", dbffileNameOnly)
        End If

        If (File.Exists(prjfile)) Then
            ds.AddExternalInputFile(prjfile)
            ds.SetSingleRowData(columnName & "Prj", prjfileNameOnly)
        End If

        ds.EndModifyRows()

    End Sub

    Private Sub ClearFile(ByVal tb As TextBox, ByVal columnName As String)

        tb.Text = Nothing
        Me.GetDataSheet().SetSingleRowData(columnName, Nothing)

    End Sub

    Private Sub ClearShapeFile(ByVal tb As TextBox, ByVal columnName As String)

        tb.Text = Nothing

        Dim ds As DataSheet = Me.GetDataSheet()

        ds.BeginModifyRows()

        ds.SetSingleRowData(columnName, Nothing)
        ds.SetSingleRowData(columnName & "Shx", Nothing)
        ds.SetSingleRowData(columnName & "Dbf", Nothing)
        ds.SetSingleRowData(columnName & "Prj", Nothing)

        ds.EndModifyRows()

    End Sub

    Private Sub ButtonCollarFileBrowse_Click(sender As System.Object, e As System.EventArgs) Handles ButtonChooseCollarFile.Click

        Dim dlg As New OpenFileDialog()

        dlg.Title = "Collar Data File"
        dlg.Filter = "Collar Data File (*.csv)|*.csv"

        If (dlg.ShowDialog(Me) = DialogResult.OK) Then
            Me.ChangeFile(Me.TextBoxCollarFile, "CollarDataFile", dlg.FileName)
        End If

    End Sub

    Private Sub ButtonCollarFileClear_Click(sender As System.Object, e As System.EventArgs) Handles ButtonClearCollarFile.Click
        Me.ClearFile(Me.TextBoxCollarFile, "CollarDataFile")
    End Sub

    Private Sub ButtonChooseExistingDevStatusShapeFile_Click(sender As System.Object, e As System.EventArgs) Handles ButtonChooseExistingDevStatusShapeFile.Click

        Dim dlg As New OpenFileDialog

        dlg.Title = "Existing Development Status Shapefile"
        dlg.Filter = "Shapefile (*.shp)|*.shp"

        If (dlg.ShowDialog(Me) = DialogResult.OK) Then
            Me.ChangeShapeFile(Me.TextBoxExistingDevStatusShapeFile, "ExistingStratumLabelZShapeFile", dlg.FileName)
        End If

    End Sub

    Private Sub ButtonClearExistingDevStatusShapeFile_Click(sender As System.Object, e As System.EventArgs) Handles ButtonClearExistingDevStatusShapeFile.Click
        Me.ClearShapeFile(Me.TextBoxExistingDevStatusShapeFile, "ExistingStratumLabelZShapeFile")
    End Sub

    Private Sub ButtonChooseExistingRoadsShapeFile_Click(sender As System.Object, e As System.EventArgs) Handles ButtonChooseExistingRoadsShapeFile.Click

        Dim dlg As New OpenFileDialog

        dlg.Title = "Existing Roads Shapefile"
        dlg.Filter = "Shapefile (*.shp)|*.shp"

        If (dlg.ShowDialog(Me) = DialogResult.OK) Then
            Me.ChangeShapeFile(Me.TextBoxExistingRoadsShapeFile, "ExistingRoadsShapeFile", dlg.FileName)
        End If

    End Sub

    Private Sub ButtonClearExistingRoadsShapeFile_Click(sender As System.Object, e As System.EventArgs) Handles ButtonClearExistingRoadsShapeFile.Click
        Me.ClearShapeFile(Me.TextBoxExistingRoadsShapeFile, "ExistingRoadsShapeFile")
    End Sub

    Private Sub ButtonChooseExistingStratumLabelXRasterFile_Click(sender As System.Object, e As System.EventArgs) Handles ButtonChooseStratumLabelXRasterFile.Click

        Dim dlg As New OpenFileDialog

        dlg.Title = "Vegetation Type Raster File"
        dlg.Filter = "Raster File (*.tif)|*.tif"

        If (dlg.ShowDialog(Me) = DialogResult.OK) Then
            Me.ChangeFile(Me.TextBoxStratumLabelXRasterFile, "StratumLabelXRasterFile", dlg.FileName)
        End If

    End Sub

    Private Sub ButtonClearExistingStratumLabelXRasterFile_Click(sender As System.Object, e As System.EventArgs) Handles ButtonClearStratumLabelXRasterFile.Click
        Me.ClearFile(Me.TextBoxStratumLabelXRasterFile, "StratumLabelXRasterFile")
    End Sub

    Private Sub Button2_Click(sender As System.Object, e As System.EventArgs) Handles ButtonChooseStratumLabelYShapeFile.Click

        Dim dlg As New OpenFileDialog

        dlg.Title = "Climate Zone Shapefile"
        dlg.Filter = "Shapefile (*.shp)|*.shp"

        If (dlg.ShowDialog(Me) = DialogResult.OK) Then
            Me.ChangeShapeFile(Me.TextBoxStratumLabelYShapeFile, "StratumLabelYShapeFile", dlg.FileName)
        End If

    End Sub

    Private Sub Button1_Click(sender As System.Object, e As System.EventArgs) Handles ButtonClearStratumLabelYShapeFile.Click
        Me.ClearShapeFile(Me.TextBoxStratumLabelYShapeFile, "StratumLabelYShapeFile")
    End Sub

    Private Sub ButtonChooseHarvestZoneShapeFile_Click(sender As System.Object, e As System.EventArgs) Handles ButtonChooseHarvestZoneShapeFile.Click

        Dim dlg As New OpenFileDialog

        dlg.Title = "Harvest Zone Shapefile"
        dlg.Filter = "Shapefile (*.shp)|*.shp"

        If (dlg.ShowDialog(Me) = DialogResult.OK) Then
            Me.ChangeShapeFile(Me.TextBoxHarvestZoneShapeFile, "HarvestZoneShapeFile", dlg.FileName)
        End If

    End Sub

    Private Sub ButtonClearHarvestZoneShapeFile_Click(sender As System.Object, e As System.EventArgs) Handles ButtonClearHarvestZoneShapeFile.Click
        Me.ClearShapeFile(Me.TextBoxHarvestZoneShapeFile, "HarvestZoneShapeFile")
    End Sub

    Private Sub ButtonChooseRangeAssessmentAreaShapeFile_Click(sender As System.Object, e As System.EventArgs) Handles ButtonChooseRangeAssessmentAreaShapeFile.Click

        Dim dlg As New OpenFileDialog

        dlg.Title = "Range Assessment Area Shapefile"
        dlg.Filter = "Shapefile (*.shp)|*.shp"

        If (dlg.ShowDialog(Me) = DialogResult.OK) Then
            Me.ChangeShapeFile(Me.TextBoxRangeAssessmentAreaShapeFile, "RangeAssessmentAreaShapeFile", dlg.FileName)
        End If

    End Sub

    Private Sub ButtonClearRangeAssessmentAreaShapeFile_Click(sender As System.Object, e As System.EventArgs) Handles ButtonClearRangeAssessmentAreaShapeFile.Click
        Me.ClearShapeFile(Me.TextBoxRangeAssessmentAreaShapeFile, "RangeAssessmentAreaShapeFile")
    End Sub
End Class
