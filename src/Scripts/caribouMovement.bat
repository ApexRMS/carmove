SET OSGEO4W_ROOT=C:\Program Files\QGIS Chugiak
CALL "%OSGEO4W_ROOT%\bin\o4w_env.bat"
pushd "%~dp0"
StartProcess --name=python.exe --no-error-box --args="caribouMovement.py "%1" "%2"" > ""%1".log" 2>&1
if %ERRORLEVEL% == -1073741819 (
	exit /b 0
) else (
	exit /b %ERRORLEVEL%
)
