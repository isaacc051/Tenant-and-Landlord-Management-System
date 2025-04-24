from django.db import models
from django.utils import timezone
from django.urls import reverse
import uuid

class Payment(models.Model):
    PAYMENT_TYPE_CHOICES = (
        ('rent', 'Rent'),
        ('deposit', 'Security Deposit'),
        ('late_fee', 'Late Fee'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    
    PAYMENT_METHOD_CHOICES = (
        ('stripe', 'Stripe Payment'),
    )
    
    tenant = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='payments')
    lease = models.ForeignKey('leases.Lease', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPE_CHOICES)
    payment_method = models.CharField(max_length=15, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    receipt_issued = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.payment_type} payment by {self.tenant.username} for {self.lease.property.title}"
    
    def is_late(self):
        return self.status == 'pending' and timezone.now().date() > self.due_date
    
    def generate_receipt(self):
        """Generate a receipt for this payment if it doesn't exist"""
        if not self.receipt_issued and self.status == 'completed':
            receipt = Receipt.objects.create(
                payment=self,
                receipt_number=f"RCP-{uuid.uuid4().hex[:8].upper()}",
                issued_date=timezone.now()
            )
            self.receipt_issued = True
            self.save()
            return receipt
        return Receipt.objects.filter(payment=self).first()
    
    def get_receipt_url(self):
        """Return the URL for viewing this payment's receipt"""
        return reverse('payment_receipt', args=[str(self.id)])
    
    def get_payment_period(self):
        """Return a formatted string representing the payment period"""
        if self.payment_type == 'rent':
            month = self.due_date.strftime('%B %Y')
            return f"Rent for {month}"
        elif self.payment_type == 'deposit':
            return "Security Deposit"
        else:
            return self.get_payment_type_display()


class Receipt(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='receipt')
    receipt_number = models.CharField(max_length=20, unique=True)
    issued_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Receipt {self.receipt_number} for {self.payment}"


class PaymentReminder(models.Model):
    lease = models.ForeignKey('leases.Lease', on_delete=models.CASCADE, related_name='payment_reminders')
    due_date = models.DateField()
    reminder_date = models.DateField()
    sent = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Payment reminder for {self.lease.tenant.username} due {self.due_date}"