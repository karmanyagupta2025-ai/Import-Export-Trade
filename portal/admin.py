from django.contrib import admin
from .models import Document, Shipment

@admin.register (Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display=['title','document_type','uploaded_by','uploaded_at']
    list_filter = ['document_type','uploaded_at']
    search_fields = ['title','description']
@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ['tracking_number', 'shipment_type', 'status', 'origin', 'destination', 'estimated_delivery', 'created_by']
    list_filter = ['status', 'shipment_type', 'created_at']
    search_fields = ['tracking_number', 'origin', 'destination']

# Register your models here.
