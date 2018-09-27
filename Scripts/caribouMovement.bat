SET OSGEO4W_ROOT=C:\Program Files\QGIS Chugiak
CALL "%OSGEO4W_ROOT%\bin\o4w_env.bat"

REM Use %~dp0 to get batch file directory
cd /d %~dp0
REM To trap Standard error, in the same directory as the input file resides.
set OP_PATH=%~dp0
StartProcess --name=python.exe --no-error-box --args="caribouMovement.py "%1" "%2"" > "%OP_PATH%caribouMovement.log" 2>&1
rem python caribouMovement.py %1 %2
if %ERRORLEVEL% == -1073741819 (
	exit /b 0
) else (
	exit /b %ERRORLEVEL%
)
rem exit /b %ERRORLEVEL%
