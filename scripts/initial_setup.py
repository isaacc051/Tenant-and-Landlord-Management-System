import os
import sys
import subprocess
from pathlib import Path

def create_directory_structure():
    """Create the basic directory structure for the project."""
    # Base directories
    directories = [
        'media',
        'media/profile_pictures',
        'media/property_images',
        'media/property_documents',
        'media/lease_documents',
        'static',
        'static/css',
        'static/js',
        'static/images',
        'templates',
        'templates/accounts',
        'templates/properties',
        'templates/leases',
        'templates/maintenance',
        'templates/payments',
        'templates/communications',
    ]
    
    for directory in directories:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), directory)
        os.makedirs(path, exist_ok=True)
        print(f"Created directory: {path}")

def create_forms_files():
    """Create basic forms.py files for all apps."""
    apps = ['accounts', 'properties', 'leases', 'maintenance', 'payments', 'communications']
    
    for app in apps:
        form_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), app, 'forms.py')
        with open(form_path, 'w') as f:
            f.write(f"""from django import forms
from .models import *

# Create your forms here
""")
        print(f"Created forms.py for {app}")

def create_views_files():
    """Create basic views.py files for all apps."""
    apps = ['accounts', 'properties', 'leases', 'maintenance', 'payments', 'communications']
    
    for app in apps:
        views_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), app, 'views.py')
        with open(views_path, 'w') as f:
            f.write(f"""from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *

# Create your views here
""")
        print(f"Created views.py for {app}")

def create_urls_files():
    """Create basic urls.py files for all apps."""
    apps = ['accounts', 'properties', 'leases', 'maintenance', 'payments', 'communications']
    
    for app in apps:
        urls_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), app, 'urls.py')
        with open(urls_path, 'w') as f:
            f.write(f"""from django.urls import path
from . import views

app_name = '{app}'

urlpatterns = [
    # Add your URL patterns here
]
""")
        print(f"Created urls.py for {app}")

if __name__ == "__main__":
    print("Setting up initial project structure...")
    create_directory_structure()
    create_forms_files()
    create_views_files()
    create_urls_files()
    print("Initial setup complete!")
