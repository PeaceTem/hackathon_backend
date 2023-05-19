from django.contrib import admin

# Register your models here.

from .models import *


admin.site.register(CourseCode)
admin.site.register(Venue)
admin.site.register(Day)
admin.site.register(Supervisor)
admin.site.register(Column)
admin.site.register(Row)
admin.site.register(TimeSlot)
admin.site.register(Cell)
