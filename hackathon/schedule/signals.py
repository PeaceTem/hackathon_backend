
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *





# The cells that will be created should be based on the department

# this must be changed to work for each department
@receiver(post_save, sender=Row)
def create_cells_by_column(sender, instance, created, *args, **kwargs):
    if created:
        columns = Column.objects.all()
        for column in columns:
            Cell.objects.create(row=instance, column=column)



@receiver(post_save, sender=Column)
def create_cells_by_row(sender, instance, created, *args, **kwargs):
    if created:
        rows = Row.objects.all()
        for row in rows:
            Cell.objects.create(row=row, column=instance)

