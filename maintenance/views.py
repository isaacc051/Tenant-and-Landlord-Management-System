from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import MaintenanceRequest, MaintenanceComment, MaintenanceImage
from .forms import MaintenanceRequestForm, MaintenanceCommentForm, MaintenanceImageForm, MaintenanceUpdateForm
from properties.models import Property
from leases.models import Lease

@login_required
def maintenance_list(request):
    """View for listing maintenance requests based on user type"""
    if request.user.user_type == 'tenant':
        # Tenants see only their own maintenance requests
        maintenance_requests = MaintenanceRequest.objects.filter(
            tenant=request.user
        ).order_by('-created_at')
        template = 'maintenance/maintenance_list.html'
    elif request.user.user_type == 'landlord':
        # Landlords see maintenance requests for properties they own
        maintenance_requests = MaintenanceRequest.objects.filter(
            property__owner=request.user
        ).order_by('-created_at')
        template = 'maintenance/landlord_maintenance_list.html'
    else:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter and status_filter != 'all':
        maintenance_requests = maintenance_requests.filter(status=status_filter)
    
    return render(request, template, {
        'maintenance_requests': maintenance_requests,
        'status_filter': status_filter or 'all',
        'STATUS_CHOICES': MaintenanceRequest.STATUS_CHOICES
    })

@login_required
def maintenance_detail(request, pk):
    """View for showing maintenance request details"""
    maintenance_request = get_object_or_404(MaintenanceRequest, pk=pk)
    
    # Check permissions - only landlord of property or tenant who created request can view
    if not (
        (request.user.user_type == 'landlord' and maintenance_request.property.owner == request.user) or
        (request.user.user_type == 'tenant' and maintenance_request.tenant == request.user)
    ):
        messages.error(request, "You don't have permission to view this maintenance request.")
        return redirect('maintenance:maintenance_list')
    
    # Handle comment form submission
    if request.method == 'POST':
        comment_form = MaintenanceCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.request = maintenance_request
            comment.user = request.user
            comment.save()
            messages.success(request, "Comment added successfully.")
            return redirect('maintenance:maintenance_detail', pk=pk)
    else:
        comment_form = MaintenanceCommentForm()
    
    # Get all comments and images for this request
    comments = maintenance_request.comments.order_by('created_at')
    images = maintenance_request.images.all()
    
    # Create update form for landlords
    update_form = None
    if request.user.user_type == 'landlord':
        update_form = MaintenanceUpdateForm(instance=maintenance_request)
    
    return render(request, 'maintenance/maintenance_detail.html', {
        'maintenance_request': maintenance_request,
        'comments': comments,
        'images': images,
        'comment_form': comment_form,
        'update_form': update_form,
    })

@login_required
def maintenance_create(request):
    """View for tenants to create a maintenance request"""
    if request.user.user_type != 'tenant':
        messages.error(request, "Only tenants can create maintenance requests.")
        return redirect('maintenance:maintenance_list')
    
    # Get all properties the tenant is leasing
    leases = Lease.objects.filter(
        tenant=request.user,
        status='active',
        end_date__gte=timezone.now().date()
    ).select_related('property')
    
    if not leases.exists():
        messages.error(request, "You don't have any active leases to create maintenance requests for.")
        return redirect('maintenance:maintenance_list')
    
    if request.method == 'POST':
        form = MaintenanceRequestForm(request.POST)
        property_id = request.POST.get('property')
        
        try:
            property_obj = Property.objects.get(id=property_id)
            # Verify tenant has a lease for this property
            if not leases.filter(property=property_obj).exists():
                messages.error(request, "You don't have an active lease for this property.")
                return redirect('maintenance:maintenance_list')
            
            if form.is_valid():
                maintenance_request = form.save(commit=False)
                maintenance_request.property = property_obj
                maintenance_request.tenant = request.user
                maintenance_request.save()
                
                messages.success(request, "Maintenance request created successfully!")
                return redirect('maintenance:maintenance_detail', pk=maintenance_request.pk)
        except Property.DoesNotExist:
            messages.error(request, "Invalid property selected.")
    else:
        form = MaintenanceRequestForm()
    
    return render(request, 'maintenance/maintenance_form.html', {
        'form': form,
        'leases': leases,
        'action': 'Create'
    })

@login_required
def maintenance_update(request, pk):
    """View for landlords to update the status of a maintenance request"""
    maintenance_request = get_object_or_404(MaintenanceRequest, pk=pk)
    
    # Check permissions - only landlord of property can update
    if request.user.user_type != 'landlord' or maintenance_request.property.owner != request.user:
        messages.error(request, "You don't have permission to update this maintenance request.")
        return redirect('maintenance:maintenance_list')
    
    if request.method == 'POST':
        form = MaintenanceUpdateForm(request.POST, instance=maintenance_request)
        if form.is_valid():
            maintenance_request = form.save(commit=False)
            
            # If status changed to completed, set completed_at
            if maintenance_request.status == 'completed' and not maintenance_request.completed_at:
                maintenance_request.completed_at = timezone.now()
            
            maintenance_request.save()
            
            # Add a system comment about the status change
            old_status = dict(MaintenanceRequest.STATUS_CHOICES).get(maintenance_request.status, maintenance_request.status)
            comment = f"Status updated to {old_status}"
            if maintenance_request.assigned_to:
                comment += f" and assigned to {maintenance_request.assigned_to}"
                
            MaintenanceComment.objects.create(
                request=maintenance_request,
                user=request.user,
                comment=comment
            )
            
            messages.success(request, "Maintenance request updated successfully!")
            return redirect('maintenance:maintenance_detail', pk=pk)
    else:
        form = MaintenanceUpdateForm(instance=maintenance_request)
    
    return render(request, 'maintenance/maintenance_update_form.html', {
        'form': form,
        'maintenance_request': maintenance_request
    })

@login_required
def add_maintenance_image(request, pk):
    """View for adding images to a maintenance request"""
    maintenance_request = get_object_or_404(MaintenanceRequest, pk=pk)
    
    # Check permissions - only tenant who created request or landlord of property can add images
    if not (
        (request.user.user_type == 'tenant' and maintenance_request.tenant == request.user) or
        (request.user.user_type == 'landlord' and maintenance_request.property.owner == request.user)
    ):
        messages.error(request, "You don't have permission to add images to this maintenance request.")
        return redirect('maintenance:maintenance_list')
    
    if request.method == 'POST':
        form = MaintenanceImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.request = maintenance_request
            image.save()
            
            messages.success(request, "Image added successfully!")
            return redirect('maintenance:maintenance_detail', pk=pk)
    else:
        form = MaintenanceImageForm()
    
    return render(request, 'maintenance/maintenance_image_form.html', {
        'form': form,
        'maintenance_request': maintenance_request
    })