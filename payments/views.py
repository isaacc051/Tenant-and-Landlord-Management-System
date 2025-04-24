from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Count, Q
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import uuid
import datetime
import stripe

from .models import Payment, PaymentReminder
from .forms import PaymentForm, PaymentDateRangeForm
from leases.models import Lease

# Set your Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def payment_list(request):
    """View for landlords to see all payments for their properties."""
    if request.user.user_type != 'landlord':
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
    # Get all payments for properties owned by the landlord
    payments = Payment.objects.filter(
        lease__property__owner=request.user
    ).select_related('tenant', 'lease', 'lease__property').order_by('-payment_date')
    
    # Filter payments based on form inputs
    form = PaymentDateRangeForm(request.GET or None)
    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        payment_type = form.cleaned_data.get('payment_type')
        status = form.cleaned_data.get('status')
        
        if start_date:
            payments = payments.filter(payment_date__date__gte=start_date)
        if end_date:
            payments = payments.filter(payment_date__date__lte=end_date)
        if payment_type:
            payments = payments.filter(payment_type=payment_type)
        if status:
            payments = payments.filter(status=status)
    
    # Calculate statistics for dashboard
    total_paid = payments.filter(status='completed').aggregate(Sum('amount'))['amount__sum'] or 0
    pending_payments = payments.filter(status='pending').count()
    
    context = {
        'payments': payments[:50],  # Limit to 50 most recent payments
        'total_paid': total_paid,
        'pending_payments': pending_payments,
        'form': form,
    }
    return render(request, 'payments/landlord_dashboard.html', context)

@login_required
def payment_history(request):
    """View for tenants to see their payment history."""
    if request.user.user_type != 'tenant':
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
    # Get all payments made by the tenant
    payments = Payment.objects.filter(
        tenant=request.user
    ).select_related('lease', 'lease__property').order_by('-payment_date')
    
    # Filter payments based on form inputs
    form = PaymentDateRangeForm(request.GET or None)
    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        payment_type = form.cleaned_data.get('payment_type')
        status = form.cleaned_data.get('status')
        
        if start_date:
            payments = payments.filter(payment_date__date__gte=start_date)
        if end_date:
            payments = payments.filter(payment_date__date__lte=end_date)
        if payment_type:
            payments = payments.filter(payment_type=payment_type)
        if status:
            payments = payments.filter(status=status)
    
    # Calculate total payments
    total_paid = payments.filter(status='completed').aggregate(Sum('amount'))['amount__sum'] or 0
    
    context = {
        'payments': payments,
        'total_paid': total_paid,
        'form': form,
    }
    return render(request, 'payments/payment_history.html', context)

@login_required
def make_payment(request, lease_id):
    """View for tenants to make a payment for a specific lease."""
    if request.user.user_type != 'tenant':
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
    lease = get_object_or_404(Lease, id=lease_id, tenant=request.user)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment_type = form.cleaned_data.get('payment_type')
            
            # Set the amount based on payment type
            if payment_type == 'rent':
                amount = lease.monthly_rent
            elif payment_type == 'deposit':
                amount = lease.security_deposit
            else:
                # For late fees or other payment types
                amount = form.cleaned_data.get('amount')
            
            # Create a payment record (initially pending)
            payment = Payment.objects.create(
                tenant=request.user,
                lease=lease,
                amount=amount,
                payment_type=payment_type,
                payment_method='stripe',  # Always use Stripe
                status='pending',
                due_date=timezone.now().date(),
                transaction_id=f"TRX-{uuid.uuid4().hex[:8].upper()}"
            )
            
            try:
                # Convert amount to pence (Stripe uses smallest currency unit)
                amount_in_pence = int(amount * 100)
                
                # Create a payment intent with Stripe
                payment_intent = stripe.PaymentIntent.create(
                    amount=amount_in_pence,
                    currency='gbp',  # UK currency
                    payment_method_types=['card'],
                    metadata={
                        'payment_id': payment.id,
                        'tenant_id': request.user.id,
                        'lease_id': lease.id,
                        'payment_type': payment_type
                    }
                )
                
                # Store the payment intent ID for later reference
                payment.transaction_id = payment_intent.id
                payment.save()
                
                # Redirect to the payment processing page with Stripe details
                return render(request, 'payments/process_payment.html', {
                    'payment': payment,
                    'lease': lease,
                    'client_secret': payment_intent.client_secret,
                    'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
                    'amount': amount
                })
                
            except stripe.error.StripeError as e:
                # Handle Stripe errors
                payment.status = 'failed'
                payment.notes = f"Payment failed: {str(e)}"
                payment.save()
                messages.error(request, f"Payment processing error: {str(e)}")
                return redirect('payments:payment_history')
    else:
        form = PaymentForm()
    
    context = {
        'form': form,
        'lease': lease,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'payments/make_payment.html', context)

