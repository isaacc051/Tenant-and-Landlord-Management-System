from django import forms
from .models import Lease, LeaseDocument
from properties.models import Property

class LeaseForm(forms.ModelForm):
    class Meta:
        model = Lease
        fields = ['property', 'tenant', 'start_date', 'end_date', 'monthly_rent', 'security_deposit', 'terms_and_conditions']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'monthly_rent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Monthly rent in £'}),
            'security_deposit': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Security deposit in £'}),
            'terms_and_conditions': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'property': forms.Select(attrs={'class': 'form-select'}),
            'tenant': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'security_deposit': 'Tenancy Deposit',
            'terms_and_conditions': 'Tenancy Terms and Conditions',
        }
        help_texts = {
            'security_deposit': 'The deposit will be protected in a government-approved tenancy deposit scheme',
            'start_date': 'The date the tenancy begins',
            'end_date': 'The date the tenancy ends (for fixed-term agreements)',
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user and user.user_type == 'landlord':
            # Only show properties owned by this landlord
            self.fields['property'].queryset = Property.objects.filter(owner=user)
            
            # Only show tenant users
            from django.contrib.auth import get_user_model
            User = get_user_model()
            self.fields['tenant'].queryset = User.objects.filter(user_type='tenant')

class LeaseDocumentForm(forms.ModelForm):
    class Meta:
        model = LeaseDocument
        fields = ['document', 'title']
        widgets = {
            'document': forms.FileInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'})
        }