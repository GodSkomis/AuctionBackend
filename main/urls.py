from django.urls import path
from .views import *

urlpatterns = [
    path('manual_update/', manual_update)
]
