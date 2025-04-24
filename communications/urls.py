from django.urls import path
from . import views

app_name = 'communications'

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('sent/', views.sent_messages, name='sent_messages'),
    path('compose/', views.compose_message, name='compose_message'),
    path('compose/<int:recipient_id>/', views.compose_message, name='compose_message_to'),
    path('message/<int:message_id>/', views.message_detail, name='message_detail'),
    path('message/<int:message_id>/delete/', views.delete_message, name='delete_message'),
    path('property/<int:property_id>/contact/', views.contact_landlord, name='contact_landlord'),
]