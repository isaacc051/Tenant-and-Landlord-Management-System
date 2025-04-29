from django.shortcuts import render
from leases.views import get_reminders

def home(request):
    """Home page view with reminder widgets for tenants"""
    if request.user.is_authenticated and request.user.user_type == 'tenant':
        return render(request, 'home.html', get_reminders(request))
    return render(request, 'home.html') 