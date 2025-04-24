from django.urls import path
from . import views

app_name = 'maintenance'

urlpatterns = [
    path('', views.maintenance_list, name='maintenance_list'),
    path('landlord/', views.maintenance_list, name='landlord_requests'),  # Added this line for landlord views
    path('create/', views.maintenance_create, name='maintenance_create'),
    path('<int:pk>/', views.maintenance_detail, name='maintenance_detail'),
    path('<int:pk>/update/', views.maintenance_update, name='maintenance_update'),
    path('<int:pk>/add-image/', views.add_maintenance_image, name='add_maintenance_image'),
]