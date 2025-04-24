@echo off
echo Installing latest compatible Pillow version...

call fresh_venv\Scripts\activate.bat

echo Uninstalling any existing Pillow installation...
python -m pip uninstall -y pillow

echo Installing the latest compatible Pillow version...
python -m pip install --no-binary :all: pillow

echo Creating static directory if it doesn't exist...
if not exist static mkdir static

echo Creating media directory if it doesn't exist...
if not exist media mkdir media

echo Verifying installation...
python -c "import PIL; print(f'Pillow version: {PIL.__version__}')"

echo.
echo If you see a Pillow version above, the installation was successful.
echo Now run the Django server with: python manage.py runserver
pause