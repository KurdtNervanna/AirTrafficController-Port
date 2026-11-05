@echo off
rem Assemble a ready-to-run folder: dist\Air Traffic Controller\ (ATC.exe + game files + manual)
setlocal
cd /d "%~dp0"
if not exist build\ATC.exe (call build.bat || exit /b 1)
if not exist game\ATC.rsrc (echo game\ATC.rsrc is missing - see README.md & exit /b 1)
if not exist game\System.rsrc (echo game\System.rsrc is missing - see README.md & exit /b 1)
set "D=dist\Air Traffic Controller"
if exist "%D%" rmdir /s /q "%D%"
mkdir "%D%\game"
copy /y build\ATC.exe "%D%\" >nul
copy /y game\ATC.rsrc "%D%\game\" >nul
copy /y game\System.rsrc "%D%\game\" >nul
if exist "game\ATC 5.03 Manual.txt" powershell -NoProfile -ExecutionPolicy Bypass -File tools\manual.ps1 "game\ATC 5.03 Manual.txt" "%D%\Manual.txt"
copy /y README.md "%D%\README.md" >nul
echo Packaged: %D%
