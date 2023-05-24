from django.urls import path

from .views import *


urlpatterns = [
    path('', testing, name='testing'),
    path('register', CreateSuperUser.as_view(), name='register'),
    path('matrix', TimeMatrix.as_view(), name='matrix'),
]