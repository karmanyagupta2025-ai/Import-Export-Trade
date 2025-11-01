from django.contrib import admin
from .models import Document
@admin.register (Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display=['title','document_type','uploaded_by','uploaded_at']
    list_filter = ['document_type','uploaded_at']
    search_fields = ['title','description']

# Register your models here.
