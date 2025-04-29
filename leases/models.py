from django.db import models
from django.utils import timezone

class Lease(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('terminated', 'Terminated'),
    )
    
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='leases')
    tenant = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='leases')
    start_date = models.DateField()
    end_date = models.DateField()
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, help_text="Monthly rent in £")
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, help_text="Security deposit in £")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    signed_by_landlord = models.BooleanField(default=False)
    signed_by_tenant = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    terms_and_conditions = models.TextField(blank=True)

    def __str__(self):
        return f"Tenancy Agreement for {self.property.title} - {self.tenant.username}"
    
    def is_fully_signed(self):
        return self.signed_by_landlord and self.signed_by_tenant
    
    def is_active(self):
        today = timezone.now().date()
        return self.status == 'active' and self.start_date <= today <= self.end_date
    
    def save(self, *args, **kwargs):
        """Override save to update property status when lease status changes"""
        is_new = self.pk is None
        old_status = None
        if not is_new:
            old_lease = Lease.objects.get(pk=self.pk)
            old_status = old_lease.status
        
        super().save(*args, **kwargs)
        
        # Update property status if lease status changed to/from active
        if is_new or old_status != self.status:
            self.property.update_status()


class LeaseDocument(models.Model):
    lease = models.ForeignKey(Lease, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to='lease_documents/')
    title = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title