from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import User
from .forms import UserProfileForm
from leases.views import get_reminders
from payments.models import Payment
from leases.models import Lease

@login_required
def profile_view(request):
    """View for users to see their profile information"""
    return render(request, 'accounts/profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    """View for users to edit their profile information"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'accounts/edit_profile.html', {'form': form})

@login_required
def tenant_dashboard(request):
    """View for tenant dashboard with reminders and lease information"""
    if request.user.user_type != 'tenant':
        messages.error(request, "This page is only available to tenants.")
        return redirect('home')
    
    # Get reminder data
    reminder_data = get_reminders(request)
    
    # Get active lease
    active_lease = Lease.objects.filter(
        tenant=request.user,
        status='active'
    ).first()
    
    # Get recent payments
    recent_payments = Payment.objects.filter(
        tenant=request.user
    ).order_by('-payment_date')[:5]
    
    context = {
        **reminder_data,
        'active_lease': active_lease,
        'recent_payments': recent_payments
    }
    
    return render(request, 'accounts/tenant_dashboard.html', context)