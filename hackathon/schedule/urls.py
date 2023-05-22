from django.urls import path

from .views import *


urlpatterns = [
    path('', testing, name='testing'),
]