@ECHO OFF
TITLE %~DP0
REM."%~dp0" == "%userprofile%\Selenium\"
IF "%~dp0" == "%userprofile%\Selenium\" (
	Echo.File is opened from folder "%userprofile%\Selenium\"
) ELSE (
	Echo.File is NOT opened from folder "%userprofile%\Selenium\" copy file into the folder
	if not exist "%userprofile%\Selenium\" (mkdir "%userprofile%\Selenium")
	copy /b/v/y "%~dpnx0" "%userprofile%\Selenium" >NUL
	Start "" "%userprofile%\Selenium\%~nx0" >NUL
	exit
)


call "%~dp001-Download-Powershell.cmd"
call "%~dp002-Download-Python-Embed.cmd"
call "%~dp003-Download_Chrome-For-Testing.cmd"
call "%~dp004-Download_Chrome-Driver.cmd"

EXIT