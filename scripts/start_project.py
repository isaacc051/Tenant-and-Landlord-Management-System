import os
import subprocess
import sys
import shutil
from pathlib import Path

# Define base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def create_virtual_environment():
    print("Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("Virtual environment created successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual environment: {e}")
        return False

def install_requirements():
    print("Installing required packages...")
    # Create requirements.txt if it doesn't exist
    requirements_file = os.path.join(BASE_DIR, "requirements.txt")
    if not os.path.exists(requirements_file):
        with open(requirements_file, "w") as f:
            f.write("""django==4.2.7
pillow==10.1.0
django-crispy-forms==2.0
crispy-bootstrap5==0.7
django-allauth==0.58.2
djangorestframework==3.14.0
python-dotenv==1.0.0
stripe==7.3.0
""")
    
    # Run pip install directly
    try:
        if os.name == 'nt':  # Windows
            venv_python = os.path.join(BASE_DIR, "venv", "Scripts", "python.exe")
        else:  # Unix/macOS
            venv_python = os.path.join(BASE_DIR, "venv", "bin", "python")
            
        subprocess.run([venv_python, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("Required packages installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {e}")
        return False

def create_django_project():
    print("Creating Django project...")
    try:
        if os.name == 'nt':  # Windows
            django_admin = os.path.join(BASE_DIR, "venv", "Scripts", "django-admin.exe")
        else:  # Unix/macOS
            django_admin = os.path.join(BASE_DIR, "venv", "bin", "django-admin")
            
        subprocess.run([django_admin, "startproject", "property_management", "."], check=True)
        print("Django project created successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error creating Django project: {e}")
        return False

def create_django_apps():
    print("Creating Django apps...")
    apps = ["accounts", "properties", "leases", "maintenance", "payments", "communications"]
    success = True
    
    for app in apps:
        try:
            if os.name == 'nt':  # Windows
                manage_py = os.path.join(BASE_DIR, "venv", "Scripts", "python.exe")
            else:  # Unix/macOS
                manage_py = os.path.join(BASE_DIR, "venv", "bin", "python")
                
            subprocess.run([manage_py, "manage.py", "startapp", app], check=True)
            print(f"App '{app}' created successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error creating app '{app}': {e}")
            success = False
    
    return success

def create_directory_structure():
    print("Creating directory structure...")
    directories = [
        'templates',
        'templates/accounts',
        'templates/properties',
        'templates/leases',
        'templates/maintenance',
        'templates/payments',
        'templates/communications',
        'static',
        'static/css',
        'static/js',
        'static/images',
        'media',
        'media/property_images',
        'media/profile_pictures',
        'media/documents',
    ]
    
    # Create directories directly
    for directory in directories:
        dir_path = os.path.join(BASE_DIR, directory)
        os.makedirs(dir_path, exist_ok=True)
        print(f"Directory '{directory}' created.")
    
    return True

def create_template_files():
    print("Creating template files...")
    
    # Base template
    base_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Tenant and Landlord Management System{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="/">Property Management</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/properties/">Properties</a>
                    </li>
                </ul>
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link" href="/accounts/login/">Login</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/accounts/signup/">Register</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        {% block content %}{% endblock %}
    </div>

    <footer class="mt-5 py-3 bg-light text-center">
        <div class="container">
            <p class="mb-0">&copy; 2023 Tenant and Landlord Management System</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
"""
    
    # Home template
    home_template = """{% extends 'base.html' %}

{% block title %}Home - Tenant and Landlord Management System{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-12 text-center mb-4">
        <h1 class="display-4">Welcome to the Tenant and Landlord Management System</h1>
        <p class="lead">A comprehensive platform to manage rental properties efficiently</p>
    </div>
</div>

<div class="row mt-4">
    <div class="col-md-4 mb-4">
        <div class="card h-100">
            <div class="card-body">
                <h5 class="card-title">Property Management</h5>
                <p class="card-text">Easily manage and showcase your rental properties with detailed information and images.</p>
                <a href="/properties/" class="btn btn-primary">View Properties</a>
            </div>
        </div>
    </div>
    <div class="col-md-4 mb-4">
        <div class="card h-100">
            <div class="card-body">
                <h5 class="card-title">Lease Management</h5>
                <p class="card-text">Generate and manage lease agreements with digital signatures and automatic reminders.</p>
                <a href="/accounts/login/" class="btn btn-primary">Login to Access</a>
            </div>
        </div>
    </div>
    <div class="col-md-4 mb-4">
        <div class="card h-100">
            <div class="card-body">
                <h5 class="card-title">Maintenance Requests</h5>
                <p class="card-text">Submit and track maintenance requests, assign tasks to service providers.</p>
                <a href="/accounts/login/" class="btn btn-primary">Login to Access</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""
    
    # Write files
    with open(os.path.join(BASE_DIR, 'templates', 'base.html'), 'w') as f:
        f.write(base_template)
    print("Created base.html")
    
    with open(os.path.join(BASE_DIR, 'templates', 'home.html'), 'w') as f:
        f.write(home_template)
    print("Created home.html")
    
    return True

def create_custom_user_model():
    print("Creating custom user model...")
    
    # User model
    user_model = """from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('landlord', 'Landlord'),
        ('tenant', 'Tenant'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
"""
    
    # User admin
    user_admin = """from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'first_name', 'last_name', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone_number', 'profile_picture')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone_number', 'profile_picture')}),
    )

admin.site.register(User, CustomUserAdmin)
"""
    
    # Write files
    accounts_dir = os.path.join(BASE_DIR, 'accounts')
    if not os.path.exists(accounts_dir):
        os.makedirs(accounts_dir)
    
    with open(os.path.join(accounts_dir, 'models.py'), 'w') as f:
        f.write(user_model)
    print("Created accounts/models.py")
    
    with open(os.path.join(accounts_dir, 'admin.py'), 'w') as f:
        f.write(user_admin)
    print("Created accounts/admin.py")
    
    return True

def update_settings():
    print("Updating settings.py...")
    
    settings_file = os.path.join(BASE_DIR, 'property_management', 'settings.py')
    if not os.path.exists(settings_file):
        print("Error: settings.py not found. Make sure the Django project is created first.")
        return False
    
    settings_content = """\"\"\"
Django settings for property_management project.
\"\"\"

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-your-secret-key-here'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    # Third-party apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'crispy_forms',
    'crispy_bootstrap5',
    'rest_framework',
    
    # Local apps
    'accounts',
    'properties',
    'leases',
    'maintenance',
    'payments',
    'communications',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'property_management.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'property_management.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Authentication settings
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Email settings (for development)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
"""
    
    with open(settings_file, 'w') as f:
        f.write(settings_content)
    print("Updated settings.py")
    
    return True

def update_urls():
    print("Updating urls.py...")
    
    urls_file = os.path.join(BASE_DIR, 'property_management', 'urls.py')
    if not os.path.exists(urls_file):
        print("Error: urls.py not found. Make sure the Django project is created first.")
        return False
    
    urls_content = """from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    # These will be implemented later as you develop each app
    # path('properties/', include('properties.urls')),
    # path('leases/', include('leases.urls')),
    # path('maintenance/', include('maintenance.urls')),
    # path('payments/', include('payments.urls')),
    # path('communications/', include('communications.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""
    
    with open(urls_file, 'w') as f:
        f.write(urls_content)
    print("Updated urls.py")
    
    return True

def migrate_database():
    print("Migrating database...")
    try:
        if os.name == 'nt':  # Windows
            python_exe = os.path.join(BASE_DIR, "venv", "Scripts", "python.exe")
        else:  # Unix/macOS
            python_exe = os.path.join(BASE_DIR, "venv", "bin", "python")
            
        subprocess.run([python_exe, "manage.py", "makemigrations", "accounts"], check=True)
        subprocess.run([python_exe, "manage.py", "migrate"], check=True)
        print("Database migrations completed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error migrating database: {e}")
        return False

def setup_project():
    print("Setting up Tenant and Landlord Management System...")
    
    # Step 1: Create virtual environment
    if not create_virtual_environment():
        return False
    
    # Step 2: Install requirements
    if not install_requirements():
        return False
    
    # Step 3: Create Django project
    if not create_django_project():
        return False
    
    # Step 4: Create Django apps
    if not create_django_apps():
        return False
    
    # Step 5: Create directories
    if not create_directory_structure():
        return False
    
    # Step 6: Create custom user model
    if not create_custom_user_model():
        return False
    
    # Step 7: Update settings.py
    if not update_settings():
        return False
    
    # Step 8: Update urls.py
    if not update_urls():
        return False
    
    # Step 9: Create templates
    if not create_template_files():
        return False
    
    # Step 10: Run migrations
    if not migrate_database():
        return False
    
    print("\nSetup complete!")
    print("To run the server: python manage.py runserver")
    print("To create a superuser: python manage.py createsuperuser")
    
    return True

if __name__ == "__main__":
    print("This script will directly set up your Django project.")
    print("Do you want to continue? (y/n)")
    choice = input().lower()
    
    if choice == 'y':
        setup_project()
    else:
        print("Setup cancelled.")
