from django import forms
from .models import Property, PropertyImage, PropertyDocument, PropertyApplication
import datetime
import re

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'property_type', 'address', 'town_city', 'county', 'postcode',
            'description', 'monthly_rent', 'bedrooms', 'bathrooms', 'square_meters', 'available'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'postcode': forms.TextInput(attrs={'placeholder': 'e.g., AB12 3CD'}),
            'square_meters': forms.NumberInput(attrs={'placeholder': 'Size in square meters'}),
        }
    
    def clean_postcode(self):
        postcode = self.cleaned_data.get('postcode')
        # UK postcode validation (basic pattern check)
        if postcode and not re.match(r'^[A-Z]{1,2}[0-9][A-Z0-9]? ?[0-9][A-Z]{2}$', postcode.upper()):
            raise forms.ValidationError("Please enter a valid UK postcode (e.g. AB12 3CD)")
        return postcode.upper() if postcode else postcode

class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image', 'caption']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'caption': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PropertyDocumentForm(forms.ModelForm):
    class Meta:
        model = PropertyDocument
        fields = ['document', 'title', 'description']
        widgets = {
            'document': forms.FileInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class PropertySearchForm(forms.Form):
    search_query = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Search properties...'}))
    min_price = forms.DecimalField(required=False, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Min Price (£)'}))
    max_price = forms.DecimalField(required=False, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Max Price (£)'}))
    bedrooms = forms.IntegerField(required=False, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Bedrooms'}))
    bathrooms = forms.DecimalField(required=False, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Bathrooms'}))
    
    PROPERTY_TYPE_CHOICES = [('', 'All Types')] + list(Property.PROPERTY_TYPE_CHOICES)
    property_type = forms.ChoiceField(
        choices=PROPERTY_TYPE_CHOICES, 
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class PropertyApplicationForm(forms.ModelForm):
    move_in_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'min': datetime.date.today().isoformat()}),
        help_text="When would you like to move in?"
    )
    
    class Meta:
        model = PropertyApplication
        fields = [
            'move_in_date', 'message', 'credit_check_consent', 'income', 'has_pets', 'pet_description', 'employment_status'
        ]
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 
                                          'placeholder': 'Introduce yourself to the landlord'}),
            'credit_check_consent': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'income': forms.NumberInput(attrs={'class': 'form-control', 
                                           'placeholder': 'Optional: Your monthly income (£)'}),
            'has_pets': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pet_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 
                                                  'placeholder': 'Describe your pets if any'}),
            'employment_status': forms.TextInput(attrs={'class': 'form-control',
                                              'placeholder': 'Your current employment status'})
        }