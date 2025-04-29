from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import Property, PropertyImage, PropertyDocument, PropertyApplication
from .forms import PropertyForm, PropertyImageForm, PropertyDocumentForm, PropertySearchForm, PropertyApplicationForm
from django.template.loader import get_template
from django.conf import settings

def property_list(request):
    """View for listing all available properties"""
    properties = Property.objects.all()
    
    # For tenants, only show available properties
    if request.user.is_authenticated and request.user.user_type == 'tenant':
        # First update all property statuses
        for property in properties:
            property.update_status()
        # Then filter for available properties
        properties = properties.filter(status='available')
    
    # Get comparison list from session
    compare_properties = request.session.get('compare_properties', [])
    
    return render(request, 'properties/property_list.html', {
        'properties': properties,
        'compare_properties': compare_properties
    })

@login_required
def property_create(request):
    """View for landlords to create a new property"""
    if request.user.user_type != 'landlord':
        messages.error(request, "Only landlords can create properties.")
        return redirect('properties:property_list')
    
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            property = form.save(commit=False)
            property.owner = request.user
            property.save()
            messages.success(request, "Property created successfully!")
            return redirect('properties:property_detail', pk=property.pk)
    else:
        form = PropertyForm()
    
    return render(request, 'properties/property_form.html', {'form': form, 'action': 'Create'})

def property_detail(request, pk):
    """View for showing property details"""
    property = get_object_or_404(Property, pk=pk)
    context = {
        'property': property,
        'images': property.images.all(),
        'documents': property.documents.all() if request.user == property.owner else None,
    }
    return render(request, 'properties/property_detail.html', context)

@login_required
def property_update(request, pk):
    """View for landlords to update their property"""
    property = get_object_or_404(Property, pk=pk)
    
    # Check if the user is the owner
    if request.user != property.owner:
        messages.error(request, "You don't have permission to edit this property.")
        return redirect('properties:property_detail', pk=property.pk)
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property)
        if form.is_valid():
            form.save()
            messages.success(request, "Property updated successfully!")
            return redirect('properties:property_detail', pk=property.pk)
    else:
        form = PropertyForm(instance=property)
    
    return render(request, 'properties/property_form.html', {'form': form, 'action': 'Update'})

@login_required
def property_delete(request, pk):
    """View for landlords to delete their property"""
    property = get_object_or_404(Property, pk=pk)
    
    # Check if the user is the owner
    if request.user != property.owner:
        messages.error(request, "You don't have permission to delete this property.")
        return redirect('properties:property_detail', pk=property.pk)
    
    if request.method == 'POST':
        property.delete()
        messages.success(request, "Property deleted successfully!")
        return redirect('properties:landlord_properties')
    
    return render(request, 'properties/property_confirm_delete.html', {'property': property})

@login_required
def landlord_properties(request):
    """View for landlords to see all their properties"""
    if request.user.user_type != 'landlord':
        messages.error(request, "Only landlords can access this page.")
        return redirect('home')
    
    properties = Property.objects.filter(owner=request.user)
    return render(request, 'properties/landlord_properties.html', {'properties': properties})

@login_required
def add_property_image(request, property_id):
    """View for landlords to add images to their property"""
    property = get_object_or_404(Property, pk=property_id)
    
    # Check if the user is the owner
    if request.user != property.owner:
        messages.error(request, "You don't have permission to add images to this property.")
        return redirect('properties:property_detail', pk=property.pk)
    
    if request.method == 'POST':
        form = PropertyImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.property = property
            image.save()
            messages.success(request, "Image added successfully!")
            return redirect('properties:property_detail', pk=property.pk)
    else:
        form = PropertyImageForm()
    
    # Debug print statements
    print("Template directories:", settings.TEMPLATES[0]['DIRS'])
    print("Looking for template at:", 'properties/property_image_form.html')
    try:
        template = get_template('properties/property_image_form.html')
        print("Template found at:", template.origin.name)
    except Exception as e:
        print("Template loading error:", str(e))
    
    return render(request, 'properties/property_image_form.html', {'form': form, 'property': property})

@login_required
def add_property_document(request, property_id):
    """View for landlords to add documents to their property"""
    property = get_object_or_404(Property, pk=property_id)
    
    # Check if the user is the owner
    if request.user != property.owner:
        messages.error(request, "You don't have permission to add documents to this property.")
        return redirect('properties:property_detail', pk=property.pk)
    
    if request.method == 'POST':
        form = PropertyDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.property = property
            document.save()
            messages.success(request, "Document added successfully!")
            return redirect('properties:property_detail', pk=property.pk)
    else:
        form = PropertyDocumentForm()
    
    return render(request, 'properties/property_document_form.html', {'form': form, 'property': property})

def property_search(request):
    """View for searching properties based on user preferences"""
    properties = Property.objects.all()
    
    # For tenants, only show available properties
    if request.user.is_authenticated and request.user.user_type == 'tenant':
        # First update all property statuses
        for property in properties:
            property.update_status()
        # Then filter for available properties
        properties = properties.filter(status='available')
    
    form = PropertySearchForm(request.GET)
    
    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        bedrooms = form.cleaned_data.get('bedrooms')
        bathrooms = form.cleaned_data.get('bathrooms')
        property_type = form.cleaned_data.get('property_type')
        
        if search_query:
            properties = properties.filter(
                Q(title__icontains=search_query) | 
                Q(description__icontains=search_query) | 
                Q(address__icontains=search_query) |
                Q(town_city__icontains=search_query) |
                Q(county__icontains=search_query) |
                Q(postcode__icontains=search_query)
            )
        
        if min_price:
            properties = properties.filter(monthly_rent__gte=min_price)
        
        if max_price:
            properties = properties.filter(monthly_rent__lte=max_price)
        
        if bedrooms:
            properties = properties.filter(bedrooms=bedrooms)
        
        if bathrooms:
            properties = properties.filter(bathrooms=bathrooms)
        
        if property_type:
            properties = properties.filter(property_type=property_type)
    
    return render(request, 'properties/property_search.html', {'properties': properties, 'form': form})

