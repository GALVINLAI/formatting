@echo off
setlocal
cd /d "%~dp0"

python -m PyInstaller --clean --onefile --noconsole --name formatting --icon=icon.ico --distpath .\ --exclude-module pkg_resources main.py

if errorlevel 1 (
    echo.
    echo Build failed.
    exit /b 1
)

echo.
echo Build completed: "%CD%\formatting.exe"
