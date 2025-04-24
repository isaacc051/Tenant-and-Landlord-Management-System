from django.contrib import admin
from .models import Property, PropertyImage, PropertyDocument

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1

class PropertyDocumentInline(admin.TabularInline):
    model = PropertyDocument
    extra = 1

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'property_type', 'address', 'town_city', 'monthly_rent', 'available')
    list_filter = ('property_type', 'town_city', 'available')
    search_fields = ('title', 'address', 'description')
    inlines = [PropertyImageInline, PropertyDocumentInline]

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property', 'caption', 'uploaded_at')

@admin.register(PropertyDocument)
class PropertyDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'property', 'uploaded_at')
