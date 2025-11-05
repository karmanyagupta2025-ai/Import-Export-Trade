from django.db import models
from django.contrib.auth.models import User


class Document(models.Model):
    DOCUMENT_TYPES = [
        ('import', 'Import Document'),
        ('export', 'Export Document'),
    ]

    title = models.CharField(max_length=200)
    document_type = models.CharField(max_length=10, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='documents/%Y/%m/%d/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} - {self.get_document_type_display()}"

    class Meta:
        ordering = ['-uploaded_at']

# Create your models here.
class Shipment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_transit', 'In Transit'),
        ('customs', 'Customs Clearance'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    SHIPMENT_TYPE = [
        ('import', 'Import'),
        ('export', 'Export'),
    ]
    
    tracking_number = models.CharField(max_length=100, unique=True)
    shipment_type = models.CharField(max_length=10, choices=SHIPMENT_TYPE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    origin = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    estimated_delivery = models.DateField()
    
    def __str__(self):
        return f"{self.tracking_number} - {self.get_status_display()}"
    
    class Meta:
        ordering = ['-created_at']
class Trade(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        product = models.CharField(max_length=200)
        quantity = models.PositiveIntegerField()
        price = models.DecimalField(max_digits=10, decimal_places=2)
        date = models.DateField()
        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return f"{self.product} ({self.quantity}) - {self.user.username}"
class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.user.username}-{self.action} at {self.timestamp}'

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

