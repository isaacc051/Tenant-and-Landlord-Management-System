from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('create/', views.property_create, name='property_create'),
    path('<int:pk>/', views.property_detail, name='property_detail'),
    path('<int:pk>/update/', views.property_update, name='property_update'),
    path('<int:pk>/delete/', views.property_delete, name='property_delete'),
    path('my-properties/', views.landlord_properties, name='landlord_properties'),
    path('<int:property_id>/add-image/', views.add_property_image, name='add_property_image'),
    path('<int:property_id>/add-document/', views.add_property_document, name='add_property_document'),
    path('search/', views.property_search, name='property_search'),
    path('<int:property_id>/apply/', views.apply_for_property, name='apply_for_property'),
    path('my-applications/', views.tenant_applications, name='tenant_applications'),
    path('applications/', views.landlord_applications, name='landlord_applications'),
    path('applications/<int:application_id>/', views.application_detail, name='application_detail'),
    path('applications/<int:application_id>/<str:status>/', views.update_application_status, name='update_application_status'),
    path('toggle-compare/', views.toggle_compare, name='toggle_compare'),
    path('clear-compare/', views.clear_compare, name='clear_compare'),
    path('compare/', views.property_compare, name='property_compare'),
]
