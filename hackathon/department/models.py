from typing import Iterable, Optional
from django.db import models
from faculty.models import Faculty
# from schedule.models import CourseCode
# Create your models here.
from django.utils.text import slugify

class Department(models.Model):
    name = models.CharField(max_length=120)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True, blank=True, related_name='departments')
    slug = models.SlugField(default="none")

    # faculty_courses = models.ManyToManyField(CourseCode, related_name="departments")

    def __str__(self):
        return f"{self.name}"
    
    def save(self, *args, **kwargs) -> None:
        if self.name:
            self.slug = slugify(self.name)

        return super().save(*args, **kwargs)


