from django import forms
from .models import Document, Shipment

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'document_type', 'file', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter document title'}),
            'document_type': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional description'}),
        }

class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ['tracking_number', 'shipment_type', 'status', 'origin', 'destination', 'description', 'estimated_delivery']
        widgets = {
            'tracking_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., TRK-2025-001'}),
            'shipment_type': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'origin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Origin country/port'}),
            'destination': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Destination country/port'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Shipment details'}),
            'estimated_delivery': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
