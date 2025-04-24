from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from django.db.models import Q
from .models import Message
from .forms import MessageForm, PropertyMessageForm
from properties.models import Property

@login_required
def inbox(request):
    """View for displaying received messages"""
    user_messages = Message.objects.filter(recipient=request.user).order_by('-sent_at')
    return render(request, 'communications/inbox.html', {'user_messages': user_messages})

@login_required
def sent_messages(request):
    """View for displaying sent messages"""
    user_messages = Message.objects.filter(sender=request.user).order_by('-sent_at')
    return render(request, 'communications/sent_messages.html', {'user_messages': user_messages})

@login_required
def message_detail(request, message_id):
    """View for displaying a specific message"""
    user_message = get_object_or_404(Message, id=message_id)
    
    # Security check: Only sender or recipient can view the message
    if request.user != user_message.sender and request.user != user_message.recipient:
        django_messages.error(request, "You don't have permission to view this message.")
        return redirect('communications:inbox')
    
    # Mark as read if the viewer is the recipient
    if request.user == user_message.recipient and not user_message.read:
        user_message.read = True
        user_message.save()
    
    return render(request, 'communications/message_detail.html', {'user_message': user_message})

@login_required
def compose_message(request, recipient_id=None):
    """View for composing a new message"""
    recipient = None
    if recipient_id:
        from accounts.models import User
        recipient = get_object_or_404(User, id=recipient_id)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            
            # If recipient_id is provided in URL
            if recipient_id:
                message.recipient = recipient
            else:
                # Get recipient from the form
                recipient_id = request.POST.get('recipient')
                if recipient_id:
                    from accounts.models import User
                    message.recipient = get_object_or_404(User, id=recipient_id)
                
            message.save()
            django_messages.success(request, "Message sent successfully!")
            return redirect('communications:sent_messages')
    else:
        form = MessageForm()
    
    # Get all users excluding the current user to populate the recipient dropdown
    from accounts.models import User
    users = User.objects.exclude(id=request.user.id).order_by('first_name', 'last_name')
    
    return render(request, 'communications/compose_message.html', {
        'form': form,
        'recipient': recipient,
        'users': users  # Pass users to the template
    })

@login_required
def contact_landlord(request, property_id):
    """View for contacting a landlord about a specific property"""
    property_obj = get_object_or_404(Property, id=property_id)
    
    # Check if the current user is the landlord
    if request.user == property_obj.owner:
        django_messages.warning(request, "You cannot send a message to yourself.")
        return redirect('properties:property_detail', pk=property_id)
    
    if request.method == 'POST':
        form = PropertyMessageForm(request.POST, property_obj=property_obj)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = property_obj.owner
            message.related_property = property_obj
            message.save()
            
            django_messages.success(request, f"Your message has been sent to {property_obj.owner.get_full_name() or property_obj.owner.username}!")
            return redirect('properties:property_detail', pk=property_id)
    else:
        form = PropertyMessageForm(property_obj=property_obj)
    
    return render(request, 'communications/contact_landlord.html', {
        'form': form,
        'property': property_obj
    })

@login_required
def delete_message(request, message_id):
    """View for deleting a message"""
    user_message = get_object_or_404(Message, id=message_id)
    
    # Security check: Only sender or recipient can delete the message
    if request.user != user_message.sender and request.user != user_message.recipient:
        django_messages.error(request, "You don't have permission to delete this message.")
        return redirect('communications:inbox')
    
    if request.method == 'POST':
        user_message.delete()
        django_messages.success(request, "Message deleted successfully!")
        return redirect('communications:inbox')
    
    return render(request, 'communications/delete_message_confirm.html', {'user_message': user_message})