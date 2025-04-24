@echo off
echo ======================================================
echo Property Management System - Easy Setup Script
echo ======================================================
echo.

:: Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.8 or newer from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

:: Check if virtual environment exists
if not exist "fresh_venv\Scripts\activate.bat" (
    echo Creating new virtual environment...
    python -m venv fresh_venv
)

echo Activating virtual environment...
call fresh_venv\Scripts\activate.bat

echo.
echo Installing all project dependencies...
pip install -r requirements.txt

echo.
echo Installing Pillow (image processing library)...
pip install --no-cache-dir pillow

echo.
echo Creating static directory if it doesn't exist...
if not exist "static" mkdir static

echo.
echo Creating database migrations...
python manage.py makemigrations

echo.
echo Applying migrations...
python manage.py migrate

echo.
echo ======================================================
echo Setup complete! Starting development server...
echo.
echo Access the application at: http://127.0.0.1:8000/
echo Press Ctrl+C to stop the server when done
echo ======================================================
echo.

python manage.py runserver

pause