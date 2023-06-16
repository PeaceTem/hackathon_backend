from django.db import models
from django.contrib.auth.models import User
# Create your models here.


"""
Department(name, description)

Create a parent institution
"""
class Object(models.Model):
    """
    This object is the main db object used in the project
    It can exist as any of the following(entity, instance, key, value)  4 possible combinations
    (-entity, instance, -key, value)
    (-entity, instance, key, -value)
    (entity, -instance, -key, value)
    (entity, -instance, key, -value)
    This is the prestigious university of Ibadan. The first and the best university in Nigeria. It is located in Ibadan, Oyo state, Nigeria.
    
    """



    name = models.CharField(max_length=200, )
    description = models.TextField(max_length=1000, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='objects')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_entity = models.BooleanField(default=False)
    is_key = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='object')

    """
    University of Ibadan is an instance of the root object
    faculty is an entity in university of ibadan
    These are the instances of faculty( science, technology, etc.)
    faculty is a child of the entity university(or school)
    department is a child of the faculty
    There are many instances of the department

    An Example
    - University: #UI
        - Faculty: #Science(UI) #Technology #Art #Education
            - Department: #Computer Science#(Science) 
        

    The university entity will be created by default when registering the institution
    
    """

    def __str__(self):
        return f"{self.name}"
    

    class Meta:
        ordering=["name"]
        verbose_name_plural = "Objects"




