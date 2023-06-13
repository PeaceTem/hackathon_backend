from django.urls import path

from .views import *


urlpatterns = [
    path('venue', testing, name='venue'),
    path('register', CreateSuperUser.as_view(), name='register'),
    path('matrix', TimeMatrix.as_view(), name='matrix'),
    path('pdf', GeneratePDF.as_view(), name="pdf"),
    path('venue/<str:venue>', VenueTimetable.as_view(), name='venue-timetable'),
    path('schedule', ScheduleCourses.as_view(), name="schedule-courses"),
]