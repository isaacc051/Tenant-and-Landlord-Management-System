@echo off
echo Starting Tenant and Landlord Management System setup...

echo Activating virtual environment...
call fresh_venv\Scripts\activate.bat

echo Installing required packages...
pip install django==4.2.7
pip install pillow==10.1.0
pip install django-crispy-forms==2.0
pip install crispy-bootstrap5==0.7
pip install django-allauth==0.58.2
pip install djangorestframework==3.14.0
pip install python-dotenv==1.0.0
pip install stripe==7.3.0

echo Creating database migrations...
python manage.py makemigrations

echo Applying migrations...
python manage.py migrate

echo Creating superuser (follow the prompts)...
python manage.py createsuperuser

echo Starting development server...
python manage.py runserver

pause