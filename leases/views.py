from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Lease, LeaseDocument
from .forms import LeaseForm, LeaseDocumentForm

@login_required
def lease_list(request):
    """View for listing all leases - redirects to appropriate view based on user type"""
    if request.user.user_type == 'landlord':
        return redirect('leases:landlord_leases')
    elif request.user.user_type == 'tenant':
        return redirect('leases:tenant_leases')
    else:
        messages.error(request, "Invalid user type for lease management.")
        return redirect('home')

@login_required
def landlord_leases(request):
    """View for landlords to see all their leases"""
    if request.user.user_type != 'landlord':
        messages.error(request, "Only landlords can access this page.")
        return redirect('home')
    
    # Get properties owned by this landlord
    properties = request.user.properties.all()
    
    # Get all leases for these properties
    leases = Lease.objects.filter(property__in=properties).order_by('-created_at')
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter and status_filter != 'all':
        leases = leases.filter(status=status_filter)
    
    return render(request, 'leases/landlord_leases.html', {
        'leases': leases,
        'status_filter': status_filter or 'all',
        'STATUS_CHOICES': Lease.STATUS_CHOICES
    })

@login_required
def tenant_leases(request):
    """View for tenants to see all their leases"""
    if request.user.user_type != 'tenant':
        messages.error(request, "Only tenants can access this page.")
        return redirect('home')
    
    leases = Lease.objects.filter(tenant=request.user).order_by('-created_at')
    
    return render(request, 'leases/tenant_leases.html', {'leases': leases})

@login_required
def lease_detail(request, pk):
    """View for showing lease details"""
    lease = get_object_or_404(Lease, pk=pk)
    
    # Check permissions
    if not (
        (request.user.user_type == 'landlord' and lease.property.owner == request.user) or
        (request.user.user_type == 'tenant' and lease.tenant == request.user)
    ):
        messages.error(request, "You don't have permission to view this lease.")
        return redirect('leases:lease_list')
    
    return render(request, 'leases/lease_detail.html', {
        'lease': lease,
        'documents': lease.documents.all()
    })

@login_required
def lease_create(request):
    """View for landlords to create a new lease"""
    if request.user.user_type != 'landlord':
        messages.error(request, "Only landlords can create leases.")
        return redirect('leases:lease_list')
    
    if request.method == 'POST':
        form = LeaseForm(request.POST, user=request.user)
        if form.is_valid():
            lease = form.save(commit=False)
            lease.status = 'draft'
            lease.save()
            
            messages.success(request, "Lease created successfully! You can now upload documents and sign the lease.")
            return redirect('leases:lease_detail', pk=lease.pk)
    else:
        form = LeaseForm(user=request.user)
    
    return render(request, 'leases/lease_form.html', {
        'form': form,
        'action': 'Create'
    })

@login_required
def lease_edit(request, pk):
    """View for landlords to edit a lease"""
    lease = get_object_or_404(Lease, pk=pk)
    
    # Check permissions
    if request.user.user_type != 'landlord' or lease.property.owner != request.user:
        messages.error(request, "You don't have permission to edit this lease.")
        return redirect('leases:lease_list')
    
    # Only allow editing of drafts
    if lease.status != 'draft':
        messages.error(request, "You can only edit draft leases.")
        return redirect('leases:lease_detail', pk=lease.pk)
    
    if request.method == 'POST':
        form = LeaseForm(request.POST, instance=lease, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Lease updated successfully!")
            return redirect('leases:lease_detail', pk=lease.pk)
    else:
        form = LeaseForm(instance=lease, user=request.user)
    
    return render(request, 'leases/lease_form.html', {
        'form': form,
        'lease': lease,
        'action': 'Edit'
    })

@login_required
def lease_delete(request, pk):
    """View for landlords to delete a lease"""
    lease = get_object_or_404(Lease, pk=pk)
    
    # Check permissions
    if request.user.user_type != 'landlord' or lease.property.owner != request.user:
        messages.error(request, "You don't have permission to delete this lease.")
        return redirect('leases:lease_list')
    
    # Only allow deletion of drafts
    if lease.status != 'draft':
        messages.error(request, "You can only delete draft leases.")
        return redirect('leases:lease_detail', pk=lease.pk)
    
    if request.method == 'POST':
        lease.delete()
        messages.success(request, "Lease deleted successfully!")
        return redirect('leases:landlord_leases')
    
    return render(request, 'leases/lease_confirm_delete.html', {'lease': lease})

@login_required
def landlord_sign(request, pk):
    """View for landlords to sign a lease"""
    lease = get_object_or_404(Lease, pk=pk)
    
    # Check permissions
    if request.user.user_type != 'landlord' or lease.property.owner != request.user:
        messages.error(request, "You don't have permission to sign this lease.")
        return redirect('leases:lease_list')
    
    if lease.status != 'draft':
        messages.error(request, "This lease cannot be signed.")
        return redirect('leases:lease_detail', pk=lease.pk)
    
    if request.method == 'POST':
        lease.signed_by_landlord = True
        
        # If both parties have signed, activate the lease
        if lease.signed_by_tenant:
            lease.status = 'active'
        
        lease.save()
        messages.success(request, "Lease signed successfully!")
    
    return redirect('leases:lease_detail', pk=lease.pk)

@login_required
def tenant_sign(request, pk):
    """View for tenants to sign a lease"""
    lease = get_object_or_404(Lease, pk=pk)
    
    # Check permissions
    if request.user.user_type != 'tenant' or lease.tenant != request.user:
        messages.error(request, "You don't have permission to sign this lease.")
        return redirect('leases:lease_list')
    
    if lease.status != 'draft':
        messages.error(request, "This lease cannot be signed.")
        return redirect('leases:lease_detail', pk=lease.pk)
    
    if request.method == 'POST':
        lease.signed_by_tenant = True
        
        # If both parties have signed, activate the lease
        if lease.signed_by_landlord:
            lease.status = 'active'
        
        lease.save()
        messages.success(request, "Lease signed successfully!")
    
    return redirect('leases:lease_detail', pk=lease.pk)

@login_required
def add_document(request, pk):
    """View for adding documents to a lease"""
    lease = get_object_or_404(Lease, pk=pk)
    
    # Check permissions
    if request.user.user_type != 'landlord' or lease.property.owner != request.user:
        messages.error(request, "You don't have permission to add documents to this lease.")
        return redirect('leases:lease_list')
    
    if request.method == 'POST':
        form = LeaseDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.lease = lease
            document.save()
            messages.success(request, "Document added successfully!")
            return redirect('leases:lease_detail', pk=lease.pk)
    else:
        form = LeaseDocumentForm()
    
    return render(request, 'leases/lease_document_form.html', {
        'form': form,
        'lease': lease
    })