@login_required
def payment_confirmation(request, payment_id):
    """View to show payment confirmation details."""
    payment = get_object_or_404(Payment, id=payment_id)
    
    # Security check - only allow the tenant or landlord to view the confirmation
    if request.user != payment.tenant and request.user != payment.lease.property.owner:
        messages.error(request, "You don't have permission to view this payment confirmation.")
        return redirect('home')
    
    context = {
        'payment': payment,
    }
    return render(request, 'payments/payment_confirmation.html', context)

@login_required
def payment_invoice(request, payment_id):
    """View to show a printable payment invoice/receipt."""
    payment = get_object_or_404(Payment, id=payment_id)
    
    # Security check - only allow the tenant or landlord to view the invoice
    if request.user != payment.tenant and request.user != payment.lease.property.owner:
        messages.error(request, "You don't have permission to view this invoice.")
        return redirect('home')
    
    context = {
        'payment': payment,
        'today': timezone.now(),
    }
    return render(request, 'payments/payment_invoice.html', context)

@login_required
def lease_payments(request, lease_id):
    """View to show all payments for a specific lease."""
    lease = get_object_or_404(Lease, id=lease_id)
    
    # Security check - only allow the tenant or landlord to view the lease payments
    if request.user != lease.tenant and request.user != lease.property.owner:
        messages.error(request, "You don't have permission to view these payments.")
        return redirect('home')
    
    payments = Payment.objects.filter(lease=lease).order_by('-payment_date')
    
    context = {
        'lease': lease,
        'payments': payments,
    }
    return render(request, 'payments/lease_payments.html', context)

@login_required
def payment_reminders(request):
    """View for landlords to manage payment reminders."""
    if request.user.user_type != 'landlord':
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
    # Get all active leases for properties owned by the landlord
    leases = Lease.objects.filter(
        property__owner=request.user,
        end_date__gte=timezone.now().date(),
    ).select_related('tenant', 'property')
    
    # Get all payment reminders
    reminders = PaymentReminder.objects.filter(
        lease__property__owner=request.user
    ).select_related('lease', 'lease__tenant')
    
    if request.method == 'POST':
        lease_id = request.POST.get('lease_id')
        due_date = request.POST.get('due_date')
        reminder_date = request.POST.get('reminder_date')
        
        if lease_id and due_date and reminder_date:
            try:
                lease = Lease.objects.get(id=lease_id, property__owner=request.user)
                PaymentReminder.objects.create(
                    lease=lease,
                    due_date=datetime.datetime.strptime(due_date, '%Y-%m-%d').date(),
                    reminder_date=datetime.datetime.strptime(reminder_date, '%Y-%m-%d').date(),
                    sent=False
                )
                messages.success(request, "Payment reminder scheduled successfully!")
                return redirect('payments:payment_reminders')
            except Exception as e:
                messages.error(request, f"Error scheduling reminder: {str(e)}")
    
    context = {
        'leases': leases,
        'reminders': reminders,
    }
    return render(request, 'payments/payment_reminders.html', context)

@csrf_exempt
def stripe_webhook(request):
    """
    Webhook handler for Stripe payment events.
    This endpoint receives events from Stripe when payment statuses change.
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        # Verify the event is from Stripe using the webhook secret
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
        
    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        
        # Extract the payment ID from metadata
        payment_id = payment_intent.get('metadata', {}).get('payment_id')
        
        if payment_id:
            try:
                # Update the payment status in your database
                payment = Payment.objects.get(id=payment_id)
                payment.status = 'completed'
                payment.save()
                
                # Generate a receipt if needed
                payment.generate_receipt()
                
            except Payment.DoesNotExist:
                # Handle the case where payment object doesn't exist
                return HttpResponse(status=404)
                
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        payment_id = payment_intent.get('metadata', {}).get('payment_id')
        
        if payment_id:
            try:
                # Update the payment status to failed
                payment = Payment.objects.get(id=payment_id)
                payment.status = 'failed'
                payment.notes = f"Payment failed: {payment_intent.get('last_payment_error', {}).get('message', 'Unknown error')}"
                payment.save()
                
            except Payment.DoesNotExist:
                return HttpResponse(status=404)
    
    # Return a 200 response to acknowledge receipt of the event
    return HttpResponse(status=200)