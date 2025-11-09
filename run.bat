@echo off
REM Convenience script to run the application on Windows

echo Website Search ^& Chatbox Finder
echo.

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Check if query provided
if "%~1"=="" (
    echo Usage: run.bat "your search query"
    echo.
    echo Examples:
    echo   run.bat "restaurants in New York"
    echo   run.bat "law firms in California"
    echo.
    python main.py
) else (
    python main.py %*
)
