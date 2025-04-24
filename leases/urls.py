from django.urls import path
from . import views

app_name = 'leases'

urlpatterns = [
    path('', views.lease_list, name='lease_list'),
    path('landlord/', views.landlord_leases, name='landlord_leases'),
    path('tenant/', views.tenant_leases, name='tenant_leases'),
    path('create/', views.lease_create, name='lease_create'),
    path('<int:pk>/', views.lease_detail, name='lease_detail'),
    path('<int:pk>/edit/', views.lease_edit, name='lease_edit'),
    path('<int:pk>/delete/', views.lease_delete, name='lease_delete'),
    path('<int:pk>/sign/landlord/', views.landlord_sign, name='landlord_sign'),
    path('<int:pk>/sign/tenant/', views.tenant_sign, name='tenant_sign'),
    path('<int:pk>/document/add/', views.add_document, name='add_document'),
]