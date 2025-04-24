@echo off
call fresh_venv\Scripts\activate.bat
python manage.py runserver
pause