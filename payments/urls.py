from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.payment_list, name='payment_list'),
    path('history/', views.payment_history, name='payment_history'),
    path('make/<int:lease_id>/', views.make_payment, name='make_payment'),
    path('confirmation/<int:payment_id>/', views.payment_confirmation, name='payment_confirmation'),
    path('invoice/<int:payment_id>/', views.payment_invoice, name='payment_invoice'),
    path('lease/<int:lease_id>/', views.lease_payments, name='lease_payments'),
    path('reminders/', views.payment_reminders, name='payment_reminders'),
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
]