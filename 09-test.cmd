@ECHO OFF
TITLE %~DP0
REM."%~dp0" == "%userprofile%\Selenium\"
IF "%~dp0" == "%userprofile%\Selenium\" (
	Echo.File is opened from folder "%userprofile%\Selenium\"
) ELSE (
	Echo.File is NOT opened from folder "%userprofile%\Selenium\" copy file into the folder
	if not exist "%userprofile%\Selenium\" (mkdir "%userprofile%\Selenium")
	copy /b/v/y "%~dpnx0" "%userprofile%\Selenium" >NUL
	copy /b/v/y "%~dpn0.ps1" "%userprofile%\Selenium" >NUL
	Start "" "%userprofile%\Selenium\%~nx0" >NUL
	exit
)

pushd "%~dp0\"
cd "%~dp0\"

SET PWSH="%~dp0powershell\pwsh.exe"

::if not exist "%userprofile%\Selenium\chromedriver\chromedriver-win64\chromedriver.exe" (
	%PWSH% -NoProfile -ExecutionPolicy Bypass -Command "& '%~dpn0.ps1'"
::)
::pause
EXIT