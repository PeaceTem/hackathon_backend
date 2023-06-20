from django.db import models
from faculty.models import Faculty
# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True, blank=True, related_name='departments')


    def __str__(self):
        return f"{self.name}"
    
