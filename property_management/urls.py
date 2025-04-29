from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),  # Added this line to include your custom accounts URLs
    path('', home, name='home'),
    path('properties/', include(('properties.urls', 'properties'), namespace='properties')),
    path('leases/', include('leases.urls')),
    path('maintenance/', include('maintenance.urls')),
    path('payments/', include('payments.urls')),
    path('communications/', include('communications.urls')),
    path('notifications/', include('notifications.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
