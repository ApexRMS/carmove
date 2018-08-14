
Imports System.Globalization
Imports System.IO
Imports System.Text.RegularExpressions
Imports System.Windows.Forms
Imports SyncroSim.Core
Imports SyncroSim.StochasticTime

Module Utilities

    Public Function GetDataStr(dr As DataRow, columnName As String) As String
        Return GetDataStr(dr(columnName))
    End Function

    Public Function GetDataStr(value As Object) As String
        If (Object.ReferenceEquals(value, DBNull.Value)) Then
            Return Nothing
        Else
            Return Convert.ToString(value, CultureInfo.InvariantCulture)
        End If
    End Function

    Public Sub GetTerminology(
        ByVal project As Project,
        ByRef outStratumLabelX As String,
        ByRef outStratumLabelY As String,
        ByRef outStratumLabelZ As String,
        ByRef outTimestepUnits As String)

        outStratumLabelX = "Stratum Label X"
        outStratumLabelY = "Stratum Label Y"
        outStratumLabelZ = "Stratum Label Z"
        outTimestepUnits = "Timestep"

        Dim dr As DataRow = project.GetDataSheet(TERMINOLOGY_DATA_SHEET_NAME).GetDataRow()

        If (dr Is Nothing) Then
            Return
        End If

        If (dr(TERMINOLOGY_STRATUM_LABEL_X_COLUMN_NAME) IsNot DBNull.Value) Then
            outStratumLabelX = CStr(dr(TERMINOLOGY_STRATUM_LABEL_X_COLUMN_NAME))
        End If

        If (dr(TERMINOLOGY_STRATUM_LABEL_Y_COLUMN_NAME) IsNot DBNull.Value) Then
            outStratumLabelY = CStr(dr(TERMINOLOGY_STRATUM_LABEL_Y_COLUMN_NAME))
        End If

        If (dr(TERMINOLOGY_STRATUM_LABEL_Z_COLUMN_NAME) IsNot DBNull.Value) Then
            outStratumLabelZ = CStr(dr(TERMINOLOGY_STRATUM_LABEL_Z_COLUMN_NAME))
        End If

        If (dr(TERMINOLOGY_TIMESTEP_UNITS_COLUMN_NAME) IsNot DBNull.Value) Then
            outTimestepUnits = CStr(dr(TERMINOLOGY_TIMESTEP_UNITS_COLUMN_NAME))
        End If

    End Sub

    Function ErrorMessageBox(text As [String]) As DialogResult
        Return MessageBox.Show(text, Application.ProductName, MessageBoxButtons.OK, MessageBoxIcon.[Error], MessageBoxDefaultButton.Button1, DirectCast(0, MessageBoxOptions))
    End Function

    Function ErrorMessageBox(text As [String], ParamArray args As Object()) As DialogResult
        Return ErrorMessageBox([String].Format(CultureInfo.InvariantCulture, text, args))
    End Function

    Function ApplicationMessageBox(text As [String], buttons As MessageBoxButtons) As DialogResult
        Return MessageBox.Show(text, Application.ProductName, buttons, MessageBoxIcon.None, MessageBoxDefaultButton.Button1, DirectCast(0, MessageBoxOptions))
    End Function

    Function ApplicationMessageBox(text As [String], buttons As MessageBoxButtons, ParamArray args As Object()) As DialogResult
        Return ApplicationMessageBox([String].Format(CultureInfo.InvariantCulture, text, args), buttons)
    End Function

    Function InformationMessageBox(text As [String]) As DialogResult
        Return ApplicationMessageBox(text, MessageBoxButtons.OK)
    End Function

    Function InformationMessageBox(text As [String], ParamArray args As Object()) As DialogResult
        Return ApplicationMessageBox(text, MessageBoxButtons.OK, args)
    End Function

    Delegate Function RenameExportFileDelegate(ByVal sourceName As String) As String

    Public Sub CopyRasterFiles(
        ByVal resultScenarios As IEnumerable(Of Scenario),
        ByVal fileFilterRegex As String,
        ByVal destFolderName As String,
        ByVal renameExportFileFunction As RenameExportFileDelegate)

        ' We need to repackage the raster files as specified by the Multiband Grouping setting for External 
        Dim mbGrouping = RasterMultiband.GetMultibandGroupingExternal(resultScenarios(0).Library)

        Dim filesCopied As Boolean = False

        For Each scenario As Scenario In resultScenarios

            ' Copy any Map Type files to a temp directory
            Dim sourceDir As String = RasterFiles.GetOutputFolderLegacy(scenario, False)
            Dim tempDir = CreateTempDir()
            CopyFiles(sourceDir, tempDir, fileFilterRegex)

            'Check to see if they're already multibanded appropriately. If so, then extracting and recombining is a waste of time
            If GetFolderMultibandGrouping(tempDir) <> mbGrouping Then
                ' Extract then to single files if appropriate
                ConvertMultibandRastersToSingles(tempDir, tempDir)
                ' Recombine them using specified Multiband Grouping
                RasterMultiband.ConvertAllSinglesToMultibandRasters(tempDir, mbGrouping)
            End If

            ' And finally, copy to the user select destination, renaming then in the process
            If CopyScenarioRasterFiles(tempDir, destFolderName, scenario, fileFilterRegex, renameExportFileFunction) Then
                filesCopied = True
            End If

            ' Clean up temp files
            Utilities.DeleteDirectoryIfExists(tempDir)

        Next

        If filesCopied Then
            Process.Start("explorer.exe", destFolderName)
        Else
            Dim sMsg As String = "No maps of the specified type found for the currently selected result scenarios. Please review your spatial output options."
            Utilities.InformationMessageBox(sMsg)
        End If

    End Sub

    Private Function CopyScenarioRasterFiles(ByVal sourceDir As String, ByVal destPath As String, ByVal scenario As Scenario, ByVal fileFilterRegex As String, ByVal renameExportFileFunction As RenameExportFileDelegate) As Boolean

        Dim filesCopied As Boolean = False

        If (Not Directory.Exists(sourceDir)) Then
            Return False
        End If

        ' Now find all the specific raster files in the source directory
        For Each filename As String In System.IO.Directory.GetFiles(sourceDir)

            Dim destFile = System.IO.Path.GetFileName(filename)
            Debug.Print(destFile)
            Dim m As Match = Regex.Match(destFile, fileFilterRegex)

            If m.Success Then

                destFile = renameExportFileFunction.Invoke(destFile)

                ' When copying over to user specified location, prepend with Scenario ID. Also sanitize, to remove any illegal characters that might have creeped in due to id to name translation
                destFile = Path.Combine(destPath, "Sc" & scenario.Id & "-" & SpatialSanitizeFileName(destFile))
                My.Computer.FileSystem.CopyFile(filename, destFile, True)

                ' Clear the ReadOnly attribute - as the source file will be R/O.
                File.SetAttributes(destFile, FileAttributes.Normal)
                filesCopied = True ' flag that we found some files that matched our file type filter

            End If

        Next

        Return filesCopied

    End Function

    Private Function GetFolderMultibandGrouping(sourcePath As String) As MultibandGrouping

        Dim files = Directory.GetFiles(sourcePath, "*.tif")
        For Each fileName In files

            fileName = Path.GetFileName(fileName)
            Dim fileFilter = String.Format("^(It([\d]*)-)*(Ts([\d]*)-)*(.*)\.tif")
            Dim m As Match = Regex.Match(fileName, fileFilter)
            If Not m.Success Or m.Groups.Count <> 6 Then
                ' We can't figure it out, so have to be pessemitic
                Return MultibandGrouping.Undefined
            Else

                Dim iterGrp = m.Groups(2)
                Dim tsGrp = m.Groups(4)
                ' If both iteration and timestep known, then we're dealing with single band
                If (iterGrp.Success) And tsGrp.Success Then
                    Return MultibandGrouping.None
                End If

                ' If neither Iteration or Timestep then All
                If Not iterGrp.Success And Not tsGrp.Success Then
                    Return MultibandGrouping.All
                End If

                ' Only iteration
                If (iterGrp.Success) And Not tsGrp.Success Then
                    Return MultibandGrouping.Timestep
                End If

                ' Only timestep
                If Not (iterGrp.Success) And tsGrp.Success Then
                    Return MultibandGrouping.Iteration
                End If

            End If

        Next

        Debug.Assert(False) ' Shouldnt get here
        Return MultibandGrouping.Undefined

    End Function

    Public Sub ConvertMultibandRastersToSingles(sourcePath As String, destPath As String)


        ' Lets extract all the indiviual bands from a multiband TIFF file
        Dim files = Directory.GetFiles(sourcePath, "*.vrt")

        For Each file In files
            Dim multbandFilename As String = file
            Dim dicBand = BuildBandDict(multbandFilename)

            For Each bandName In dicBand.Keys
                ExtractBand(destPath, multbandFilename, dicBand, bandName)
            Next

            ' Remove the source files ( vrt and tif)
            IO.File.SetAttributes(file, FileAttributes.Normal)
            IO.File.Delete(file)

            Dim tifFile = Path.ChangeExtension(file, "tif")
            IO.File.SetAttributes(tifFile, FileAttributes.Normal)
            IO.File.Delete(tifFile)

        Next


    End Sub

    Friend Function ExtractBand(destFolder As String, multibandFilename As String, dicBands As Dictionary(Of String, Integer), bandName As String) As String

        Dim bandNum As Integer?
        Dim extractFilename As String = Path.Combine(destFolder, bandName)

        If (Not Directory.Exists(Path.GetDirectoryName(extractFilename))) Then
            Directory.CreateDirectory(Path.GetDirectoryName(extractFilename))
        End If

        'TODO: TKR - Could add caching to make it faster

        If Not dicBands.ContainsKey(bandName) Then
            Return ""
        End If

        bandNum = dicBands.Item(bandName)

        Translate.GdalTranslate(multibandFilename, extractFilename, GdalOutputFormat.GTiff, GdalOutputType.CFloat64, GeoTiffCompressionType.DEFLATE, bandNum)

        Return extractFilename

    End Function

    Friend Function BuildBandDict(multibandFilename As String) As Dictionary(Of String, Integer)

        Dim vrtFilename As String = Path.ChangeExtension(multibandFilename, "vrt")

        Dim dicBand As New Dictionary(Of String, Integer)

        If Not File.Exists((vrtFilename)) Then
            Return dicBand
        Else
            Dim doc As XDocument = XDocument.Load(vrtFilename)

            Dim vrtRoot As XElement = doc.Element("VRTDataset")

            'Bands
            Dim bands = vrtRoot.Elements("VRTRasterBand")
            For Each band As XElement In bands
                Dim source As XElement = band.Element("ComplexSource")
                Dim sourceFilename As XElement = source.Element("SourceFilename")

                dicBand.Add(sourceFilename.Value, CInt(band.Attribute("band")))
            Next
        End If

        Return dicBand

    End Function

    Private Sub CopyFiles(sourceDir As String, destDir As String, fileFilterRegex As String)

        For Each filename As String In System.IO.Directory.GetFiles(sourceDir)

            Dim destFile = System.IO.Path.GetFileName(filename)
            Dim m As Match = Regex.Match(destFile, fileFilterRegex)

            If m.Success Then
                My.Computer.FileSystem.CopyFile(filename, Path.Combine(destDir, destFile), True)
            End If
        Next

    End Sub

    Private Sub DeleteDirectoryIfExists(ByVal directoryName As String)
        If Not Directory.Exists(directoryName) Then
            Return
        End If

        For Each d As String In Directory.GetDirectories(directoryName)
            DeleteDirectoryIfExists(d)
        Next

        For Each f As String In Directory.GetFiles(directoryName)
            File.SetAttributes(f, FileAttributes.Normal)
            File.Delete(f)
        Next

        Directory.Delete(directoryName)
    End Sub

    Private Function CreateTempDir() As String

        Dim rnd As Integer
        Dim folderName As String

        Do
            rnd = New System.Random().Next()
            folderName = Path.Combine(Path.GetTempPath(), "STSim_MultibandProcessing_" & rnd)

        Loop While Directory.Exists(folderName)

        Directory.CreateDirectory(folderName)

        Return folderName

    End Function

    Private Function SpatialSanitizeFileName(ByVal fileName As String) As String

        Dim invalids As Char() = System.IO.Path.GetInvalidFileNameChars()
        Return String.Join("_", fileName.Split(invalids, StringSplitOptions.RemoveEmptyEntries)).TrimEnd()

    End Function

End Module
