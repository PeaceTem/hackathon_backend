from django.db import models

# Create your models here.

class Faculty(models.Model):
    name = models.CharField(max_length=100)
    

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = 'Faculties'
        ordering = ["name"]





