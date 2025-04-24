from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import User
from .forms import UserProfileForm

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