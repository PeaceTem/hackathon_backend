from django.urls import path

from .views import *


urlpatterns = [
    path('venue', testing, name='venue'),
    path('register', CreateSuperUser.as_view(), name='register'),
    path('matrix/<slug:slug>', TimeMatrix.as_view(), name='matrix'),
    path('pdf', GeneratePDF.as_view(), name="pdf"),
    path('venue/<str:venue>', VenueTimetable.as_view(), name='venue-timetable'),
    path('<slug:slug>', ScheduleCourses.as_view(), name="schedule-courses"),
    path('department-exclusion', DepartmentExclusion.as_view(), name="department-exclusion")
]