@login_required
def apply_for_property(request, property_id):
    """View for tenants to apply for a property"""
    property = get_object_or_404(Property, pk=property_id)
    
    # Check if property is available
    if not property.available:
        messages.error(request, "This property is no longer available for applications.")
        return redirect('properties:property_detail', pk=property.pk)
    
    # Check if user is a tenant
    if request.user.user_type != 'tenant':
        messages.error(request, "Only tenants can apply for properties.")
        return redirect('properties:property_detail', pk=property.pk)
    
    # Check if user has already applied for this property
    existing_application = PropertyApplication.objects.filter(
        property=property,
        applicant=request.user
    ).exists()
    
    if existing_application:
        messages.warning(request, "You have already applied for this property.")
        return redirect('properties:tenant_applications')
    
    if request.method == 'POST':
        form = PropertyApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.property = property
            application.applicant = request.user
            application.save()
            messages.success(request, "Your application has been submitted successfully!")
            return redirect('properties:tenant_applications')
    else:
        form = PropertyApplicationForm()
    
    return render(request, 'properties/property_application_form.html', {
        'form': form,
        'property': property
    })

@login_required
def tenant_applications(request):
    """View for tenants to see all their property applications"""
    if request.user.user_type != 'tenant':
        messages.error(request, "This page is only available to tenants.")
        return redirect('home')
    
    applications = PropertyApplication.objects.filter(applicant=request.user)
    return render(request, 'properties/tenant_applications.html', {'applications': applications})

@login_required
def landlord_applications(request):
    """View for landlords to see applications for their properties"""
    if request.user.user_type != 'landlord':
        messages.error(request, "This page is only available to landlords.")
        return redirect('home')
    
    # Get all applications for the landlord's properties
    applications = PropertyApplication.objects.filter(property__owner=request.user)
    pending_count = applications.filter(status='pending').count()
    approved_count = applications.filter(status='approved').count()
    rejected_count = applications.filter(status='rejected').count()
    return render(request, 'properties/landlord_applications.html', {
        'applications': applications,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
    })

@login_required
def application_detail(request, application_id):
    """View for viewing application details"""
    application = get_object_or_404(PropertyApplication, pk=application_id)
    
    # Check if user has permission to view this application
    if request.user != application.property.owner and request.user != application.applicant:
        messages.error(request, "You don't have permission to view this application.")
        return redirect('home')
    
    return render(request, 'properties/application_detail.html', {'application': application})

@login_required
def update_application_status(request, application_id, status):
    """View for landlords to update application status"""
    application = get_object_or_404(PropertyApplication, pk=application_id)
    
    # Check if user is the property owner
    if request.user != application.property.owner:
        messages.error(request, "Only the property owner can update application status.")
        return redirect('home')
    
    # Validate status
    if status not in ['approved', 'rejected']:
        messages.error(request, "Invalid status.")
        return redirect('properties:application_detail', application_id=application.pk)
    
    # Update status
    application.status = status
    application.save()
    
    # If application is approved, create a lease for the tenant
    if status == 'approved':
        messages.success(request, f"Application approved. You can now create a lease for {application.applicant.get_full_name()}.")
        return redirect('leases:lease_create', property_id=application.property.pk, tenant_id=application.applicant.pk)
    else:
        messages.success(request, "Application status updated successfully.")
        return redirect('properties:application_detail', application_id=application.pk)

def toggle_compare(request):
    """AJAX view to add/remove a property from comparison list"""
    if request.method == 'GET' and 'property_id' in request.GET:
        property_id = request.GET.get('property_id')
        add_to_compare = request.GET.get('add') == '1'
        
        # Initialize comparison list if it doesn't exist
        if 'compare_properties' not in request.session:
            request.session['compare_properties'] = []
        
        compare_list = request.session['compare_properties']
        
        # Add or remove property from comparison list
        if add_to_compare:
            if property_id not in compare_list:
                # Limit to maximum 4 properties for comparison
                if len(compare_list) >= 4:
                    return JsonResponse({
                        'success': False,
                        'error': 'You can compare a maximum of 4 properties at once.'
                    })
                compare_list.append(property_id)
        else:
            if property_id in compare_list:
                compare_list.remove(property_id)
        
        # Save updated list back to session
        request.session['compare_properties'] = compare_list
        request.session.modified = True
        
        return JsonResponse({'success': True, 'count': len(compare_list)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def clear_compare(request):
    """View to clear the comparison list"""
    if 'compare_properties' in request.session:
        request.session['compare_properties'] = []
        request.session.modified = True
    
    return redirect('properties:property_list')

def property_compare(request):
    """View for comparing selected properties"""
    compare_ids = request.session.get('compare_properties', [])
    
    if not compare_ids:
        messages.warning(request, "No properties selected for comparison.")
        return redirect('properties:property_list')
    
    # Get properties by ID
    properties = list(Property.objects.filter(id__in=compare_ids))
    
    # Sort properties to match the order in the session
    properties.sort(key=lambda p: compare_ids.index(str(p.id)))
    
    return render(request, 'properties/property_compare.html', {'properties': properties})