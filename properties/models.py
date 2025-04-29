from django.db import models
from django.utils import timezone

class Property(models.Model):
    PROPERTY_TYPE_CHOICES = (
        ('flat', 'Flat'),
        ('house', 'House'),
        ('terraced', 'Terraced House'),
        ('semi_detached', 'Semi-Detached House'),
        ('detached', 'Detached House'),
        ('bungalow', 'Bungalow'),
        ('cottage', 'Cottage'),
        ('studio', 'Studio'),
        ('maisonette', 'Maisonette'),
        ('commercial', 'Commercial'),
    )
    
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance'),
    )
    
    owner = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=100)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    address = models.CharField(max_length=255)
    town_city = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)
    description = models.TextField()
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, help_text="Monthly rent in £")
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1)
    square_meters = models.PositiveIntegerField(help_text="Property size in square meters")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.address}"

    def square_feet(self):
        return int(self.square_meters * 10.764)
    
    @property
    def available(self):
        """Compute availability based on status"""
        return self.status == 'available'
    
    def update_status(self):
        """Update property status based on active leases"""
        from leases.models import Lease
        has_active_lease = Lease.objects.filter(
            property=self,
            status='active',
            start_date__lte=timezone.now().date(),
            end_date__gte=timezone.now().date()
        ).exists()
        
        if has_active_lease:
            self.status = 'occupied'
        else:
            self.status = 'available'
        self.save()


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.FileField(upload_to='property_images/')
    caption = models.CharField(max_length=100, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.property.title}"


class PropertyDocument(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to='property_documents/')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class PropertyApplication(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='property_applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    move_in_date = models.DateField()
    message = models.TextField(help_text="Message to the landlord")
    credit_check_consent = models.BooleanField(default=False, help_text="Consent to perform credit check")
    income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, 
                               help_text="Monthly income in £")
    has_pets = models.BooleanField(default=False)
    pet_description = models.TextField(blank=True)
    employment_status = models.CharField(max_length=50, blank=True, help_text="Current employment status")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Application for {self.property.title} by {self.applicant.username}"
