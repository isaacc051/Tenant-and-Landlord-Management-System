from allauth.account.adapter import DefaultAccountAdapter
from django.http import HttpRequest

class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Custom adapter for django-allauth to handle saving user_type during signup
    """
    def save_user(self, request, user, form, commit=True):
        """
        This is called when saving user via allauth registration.
        We override this to save the user_type field.
        """
        # First save the user using the parent method
        user = super().save_user(request, user, form, commit=False)
        
        # Get data from the custom field in the signup form
        user_type = request.POST.get('user_type')
        
        # Save the user type if it's provided
        if user_type:
            user.user_type = user_type
            
        if commit:
            user.save()
            
        return user