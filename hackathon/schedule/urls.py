from django.urls import path

from .views import *


urlpatterns = [
    path('venue', testing, name='venue'),
    path('register', CreateSuperUser.as_view(), name='register'),
    path('matrix', TimeMatrix.as_view(), name='matrix'),
]