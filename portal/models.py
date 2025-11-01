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
